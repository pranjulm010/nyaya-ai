chat_memory = []

def save_memory(role, content):

    chat_memory.append({
        "role": role,
        "content": content
    })

def get_memory():

    return chat_memory