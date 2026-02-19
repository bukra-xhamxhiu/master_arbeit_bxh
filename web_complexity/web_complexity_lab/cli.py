# web_complexity_lab/cli.py
import argparse
from .config import load_config
from .pipeline import run_evaluation


def main():
    parser = argparse.ArgumentParser(
        prog="wcx",
        description="Web Complexity Lab – UI complexity evaluation from tests & logs",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    eval_parser = subparsers.add_parser("evaluate", help="Run complexity evaluation")
    eval_parser.add_argument("--config", required=True, help="Path to config.yaml")

    info_parser = subparsers.add_parser("info", help="Show tool info")

    args = parser.parse_args()

    if args.command == "info":
        print("Web Complexity Lab – Python engine for UI complexity evaluation.")
        return

    if args.command == "evaluate":
        cfg = load_config(args.config)
        run_evaluation(cfg)


if __name__ == "__main__":
    main()
