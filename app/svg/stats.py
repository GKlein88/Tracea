from .fonts import (
    get_font_path,
    measure_text_width
)


def draw_stats(dwg, config, template):
    """
    Draw poster statistics with separate value and unit tspans for JS manipulation.
    """
    positions = [
        template.stats.positions3.left,
        template.stats.positions3.center,
        template.stats.positions3.right
    ]
    anchors = [
        template.stats.text_anchors3.left,
        template.stats.text_anchors3.center,
        template.stats.text_anchors3.right
    ]

    # Utilisation des nouveaux noms de champs : distance_text, elevation_text, duration_text
    stat_data = [
        {"id": "stat-distance", "val": config.distance_text, "show": config.show_distance},        
        {"id": "stat-elevation", "val": config.elevation_text, "show": config.show_elevation},        
        {"id": "stat-duration", "val": config.duration_text, "show": config.show_duration},
    ]
    
    for index, stat in enumerate(stat_data):
        group = dwg.g(id=stat["id"], display="inline" if stat["show"] else "none")
        
        txt = dwg.text(
            "", # Start with empty text to hold nested tspans
            insert=(positions[index], template.stats.y),
            dominant_baseline="hanging",
            font_family=template.stats.font_family,
            font_size=template.stats.font_size,
            font_weight=template.stats.font_weight,
            fill=template.stats.color,
            text_anchor=anchors[index]
        )
        
        # Check if the statistic string contains an editable unit (KM or M)
        raw_val = stat["val"]
        unit = ""
        if "KM" in raw_val:
            raw_val = raw_val.replace("KM", "").strip()
            unit = " KM"
        elif "M" in raw_val and not any(char in raw_val for char in ["'", '"', "h", "m", "s"]): # Avoid matching duration symbols
            raw_val = raw_val.replace("M", "").strip()
            unit = " M"
            
        if unit:
            # Add dynamic editable value tspan
            txt.add(dwg.tspan(raw_val, class_="stat-value"))
            # Add static locked unit tspan
            txt.add(dwg.tspan(unit, class_="stat-unit"))
        else:
            # Duration or statistics without separate unit labels
            txt.add(dwg.tspan(stat["val"], class_="stat-value"))
            
        group.add(txt)
        dwg.add(group)