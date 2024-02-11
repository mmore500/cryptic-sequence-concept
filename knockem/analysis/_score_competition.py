import warnings


def score_competition(
    resultNumAlpha: int, resultNumBeta: int, resultUpdatesElapsed: int
) -> float:
    if resultNumAlpha == 0 and resultNumBeta == 0:
        warnings.warn("Alpha and beta both extinct.")
        return 0.0
    if resultUpdatesElapsed == 0:
        warnings.warn("No competition updates elapsed.")
        return 0.0

    fracAlpha = resultNumAlpha / (resultNumAlpha + resultNumBeta)
    fracBeta = resultNumBeta / (resultNumAlpha + resultNumBeta)

    return (fracAlpha - fracBeta) / resultUpdatesElapsed
