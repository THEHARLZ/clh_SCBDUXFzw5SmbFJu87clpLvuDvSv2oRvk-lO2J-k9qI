# clh_SCBDUXFzw5SmbFJu87clpLvuDvSv2oRvk-lO2J-k9qI

MARTY is a lightweight personal assistant CLI for keeping tasks and notes on track.

## Quick start

```bash
python3 assistant.py summary
python3 assistant.py add-task "Book the dentist" --due 2026-03-01 --priority high
python3 assistant.py add-note "Pick up coffee beans on Friday"
python3 assistant.py list-tasks
python3 assistant.py list-notes
```

### Helpful commands

- `summary` shows a quick daily overview (default).
- `add-task` and `list-tasks` manage tasks, with optional due dates.
- `complete-task` or `delete-task` keeps your list tidy.
- `add-note` and `list-notes` save quick notes.

By default, data is stored in `~/.personal_assistant.json`. Use `--data-file` to point to a custom path.
