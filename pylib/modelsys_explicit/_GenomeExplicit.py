import typing

import numpy as np


class GenomeExplicit:
    _assay_artifact_functors: typing.List[typing.Callable]
    _knockout_effect_functors: typing.List[typing.Callable]

    def __init__(
        self: "GenomeExplicit",
        knockout_effects: typing.Sequence[typing.Callable],
        assay_artifacts: typing.Sequence[typing.Callable] = tuple(),
    ) -> None:
        self._knockout_effect_functors = [*knockout_effects]
        self._assay_artifact_functors = [*assay_artifacts]

    def test_knockout(self: "GenomeExplicit", knockout: np.array) -> bool:
        result = sum(
            effect(knockout) for effect in self._knockout_effect_functors
        )
        for artifact in self._assay_artifact_functors:
            result = artifact(result)
        return result >= 1.0
