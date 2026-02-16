#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_DATA_FILE = str(Path.home() / ".personal_assistant.json")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _default_data() -> Dict[str, List[Dict[str, Any]]]:
    return {"tasks": [], "notes": []}


def load_data(path: str) -> Dict[str, List[Dict[str, Any]]]:
    file_path = Path(path)
    if not file_path.exists():
        return _default_data()
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _default_data()
    return {
        "tasks": list(raw.get("tasks", [])),
        "notes": list(raw.get("notes", [])),
    }


def save_data(path: str, data: Dict[str, List[Dict[str, Any]]]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def next_id(items: List[Dict[str, Any]]) -> int:
    return max((item.get("id", 0) for item in items), default=0) + 1


def parse_due_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def format_task(task: Dict[str, Any]) -> str:
    status = "✓" if task.get("completed") else " "
    priority = task.get("priority", "medium")
    due = f" (due {task['due']})" if task.get("due") else ""
    return f"[{status}] {task['id']}. {task['description']} [{priority}]{due}"


def format_note(note: Dict[str, Any]) -> str:
    created = note.get("created_at", "unknown")
    return f"{note['id']}. {note['content']} ({created})"


def list_tasks(tasks: List[Dict[str, Any]], show_all: bool) -> None:
    visible = tasks if show_all else [task for task in tasks if not task.get("completed")]
    if not visible:
        print("No tasks to show.")
        return
    for task in visible:
        print(format_task(task))


def list_notes(notes: List[Dict[str, Any]]) -> None:
    if not notes:
        print("No notes saved yet.")
        return
    for note in notes:
        print(format_note(note))


def find_item(items: List[Dict[str, Any]], item_id: int) -> Optional[Dict[str, Any]]:
    for item in items:
        if item.get("id") == item_id:
            return item
    return None


def summarize(data: Dict[str, List[Dict[str, Any]]]) -> None:
    tasks = data.get("tasks", [])
    notes = data.get("notes", [])
    pending = [task for task in tasks if not task.get("completed")]
    completed = [task for task in tasks if task.get("completed")]
    due_candidates = [
        (parse_due_date(task.get("due")), task)
        for task in pending
        if task.get("due")
    ]
    due_candidates = [(due, task) for due, task in due_candidates if due]
    next_due = min(due_candidates, default=(None, None))[1]

    print("Personal Assistant Summary")
    print("--------------------------")
    print(f"Pending tasks: {len(pending)}")
    print(f"Completed tasks: {len(completed)}")
    print(f"Notes stored: {len(notes)}")
    if next_due:
        print(f"Next due: {format_task(next_due)}")
    elif pending:
        print("Next due: No due dates set yet.")
    else:
        print("Next due: No pending tasks.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Your personal assistant CLI.")
    parser.add_argument(
        "--data-file",
        default=DEFAULT_DATA_FILE,
        help=f"Path to data file (default: {DEFAULT_DATA_FILE})",
    )
    subparsers = parser.add_subparsers(dest="command")

    add_task = subparsers.add_parser("add-task", help="Add a new task.")
    add_task.add_argument("description", help="Task description.")
    add_task.add_argument("--due", help="Due date in ISO format (YYYY-MM-DD).")
    add_task.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority.",
    )

    list_task = subparsers.add_parser("list-tasks", help="List tasks.")
    list_task.add_argument("--all", action="store_true", help="Show all tasks.")

    complete_task = subparsers.add_parser("complete-task", help="Complete a task.")
    complete_task.add_argument("task_id", type=int, help="Task ID to complete.")

    delete_task = subparsers.add_parser("delete-task", help="Delete a task.")
    delete_task.add_argument("task_id", type=int, help="Task ID to delete.")

    add_note = subparsers.add_parser("add-note", help="Add a quick note.")
    add_note.add_argument("content", help="Note content.")

    list_note = subparsers.add_parser("list-notes", help="List saved notes.")

    delete_note = subparsers.add_parser("delete-note", help="Delete a note.")
    delete_note.add_argument("note_id", type=int, help="Note ID to delete.")

    subparsers.add_parser("summary", help="Show a quick summary.")
    parser.set_defaults(command="summary")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    data = load_data(args.data_file)
    changed = False

    if args.command == "add-task":
        tasks = data["tasks"]
        task = {
            "id": next_id(tasks),
            "description": args.description,
            "due": args.due,
            "priority": args.priority,
            "completed": False,
            "created_at": _now_iso(),
        }
        tasks.append(task)
        changed = True
        print(f"Added task {task['id']}.")
    elif args.command == "list-tasks":
        list_tasks(data["tasks"], args.all)
    elif args.command == "complete-task":
        task = find_item(data["tasks"], args.task_id)
        if not task:
            print("Task not found.")
        else:
            task["completed"] = True
            changed = True
            print(f"Completed task {task['id']}.")
    elif args.command == "delete-task":
        task = find_item(data["tasks"], args.task_id)
        if not task:
            print("Task not found.")
        else:
            data["tasks"].remove(task)
            changed = True
            print(f"Deleted task {task['id']}.")
    elif args.command == "add-note":
        notes = data["notes"]
        note = {
            "id": next_id(notes),
            "content": args.content,
            "created_at": _now_iso(),
        }
        notes.append(note)
        changed = True
        print(f"Added note {note['id']}.")
    elif args.command == "list-notes":
        list_notes(data["notes"])
    elif args.command == "delete-note":
        note = find_item(data["notes"], args.note_id)
        if not note:
            print("Note not found.")
        else:
            data["notes"].remove(note)
            changed = True
            print(f"Deleted note {note['id']}.")
    elif args.command == "summary":
        summarize(data)
    else:
        parser.print_help()

    if changed:
        save_data(args.data_file, data)


if __name__ == "__main__":
    main()
