import utils


class CoreMemory(object):
    def __init__(self, persona, human):
        self.persona = persona
        self.human = human

    def __repr__(self) -> str:
        return f"\n### CORE MEMORY ###" + f"\n=== Persona ===\n{self.persona}" + f"\n\n=== Human ===\n{self.human}"

    def edit_persona(self, new_persona):
        self.persona = new_persona

    def edit_human(self, new_human):
        self.human = new_human

    def append(self, field, content, sep="\n"):
        if field == "persona":
            new_content = self.persona + sep + content
            self.edit_persona(new_content)
        elif field == "human":
            new_content = self.human + sep + content
            self.edit_human(new_content)
        else:
            raise KeyError

    def replace(self, field, old_content, new_content):
        if field == "persona":
            if old_content in self.persona:
                new_persona = self.persona.replace(old_content, new_content)
                self.edit_persona(new_persona)
            else:
                raise ValueError("Content not found in persona (make sure to use exact string)")
        elif field == "human":
            if old_content in self.human:
                new_human = self.human.replace(old_content, new_content)
                self.edit_human(new_human)
            else:
                raise ValueError("Content not found in human (make sure to use exact string)")
        else:
            raise KeyError


class ArchivalMemory(object):
    def __init__(self):
        self.archive = []

    def __len__(self):
        return len(self.archive)

    def __repr__(self) -> str:
        if len(self.archive) == 0:
            memory_str = "<empty>"
        else:
            memory_str = "\n".join([d["content"] for d in self.archive])
        return f"\n### ARCHIVAL MEMORY ###" + f"\n{memory_str}"

    def insert(self, memory_string):
        self.archive.append(
            {
                "timestamp": utils.get_local_time(),
                "content": memory_string,
            }
        )

    def search(self, query_string, count=None, start=None):
        # run an (inefficient) case-insensitive match search
        matches = [s for s in self.archive if query_string.lower() in s["content"].lower()]
        # start/count support paging through results
        if start is not None and count is not None:
            return matches[start: start + count], len(matches)
        elif start is None and count is not None:
            return matches[:count], len(matches)
        elif start is not None and count is None:
            return matches[start:], len(matches)
        else:
            return matches, len(matches)


class RecallMemory(object):
    def __init__(self):
        self.message_logs = []

    def __len__(self):
        return len(self.message_logs)

    def __repr__(self) -> str:
        system_count = user_count = assistant_count = function_count = other_count = 0
        for msg in self.message_logs:
            role = msg["message"]["role"]
            if role == "system":
                system_count += 1
            elif role == "user":
                user_count += 1
            elif role == "assistant":
                assistant_count += 1
            elif role == "function":
                function_count += 1
            else:
                other_count += 1
        memory_str = (
                f"Statistics:"
                + f"\n{len(self.message_logs)} total messages"
                + f"\n{system_count} system"
                + f"\n{user_count} user"
                + f"\n{assistant_count} assistant"
                + f"\n{function_count} function"
                + f"\n{other_count} other"
        )
        return f"\n### RECALL MEMORY ###" + f"\n{memory_str}"

    def text_search(self, query_string, count=None, start=None):
        # run an (inefficient) case-insensitive match search
        message_pool = [d for d in self.message_logs if d["message"]["role"] not in ["system", "function"]]
        matches = [
            d for d in message_pool if
            d["message"]["content"] is not None and query_string.lower() in d["message"]["content"].lower()
        ]
        # start/count support paging through results
        if start is not None and count is not None:
            return matches[start: start + count], len(matches)
        elif start is None and count is not None:
            return matches[:count], len(matches)
        elif start is not None and count is None:
            return matches[start:], len(matches)
        else:
            return matches, len(matches)
