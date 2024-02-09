import argparse
import logging

from ..common import records as rec


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
