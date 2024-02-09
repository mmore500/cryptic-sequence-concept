import argparse
import logging
import os

from ..common import records as rec


def report_competition(args: argparse.Namespace) -> None:
    updates_elapsed = args.updates_elapsed
    num_alpha = args.num_alpha
    num_beta = args.num_beta

    # Implement the logic to check if the result is already in the database
    # If not, upload the result
    logging.info(
        "Reporting competition results: "
        f"Updates Elapsed={updates_elapsed}, "
        f"Num Alpha={num_alpha}, "
        f"Num Beta={num_beta}"
    )
    rec.add_competition_result(
        assayId=os.environ["KNOCKEM_ASSAY_ID"],
        competitionId=os.environ["KNOCKEM_COMPETITION_ID"],
        numKnockoutSites=os.environ["KNOCKEM_NUM_KNOCKOUT_SITES"],
        resultUpdatesElapsed=updates_elapsed,
        resultNumAlpha=num_alpha,
        resultNumBeta=num_beta,
        submissionId=os.environ["KNOCKEM_SUBMISSION_ID"],
        userEmail=os.environ["KNOCKEM_USER_EMAIL"],
    )

    # Example: Insert competition results into the database
    # Success/failure handling
    logging.info("Competition results reported successfully.")
