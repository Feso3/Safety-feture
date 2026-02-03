import argparse
from pathlib import Path
from typing import Optional

from hidprompt.pipeline import run_scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hidprompt", description="Hidden prompt detector")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a file for prompt-injection signals")
    scan_parser.add_argument("path", type=Path, help="Path to .txt, .md, or .html file")
    scan_parser.add_argument(
        "--format",
        choices=["json", "md", "both"],
        default="both",
        help="Output format (default: both)",
    )
    scan_parser.add_argument("--out", type=Path, default=Path("."), help="Output directory")
    scan_parser.add_argument("--quiet", action="store_true", help="Suppress stdout output")
    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        report = run_scan(args.path, args.out, args.format)
        if not args.quiet:
            print(f"Scan complete. Risk score: {report['risk_score']} ({report['risk_level']})")
            print(f"Reports written to: {args.out.resolve()}")
        return 0

    parser.error("Unknown command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
