import argparse
import json
from typing import Optional

from app.dates import resolve_target_date
from app.ingestion_service import ingest_habitat_results


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Habitat auction results backend CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Fetch and store Habitat NESO auction results")
    ingest_parser.add_argument("--date", help="Target delivery date in YYYY-MM-DD format")

    args = parser.parse_args(argv)
    if args.command == "ingest":
        target_date = resolve_target_date(args.date)
        run = ingest_habitat_results(target_date)
        print(json.dumps(run, indent=2, sort_keys=True))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
