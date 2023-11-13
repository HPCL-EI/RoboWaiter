import math
import json
import openai
import utils
from memory import CoreMemory, ArchivalMemory, RecallMemory


def construct_system_with_memory(system, core_memory, memory_edit_timestamp, archival_memory=None, recall_memory=None):
    full_system_message = "\n".join(
        [
            system,
            "\n",
            f"### Memory [last modified: {memory_edit_timestamp}]",
            f"{len(recall_memory) if recall_memory else 0} previous messages between you and the user are stored in recall memory (use functions to access them)",
            f"{len(archival_memory) if archival_memory else 0} total memories you created are stored in archival memory (use functions to access them)",
            "\nCore memory shown below (limited in size, additional information stored in archival / recall memory):",
            "<persona>",
            core_memory.persona,
            "</persona>",
            "<human>",
            core_memory.human,
            "</human>",
        ]
    )
    return full_system_message


def initialize_message_sequence(system, core_memory, archival_memory=None, recall_memory=None):
    memory_edit_timestamp = utils.get_local_time()
    full_system_message = construct_system_with_memory(system, core_memory, memory_edit_timestamp,
                                                       archival_memory=archival_memory, recall_memory=recall_memory)
    messages = [
        {"role": "system", "content": full_system_message},
    ]
    return messages


class Agent:
    def __init__(self, model, system, functions_description, persona_notes, human_notes):
        self.model = model
        self.system = system
        self.functions_description = functions_description
        self.core_memory = CoreMemory(persona_notes, human_notes)
        self.archival_memory = ArchivalMemory()
        self.recall_memory = RecallMemory()
        self.messages = initialize_message_sequence(self.system, self.core_memory)
        self.functions = {
            "send_message": self.send_ai_message,
            "core_memory_append": self.edit_memory_append,
            "core_memory_replace": self.edit_memory_replace,
            "conversation_search": self.recall_memory_search,
            "archival_memory_insert": self.archival_memory_insert,
            "archival_memory_search": self.archival_memory_search,
        }

    def rebuild_memory(self):
        new_system_message = initialize_message_sequence(
            self.system,
            self.core_memory,
            archival_memory=self.archival_memory,
            recall_memory=self.recall_memory,
        )[0]
        self.messages = [new_system_message] + self.messages[1:]

    def send_ai_message(self, message):
        print("RoboWaiter: " + message)

    def edit_memory_append(self, name, content):
        self.core_memory.append(name, content)
        self.rebuild_memory()

    def edit_memory_replace(self, name, old_content, new_content):
        self.core_memory.replace(name, old_content, new_content)
        self.rebuild_memory()

    def recall_memory_search(self, query, count=5, page=0):
        results, total = self.recall_memory.text_search(query, count=count, start=page * count)
        num_pages = math.ceil(total / count) - 1
        if len(results) == 0:
            results_str = f"No results found."
        else:
            results_pref = f"Showing {len(results)} of {total} results (page {page}/{num_pages}):"
            results_formatted = [f"timestamp: {d['timestamp']}, {d['message']['role']} - {d['message']['content']}" for
                                 d in results]
            results_str = f"{results_pref} {json.dumps(results_formatted)}"
        return results_str

    def archival_memory_insert(self, content):
        self.archival_memory.insert(content)

    def archival_memory_search(self, query, count=5, page=0):
        results, total = self.archival_memory.search(query, count=count, start=page * count)
        num_pages = math.ceil(total / count) - 1
        if len(results) == 0:
            results_str = f"No results found."
        else:
            results_pref = f"Showing {len(results)} of {total} results (page {page}/{num_pages}):"
            results_formatted = [f"timestamp: {d['timestamp']}, memory: {d['content']}" for d in results]
            results_str = f"{results_pref} {json.dumps(results_formatted)}"
        return results_str

    def append_to_messages(self, added_messages):
        added_messages_with_timestamp = [{"timestamp": utils.get_local_time(), "message": msg} for msg in added_messages]
        self.recall_memory.message_logs.extend(added_messages_with_timestamp)
        for msg in added_messages:
            msg.pop("api_response", None)
            msg.pop("api_args", None)
        self.messages = self.messages + added_messages

    def handle_ai_response(self, response_message):
        messages = []
        if response_message.get("function_call"):
            print("### Internal monologue: " + (response_message.content if response_message.content else ""))
            messages.append(response_message)
            function_name = response_message["function_call"]["name"]
            try:
                function_to_call = self.functions[function_name]
            except KeyError as e:
                error_msg = f"No function named {function_name}"
                function_response = utils.package_function_response(False, error_msg)
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                return messages, True
            try:
                raw_function_args = response_message["function_call"]["arguments"]
                function_args = utils.parse_json(raw_function_args)
            except Exception as e:
                error_msg = f"Error parsing JSON for function '{function_name}' arguments: {raw_function_args}"
                function_response = utils.package_function_response(False, error_msg)
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                return messages, True
            try:
                function_response_string = function_to_call(**function_args)
                function_response = utils.package_function_response(True, function_response_string)
                function_failed = False
            except Exception as e:
                error_msg = f"Error calling function {function_name} with args {function_args}: {str(e)}"
                function_response = utils.package_function_response(False, error_msg)
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                return messages, True

            # If no failures happened along the way: ...
            if function_response_string:
                print(f"Success: {function_response_string}")
            else:
                print(f"Success")
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )
        else:
            # Standard non-function reply
            # print("### Internal monologue: " + (response_message.content if response_message.content else ""))
            print("### Internal monologue: " + (response_message['content'] if response_message['content'] else ""))
            messages.append(response_message)
            function_failed = None

        return messages, function_failed

    def step(self, user_message):
        input_message_sequence = self.messages + [{"role": "user", "content": user_message}]

        # 原来的通信方式
        # response = openai.ChatCompletion.create(model=self.model, messages=input_message_sequence,
        #                                         functions=self.functions_description, function_call="auto")
        #
        # response_message = response.choices[0].message
        # response_message_copy = response_message.copy()

        # ===我们的通信方式 "tools": self.functions_description 不起作用===
        import requests
        url = "https://45.125.46.134:25344/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "RoboWaiter",
            "messages": input_message_sequence,
            # "functions":self.functions_description,
            # "function_call":"auto"
            # "function_call":self.functions_description
            "tools": self.functions_description
        }
        response = requests.post(url, headers=headers, json=data, verify=False)
        if response.status_code == 200:
            result = response.json()
            response_message = result['choices'][0]['message']
        else:
            response_message = "大模型请求失败:"+ str(response.status_code)
        response_message_copy = response_message
        # ===我们的通信方式 "tools": self.functions_description 不起作用===


        all_response_messages, function_failed = self.handle_ai_response(response_message)
        assert "api_response" not in all_response_messages[0], f"api_response already in {all_response_messages[0]}"
        all_response_messages[0]["api_response"] = response_message_copy
        assert "api_args" not in all_response_messages[0], f"api_args already in {all_response_messages[0]}"
        all_response_messages[0]["api_args"] = {
            "model": self.model,
            "messages": input_message_sequence,
            "functions": self.functions,
        }

        if user_message is not None:
            all_new_messages = [{"role": "user", "content": user_message}] + all_response_messages
        else:
            all_new_messages = all_response_messages

        self.append_to_messages(all_new_messages)
