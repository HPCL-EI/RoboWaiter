import os
import json
import demjson3 as demjson
from datetime import datetime

HUMAN_DEFAULT = "customer"
PERSONA_DEFAULT = "robowaiter"
SYSTEM_DEFAULT = "system_gpt3.5"


def get_persona_text(key=PERSONA_DEFAULT):
    dir = "personas"
    filename = key if key.endswith(".txt") else f"{key}.txt"
    file_path = os.path.join(dir, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"No file found for key {key}, path={file_path}")


def get_human_text(key=HUMAN_DEFAULT):
    dir = "humans"
    filename = key if key.endswith(".txt") else f"{key}.txt"
    file_path = os.path.join(dir, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"No file found for key {key}, path={file_path}")

def get_system_text(key=SYSTEM_DEFAULT):
    dir = "system"
    filename = key if key.endswith(".txt") else f"{key}.txt"
    file_path = os.path.join(dir, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"No file found for key {key}, path={file_path}")

def get_local_time():
    local_time = datetime.now()
    formatted_time = local_time.strftime("%Y-%m-%d %I:%M:%S %p %Z%z")
    return formatted_time


def package_user_message(user_message):
    formatted_time = get_local_time()
    packaged_message = {
        "type": "user_message",
        "message": user_message,
        "time": formatted_time,
    }
    return json.dumps(packaged_message, ensure_ascii=False)


def package_function_response(was_success, response_string):
    formatted_time = get_local_time()
    packaged_message = {
        "status": "OK" if was_success else "Failed",
        "message": response_string,
        "time": formatted_time,
    }
    return json.dumps(packaged_message, ensure_ascii=False)


def parse_json(string):
    result = None
    try:
        result = json.loads(string)
        return result
    except Exception as e:
        print(f"Error parsing json with json package: {e}")

    try:
        result = demjson.decode(string)
        return result
    except demjson.JSONDecodeError as e:
        print(f"Error parsing json with demjson package: {e}")
        raise e

