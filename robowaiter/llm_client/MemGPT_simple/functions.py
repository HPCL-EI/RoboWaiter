FUNCTIONS = [
    {
        "name": "send_message",
        "description": "Sends a message to the human user",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message contents. All unicode (including emojis) are supported.",
                },
            },
            "required": ["message"],
        },
    },
    {
        "name": "core_memory_append",
        "description": "Append to the contents of core memory.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Section of the memory to be edited (persona or human).",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the memory. All unicode (including emojis) are supported.",
                },
            },
            "required": ["name", "content"],
        },
    },
    {
        "name": "core_memory_replace",
        "description": "Replace to the contents of core memory. To delete memories, use an empty string for new_content.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Section of the memory to be edited (persona or human).",
                },
                "old_content": {
                    "type": "string",
                    "description": "String to replace. Must be an exact match.",
                },
                "new_content": {
                    "type": "string",
                    "description": "Content to write to the memory. All unicode (including emojis) are supported.",
                },
            },
            "required": ["name", "old_content", "new_content"],
        },
    },
    {
        "name": "conversation_search",
        "description": "Search prior conversation history using case-insensitive string matching.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "String to search for.",
                },
                "page": {
                    "type": "integer",
                    "description": "Allows you to page through results. Only use on a follow-up query. Defaults to 0 (first page).",
                },
            },
            "required": ["query", "page"],
        },
    },
    {
        "name": "archival_memory_insert",
        "description": "Add to archival memory. Make sure to phrase the memory contents such that it can be easily queried later.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Content to write to the memory. All unicode (including emojis) are supported.",
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "archival_memory_search",
        "description": "Search archival memory using semantic (embedding-based) search.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "String to search for.",
                },
                "page": {
                    "type": "integer",
                    "description": "Allows you to page through results. Only use on a follow-up query. Defaults to 0 (first page).",
                },
            },
            "required": ["query", "page"],
        },
    },
]
