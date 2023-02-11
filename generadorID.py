import uuid

def generate_id():
    return str(uuid.uuid4())

print(generate_id())