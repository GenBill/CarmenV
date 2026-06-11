# Attribution Design

CarmenV saves research artifacts so every recommendation can be evaluated later.

## Required persisted artifacts

- `daily candidates`: the full candidate set, not only the final top 5/top 10, so rejected ideas can be evaluated.
- `agent scores`: structured score components make it possible to test whether trend, liquidity, narrative, risk, or fundamentals predicted returns.
- `trade plans`: the intended entry, stop, targets, invalidation, holding period, and sizing define the decision before outcomes are known.
- `actual trades`: manual execution records show whether human discretion improved or degraded model output.
- `forward returns`: objective 1/3/5/10/20 day labels allow calibration without relying on memory.
- `manual reviews`: tags and comments capture qualitative lessons that can become future structured features.

## First statistics

The baseline supports score-bucket, pattern-type, and horizon summaries with count, mean return, median return, win rate, and average max drawdown.

## Persona consensus as cognitive attribution

Future multi-style agents should be evaluated as a `persona council`, not as a direct return predictor. Persona consensus is a structured measurement of market cognition and disagreement: it records whether different investor styles can explain the same ticker with the same or conflicting thesis.

When multiple personas agree, the ticker can be explained by more than one market aesthetic. That may create higher consensus diffusion potential because technical traders, industry researchers, value investors, and risk-aware allocators can all find a reason to pay attention.

When multiple personas disagree, the ticker sits in a cognitive-disagreement zone. That can mean a larger expectation gap and a better opportunity for differentiated research, but it also means larger thesis risk. CarmenV should persist both the consensus score and the disagreement score so later attribution can test whether agreement or disagreement was more useful in each market regime.
