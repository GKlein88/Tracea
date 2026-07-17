def format_duration(
    seconds: int,
    style="prime"
):
    """
    Format duration for display.
    """

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60


    if style == "clock":
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    if style == "hms":
        return f"{hours}h{minutes:02d}m{secs:02d}s"
        

    if style == "hms-short":
        return f"{hours}h{minutes:02d}m"


    if style == "prime":
        return f"{hours}h{minutes:02d}'{secs:02d}\""


    if style == "prime-short":
        return f"{hours}h{minutes:02d}"


    return f"{hours:02d}:{minutes:02d}:{secs:02d}"