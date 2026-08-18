import json

import long_term_memory


def test_save_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(
        long_term_memory,
        "MEMORY_FILE",
        test_file
    )

    result = long_term_memory.save_memory(
        "favorite_number",
        "42"
    )

    assert result == "Saved favorite_number = 42"

    with open(test_file, "r") as file:
        data = json.load(file)

    assert data["favorite_number"] == "42"


def test_update_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(
        long_term_memory,
        "MEMORY_FILE",
        test_file
    )

    long_term_memory.save_memory(
        "favorite_number",
        "42"
    )

    result = long_term_memory.update_memory(
        "favorite_number",
        "7"
    )

    assert "Updated favorite_number" in result

    with open(test_file, "r") as file:
        data = json.load(file)

    assert data["favorite_number"] == "7"


def test_delete_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(
        long_term_memory,
        "MEMORY_FILE",
        test_file
    )

    long_term_memory.save_memory(
        "favorite_number",
        "42"
    )

    result = long_term_memory.delete_memory(
        "favorite_number"
    )

    assert result == "Deleted memory favorite_number"

    with open(test_file, "r") as file:
        data = json.load(file)

    assert "favorite_number" not in data

def test_save_duplicate_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(
        long_term_memory,
        "MEMORY_FILE",
        test_file
    )

    long_term_memory.save_memory(
        "favorite_number",
        "42"
    )

    result = long_term_memory.save_memory(
        "favorite_number",
        "42"
    )

    assert result == "Memory key 'favorite_number' already exists."


def test_update_missing_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(
        long_term_memory,
        "MEMORY_FILE",
        test_file
    )

    result = long_term_memory.update_memory(
        "favorite_number",
        "7"
    )

    assert result == "Memory key 'favorite_number' does not exist."


def test_delete_missing_memory(tmp_path, monkeypatch):
    test_file = tmp_path / "memory.json"

    monkeypatch.setattr(
        long_term_memory,
        "MEMORY_FILE",
        test_file
    )

    result = long_term_memory.delete_memory(
        "favorite_number"
    )

    assert result == "Memory key 'favorite_number' does not exist."