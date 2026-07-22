def format_duration(
    seconds: int = 0,
    hours: int = None,
    minutes: int = None,
    secs: int = None,
    style: str = "clock"
) -> str:
    """
    Format duration for display based on total seconds or separate h, m, s components.
    """
    if hours is None or minutes is None or secs is None:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

    if style == "clock":
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    if style == "hms":
        return f"{hours}h{minutes:02d}m{secs:02d}s"

    if style == "prime":
        return f"{hours}h{minutes:02d}'{secs:02d}\""

    if style == "short":
        return f"{hours}h{minutes:02d}"

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"