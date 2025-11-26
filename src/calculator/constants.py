"""
Constants and configuration values for utility calculations.

Modify these values to adjust the behavior of the utility calculator.
"""

# Necessity scoring
NECESSITY_SCORES = {
    "essential": 1.0,
    "nice_to_have": 0.6,
}

# Category multipliers
CATEGORY_MULTIPLIERS = {
    "entertainment": 1.0,
    "efficiency": 1.2,  # Efficiency gains may have higher long-term value
    "qol": 1.1,  # Quality of life improvements
}

# Life area weights
LIFE_AREA_WEIGHTS = {
    "career": 1.3,  # Career impact typically has high long-term value
    "personal": 1.0,  # Baseline
    "health": 1.4,  # Health impacts are often most important
}
