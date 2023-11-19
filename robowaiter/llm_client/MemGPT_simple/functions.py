FUNCTIONS = [
    {
        "name": "send_message",
        "description": "给用户发送一条消息",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "消息内容",
                },
            },
            "required": ["message"],
        },
    },
    {
        "name": "core_memory_append",
        "description": "向你的核心记忆中添加内容",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "需要编辑的记忆部分(persona或human)",
                },
                "content": {
                    "type": "string",
                    "description": "要写入记忆的内容",
                },
            },
            "required": ["name", "content"],
        },
    },
    {
        "name": "core_memory_replace",
        "description": "替换核心记忆中的内容。要删除记忆，请将new_content赋值为空",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "需要编辑的记忆部分(persona或human)",
                },
                "old_content": {
                    "type": "string",
                    "description": "替换的字符串，一定要是精确的匹配",
                },
                "new_content": {
                    "type": "string",
                    "description": "要写入记忆的内容",
                },
            },
            "required": ["name", "old_content", "new_content"],
        },
    },
    {
        "name": "conversation_search",
        "description": "搜索回忆存储中的内容",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "需要搜索的字符串",
                },
                "page": {
                    "type": "integer",
                    "description": "允许你对结果分页。默认是0(第1页)",
                },
            },
            "required": ["query", "page"],
        },
    },
    {
        "name": "archival_memory_insert",
        "description": "写入存档记忆。要将写入的内容格式化，以便后续方便查询",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "要写入记忆的内容",
                },
            },
            "required": ["content"],
        },
    },
    {
        "name": "archival_memory_search",
        "description": "搜索存档记忆",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "要搜索的字符串",
                },
                "page": {
                    "type": "integer",
                    "description": "允许你对结果分页。默认是0(第1页)",
                },
            },
            "required": ["query", "page"],
        },
    },
]
