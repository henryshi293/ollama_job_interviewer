"""Command-line helper: quick demo of the *mypackage* workflow."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .api import OllamaAPI
from .job_description import generate_job_description
from .ranking import rank_applicants

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mypackage",
        description="Generate a JD + rank applicants via Ollama",
    )
    parser.add_argument(
        "job_title",
        help="One-line job title, e.g. 'Software Engineer'",
    )
    parser.add_argument(
        "resumes",
        nargs="+",
        type=Path,
        help="One or more PDF résumé files",
    )
    parser.add_argument(
        "--model",
        default="gemma3:latest",
        help="Ollama model name (default: %(default)s)",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:11434",
        help="Ollama base URL (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:  # pragma: no cover
    args = _parse_args()
    api = OllamaAPI(base_url=args.base_url, model_name=args.model)

    logging.info("Generating job description …")
    jd = generate_job_description(args.job_title, api=api)
    print("# Job Description\n")
    print(jd)
    print("\n" + "=" * 80 + "\n")

    logging.info("Ranking applicants …")
    ranking = rank_applicants(jd, args.resumes, api=api)
    print("# Applicant Ranking\n")
    print(ranking)


if __name__ == "__main__":  # Allows “python path/to/cli.py …” as well
    main()
