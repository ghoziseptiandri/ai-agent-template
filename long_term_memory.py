import json
from pathlib import Path

MEMORY_FILE = Path("long_term_memory.json")


def load_long_term_memory() -> dict:
    if not MEMORY_FILE.exists():
        return {}

    if MEMORY_FILE.stat().st_size == 0:
        return {}

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)


def save_long_term_memory(memory: dict) -> None:
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=2)


def save_memory(key: str, value: str) -> str:
    memory = load_long_term_memory()

    if key in memory:
        return f"Memory key '{key}' already exists."

    memory[key] = value
    save_long_term_memory(memory)

    #print(f"🧠 Memory saved: {key} = {value}")
    return f"Saved {key} = {value}"


def update_memory(key: str, value: str) -> str:
    memory = load_long_term_memory()

    if key not in memory:
        return f"Memory key '{key}' does not exist."

    old_value = memory[key]
    memory[key] = value
    save_long_term_memory(memory)

    #print(f"🧠 Memory updated: {key}: {old_value} → {value}")
    return f"Updated {key} from {old_value} to {value}"


def delete_memory(key: str) -> str:
    memory = load_long_term_memory()

    if key not in memory:
        return f"Memory key '{key}' does not exist."

    old_value = memory.pop(key)
    save_long_term_memory(memory)

    #print(f"🧠 Memory deleted: {key} = {old_value}")
    return f"Deleted memory {key}"