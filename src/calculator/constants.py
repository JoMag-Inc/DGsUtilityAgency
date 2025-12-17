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

# Use probability mappings
USE_PROBABILITY_VALUES = {
    "low": 0.3,
    "medium": 0.6,
    "high": 0.9,
}

# Time conversion factors
WEEKS_PER_YEAR = 52
MONTHS_PER_YEAR = 12

# Income level weights for utility calculations
# Format: {income_level: {"buy": [useful_weight, not_useful_weight],
#                          "not_buy": [useful_weight, not_useful_weight]}}
INCOME_WEIGHTS = {
    "low": {
        "buy": [2, -8],
        "not_buy": [-1, 0],
    },
    "medium": {
        "buy": [2, -3],
        "not_buy": [-4, 2],
    },
    "high": {
        "buy": [4, -1],
        "not_buy": [-8, 1],
    },
}

# Default income weights (when income level is not specified or unknown)
DEFAULT_INCOME_WEIGHTS = {
    "buy": [1, 1],
    "not_buy": [1, 1],
}

# Default values
DEFAULT_USE_FACTOR_ZERO_PRICE = 0.1  # Use factor when price is 0
DEFAULT_BREAKEVEN_PROBABILITY = 0.5  # Neutral case for breakeven probability
