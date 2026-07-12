def evaluate_understanding(similarity, filler_ratio, audio):
    """Combine similarity, filler usage, and audio confidence into a score.
    Returns (score:int, level:str, color:str)
    """
    score = 0
    score += 50 if similarity > 0.7 else 30 if similarity > 0.4 else 10
    score += 20 if filler_ratio < 0.05 else 10
    score += 15 if audio.get("pause_ratio", 1.0) < 0.25 else 5
    score += 15 if audio.get("rms_energy", 0.0) > 0.01 else 5

    if score >= 80:
        return score, "Strong Understanding", "#2ecc71"
    elif score >= 50:
        return score, "Moderate Understanding", "#f39c12"
    else:
        return score, "Poor Understanding", "#e74c3c"
