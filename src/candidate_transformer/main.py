"""
Main pipeline runner.

Runs the candidate transformation pipeline end-to-end.
"""

import argparse
import json
import logging
from pathlib import Path

from candidate_transformer.config.settings import load_config
from candidate_transformer.merge.merger import merge_candidates
from candidate_transformer.parsers.csv_parser import parse_csv
from candidate_transformer.parsers.notes_parser import parse_notes
from candidate_transformer.projection.projector import project_candidates
from candidate_transformer.validation.validator import validate_candidates


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def run_pipeline(
    csv_path: Path,
    notes_path: Path,
    config_path: Path,
    output_path: Path,
) -> None:
    """Run the full candidate transformation pipeline."""
    logger.info("Loading configuration from %s", config_path)
    config = load_config(config_path)

    logger.info("Parsing CSV input from %s", csv_path)
    csv_candidates = parse_csv(csv_path)

    logger.info("Parsing recruiter notes from %s", notes_path)
    notes_candidates = parse_notes(notes_path)

    logger.info("Merging candidate records")
    candidates = merge_candidates(csv_candidates, notes_candidates)

    logger.info("Validating merged candidates")
    validation_results = validate_candidates(candidates)

    logger.info("Projecting candidates using runtime config")
    projected_output = project_candidates(candidates, config)

    final_output = {
        "validation": validation_results,
        "candidates": projected_output,
    }

    logger.info("Writing output to %s", output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(final_output, indent=2),
        encoding="utf-8",
    )

    logger.info("Pipeline completed successfully")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run the candidate data transformation pipeline."
    )

    parser.add_argument("--csv", required=True, help="Path to recruiter CSV file.")
    parser.add_argument("--notes", required=True, help="Path to recruiter notes TXT file.")
    parser.add_argument("--config", required=True, help="Path to output config JSON file.")
    parser.add_argument("--output", required=True, help="Path to write output JSON.")

    args = parser.parse_args()

    run_pipeline(
        csv_path=Path(args.csv),
        notes_path=Path(args.notes),
        config_path=Path(args.config),
        output_path=Path(args.output),
    )


if __name__ == "__main__":
    main()