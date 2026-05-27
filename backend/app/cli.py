import argparse
import json
from datetime import timedelta
from typing import Optional

from app.dates import parse_target_date, resolve_target_date
from app.ingestion_service import ingest_habitat_results


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Habitat auction results backend CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Fetch and store Habitat NESO auction results")
    ingest_parser.add_argument("--date", help="Target delivery date in YYYY-MM-DD format")

    range_parser = subparsers.add_parser("ingest-range", help="Backfill Habitat NESO auction results")
    range_parser.add_argument("--start", required=True, help="Start delivery date in YYYY-MM-DD format")
    range_parser.add_argument("--end", required=True, help="End delivery date in YYYY-MM-DD format")
    range_parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue backfill if one date fails",
    )

    args = parser.parse_args(argv)
    if args.command == "ingest":
        target_date = resolve_target_date(args.date)
        run = ingest_habitat_results(target_date)
        print(json.dumps(run, indent=2, sort_keys=True))
        return 0

    if args.command == "ingest-range":
        start_date = parse_target_date(args.start)
        end_date = parse_target_date(args.end)
        if end_date < start_date:
            parser.error("--end must be on or after --start")

        runs = []
        target_date = start_date
        while target_date <= end_date:
            try:
                runs.append(ingest_habitat_results(target_date))
            except Exception as exc:
                if not args.continue_on_error:
                    raise
                runs.append(
                    {
                        "target_date": target_date.isoformat(),
                        "status": "failed",
                        "error_message": str(exc),
                    }
                )
            target_date += timedelta(days=1)

        print(json.dumps(runs, indent=2, sort_keys=True))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
