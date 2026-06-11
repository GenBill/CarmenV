from statistics import fmean, pstdev

from carmenv.agents.schema import ConsensusSummary, PersonaOpinion


def mean_score(opinions: list[PersonaOpinion]) -> float:
    if not opinions:
        return 0.0
    return round(float(fmean(opinion.score for opinion in opinions)), 4)


def score_std(opinions: list[PersonaOpinion]) -> float:
    if len(opinions) < 2:
        return 0.0
    return round(float(pstdev(opinion.score for opinion in opinions)), 4)


def bullish_count(opinions: list[PersonaOpinion]) -> int:
    return sum(opinion.stance == "bullish" for opinion in opinions)


def neutral_count(opinions: list[PersonaOpinion]) -> int:
    return sum(opinion.stance == "neutral" for opinion in opinions)


def bearish_count(opinions: list[PersonaOpinion]) -> int:
    return sum(opinion.stance == "bearish" for opinion in opinions)


def consensus_score(opinions: list[PersonaOpinion]) -> float:
    """Return a 0-100 agreement-adjusted long-attractiveness score."""
    if not opinions:
        return 0.0
    disagreement = disagreement_score(opinions)
    return round(max(0.0, min(100.0, mean_score(opinions) * (1 - disagreement / 200))), 4)


def disagreement_score(opinions: list[PersonaOpinion]) -> float:
    """Return a 0-100 measure of persona dispersion and stance conflict."""
    if not opinions:
        return 0.0
    std_component = min(score_std(opinions) * 2, 70.0)
    stance_kinds = len({opinion.stance for opinion in opinions})
    stance_component = {1: 0.0, 2: 15.0, 3: 30.0}[stance_kinds]
    return round(min(100.0, std_component + stance_component), 4)


def summarize_consensus(opinions: list[PersonaOpinion]) -> ConsensusSummary:
    return ConsensusSummary(
        mean_score=mean_score(opinions),
        score_std=score_std(opinions),
        bullish_count=bullish_count(opinions),
        neutral_count=neutral_count(opinions),
        bearish_count=bearish_count(opinions),
        consensus_score=consensus_score(opinions),
        disagreement_score=disagreement_score(opinions),
    )
