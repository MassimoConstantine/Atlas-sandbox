"""CLI entry point for the Atlas Ledger reader tool."""

import argparse
from datetime import datetime
from pathlib import Path

from src.ledger_models import LedgerEvent
from src.ledger_reader import filter_events, parse_ledger_file


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for the ledger CLI."""
    parser = argparse.ArgumentParser(
        description="Read and filter Atlas Ledger event files.",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to a JSONL ledger file",
    )
    parser.add_argument(
        "--event-type",
        type=str,
        default=None,
        help="Filter by event type",
    )
    parser.add_argument(
        "--from",
        type=str,
        default=None,
        dest="from_date",
        help="Filter events from this date (ISO 8601)",
    )
    parser.add_argument(
        "--to",
        type=str,
        default=None,
        dest="to_date",
        help="Filter events up to this date (ISO 8601)",
    )
    parser.add_argument(
        "--task-id",
        type=str,
        default=None,
        help="Filter by task ID",
    )
    return parser


def format_table(events: list[LedgerEvent]) -> str:
    """Format a list of ledger events as a human-readable table."""
    if not events:
        return "No matching events found."

    headers = ["timestamp", "event_type", "task_id", "description"]
    rows: list[list[str]] = []
    for e in events:
        rows.append([
            e.timestamp.isoformat(),
            e.event_type,
            e.task_id,
            e.description,
        ])

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    def fmt_row(cells: list[str]) -> str:
        return "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(cells))

    lines = [fmt_row(headers), "  ".join("-" * w for w in col_widths)]
    for row in rows:
        lines.append(fmt_row(row))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    """Run the ledger CLI with the given arguments."""
    parser = build_parser()
    args = parser.parse_args(argv)

    from_dt: datetime | None = None
    to_dt: datetime | None = None
    if args.from_date is not None:
        from_dt = datetime.fromisoformat(args.from_date)
    if args.to_date is not None:
        to_dt = datetime.fromisoformat(args.to_date)

    events = parse_ledger_file(args.file)
    filtered = filter_events(
        events,
        event_type=args.event_type,
        from_date=from_dt,
        to_date=to_dt,
        task_id=args.task_id,
    )
    print(format_table(filtered))


if __name__ == "__main__":
    main()
