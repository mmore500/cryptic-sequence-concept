import argparse
import logging

from ..common import records as rec


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
