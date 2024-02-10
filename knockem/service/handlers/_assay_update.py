import logging

from .. import assays
from .. import orchestration as orch
from ...common import records as rec


def assay_update() -> int:
    num_updated = 0
    for assayId in orch.iter_pending_assayIds():
        if orch.depends_on_unresolved(assayId):
            logging.info(f"Assay {assayId} depends on unresolved assays.")
            continue
        else:
            num_updated += 1

        document = orch.get_assay_document(assayId)
        try:
            assay_module = getattr(assays, document["assayType"])
        except KeyError:
            raise NotImplementedError(
                f"Assay type {document['assayType']} is not supported.",
            )

        if n := assay_module.dispatch_depended_assays(document):
            logging.info(
                f"{document['assayType']} assay {assayId} "
                f"dispatched {n} depended assays.",
            )
            continue
        elif n := assay_module.dispatch_depended_competitions(document):
            logging.info(
                f"{document['assayType']} assay {assayId} "
                f"dispatched {n} depended competitions.",
            )
            continue
        else:
            result = assay_module.finalize_result(document)
            logging.info(
                f"{document['assayType']} assay {assayId} finalized {result=}.",
            )

    if num_updated > 0:
        logging.info(f"Updated {num_updated} assays.")
    return num_updated
