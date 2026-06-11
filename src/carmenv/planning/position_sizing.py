def fixed_fraction_position_size(confidence: float, max_pct: float = 5.0) -> float:
    return round(max(0.0, min(1.0, confidence)) * max_pct, 2)
