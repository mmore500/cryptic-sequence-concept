import argparse
import logging
import os

from .common import records as rec

logging.basicConfig(level=logging.INFO)


def cleanup_genome(args: argparse.Namespace) -> None:
    genome_id = args.genome_id
    logging.info(f"Deleting genome with ID: {genome_id}")
    document = rec.get_genome_document(genome_id)
    if document is None:
        logging.error(f"Genome {genome_id} not found.")
    elif document["isEphemeral"]:
        rec.delete_genome_document(genome_id)
        logging.info(f"Genome {genome_id} deleted successfully.")
    else:
        logging.info(f"Genome {genome_id} is not ephemeral.")


def fetch_genome(args: argparse.Namespace) -> None:
    genome_id = args.genome_id
    # Implement the logic to fetch the genome from the database
    logging.info(f"Fetching genome with ID: {genome_id}")
    document = rec.get_genome_document(genome_id)
    if document is None:
        logging.error(f"Genome {genome_id} not found.")
        return
    print(document["genomeContent"])
    # Success/failure handling
    logging.info(f"Genome {genome_id} fetched successfully.")


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


def main() -> None:
    parser = argparse.ArgumentParser(description="knockem CLI tool")
    subparsers = parser.add_subparsers(help="commands")

    # Subparser for the "cleanup-genome" command
    parser_cleanup_genome = subparsers.add_parser(
        "cleanup-genome", help="Delete a genome from the database if ephemeral"
    )
    parser_cleanup_genome.add_argument(
        "genome_id", type=str, help="The ID of the genome to maybe delete"
    )
    parser_cleanup_genome.set_defaults(func=cleanup_genome)

    # Subparser for the "fetch-genome" command
    parser_fetch_genome = subparsers.add_parser(
        "fetch-genome", help="Fetch a genome from the database to stdout"
    )
    parser_fetch_genome.add_argument(
        "genome_id", type=str, help="The ID of the genome to fetch"
    )
    parser_fetch_genome.set_defaults(func=fetch_genome)

    # Subparser for the "report-competition" command
    parser_report_competition = subparsers.add_parser(
        "report-competition", help="Upload competition results to database"
    )
    parser_report_competition.add_argument(
        "updates_elapsed", type=int, help="Elapsed updates"
    )
    parser_report_competition.add_argument(
        "num_alpha", type=int, help="Number of alpha genomes"
    )
    parser_report_competition.add_argument(
        "num_beta", type=int, help="Number of beta genomes"
    )
    parser_report_competition.set_defaults(func=report_competition)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
