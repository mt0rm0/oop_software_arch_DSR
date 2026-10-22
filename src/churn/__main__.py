"""Command line entry point.

    uv run python -m churn --config configs/baseline.json --save models/churn.joblib
    uv run churn-train --config configs/random_forest.json

This is the only place that configures logging: libraries emit log records,
applications decide where they go.
"""

from __future__ import annotations

import argparse
import logging
import sys

from churn.config import ExperimentConfig
from churn.errors import ChurnError
from churn.experiment import run_experiment

logger = logging.getLogger("churn")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Train and evaluate the churn model.")
    parser.add_argument("--config", help="JSON experiment config (defaults are used if omitted)")
    parser.add_argument("--save", help="Where to store the fitted model, e.g. models/churn.joblib")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show debug messages")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    )

    try:
        config = ExperimentConfig.from_json(args.config) if args.config else ExperimentConfig()
        model, result = run_experiment(config)
        if args.save:
            model.save(args.save)
    except ChurnError:
        # Expected problems (bad config, bad data): one clear message, no traceback noise
        logger.exception("Run failed")
        return 1

    print(result.summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
