import uuid


def generate_id() -> int:
    """Generate a unique UUID and convert it to an 15-digit integer"""
    id = int(str(uuid.uuid4().int)[:15])
    return id