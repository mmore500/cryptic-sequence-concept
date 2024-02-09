import argparse
import logging

from ._cleanup_genome import cleanup_genome
from ._fetch_genome import fetch_genome
from ._report_competition import report_competition


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="knockem CLI tool")
    subparsers = parser.add_subparsers(help="commands")

    # Subparser for the "cleanup-genome" command
    parser_cleanup_genome = subparsers.add_parser(
        "cleanup-genome", help="Delete a genome from the database if ephemeral"
    )
    parser_cleanup_genome.add_argument(
        "genome_id",
        type=str,
        help="The ID of the genome to delete if ephemeral",
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
