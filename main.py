"""
Genomic Literature Mining Agent
--------------------------------
Usage:
    python main.py --query "BRCA1 breast cancer"
    python main.py --gene TP53 --disease "lung cancer"
"""

import argparse
from agent.loop import run
from outputs.formatter import print_output
import asyncio


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Autonomous literature mining agent for genomics research.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", "-q", type=str, help="Free-text query")
    group.add_argument("--gene", type=str, help="Gene symbol e.g. BRCA1")

    parser.add_argument("--disease", type=str, default="", help="Disease context")
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.query:
        query = args.query
    else:
        parts = [args.gene]
        if args.disease:
            parts.append(args.disease)
        query = " ".join(parts)

    print(f"\nRunning agent for: {query}\n")
    output = asyncio.run(run(query))
    print_output(output)


if __name__ == "__main__":
    main()