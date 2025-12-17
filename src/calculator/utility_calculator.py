"""
Utility calculator for analyzing purchase decisions.

This module processes form data from the DGs Utility Agency application
and calculates various utility metrics to help users make informed purchase decisions.
"""

from typing import TypedDict

from .constants import (
    CATEGORY_MULTIPLIERS,
    DEFAULT_BREAKEVEN_PROBABILITY,
    DEFAULT_INCOME_WEIGHTS,
    DEFAULT_USE_FACTOR_ZERO_PRICE,
    INCOME_WEIGHTS,
    LIFE_AREA_WEIGHTS,
    MONTHS_PER_YEAR,
    NECESSITY_SCORES,
    USE_PROBABILITY_VALUES,
    WEEKS_PER_YEAR,
)


class PurchaseData(TypedDict):
    """Type definition for the purchase form data input."""

    item_name: str
    price: float
    income_level: str  # "low", "medium", or "high"
    life_areas: list[str]  # e.g., ["career", "personal", "health"]
    necessity: str  # "essential" or "nice_to_have"
    time_use: float  # hours per week
    use_probability: str
    life_span: int  # in months
    category: str  # "entertainment", "efficiency", or "qol"


class UtilityMetrics(TypedDict):
    """Type definition for calculated utility metrics output."""

    use_factor: float
    u_buy_useful: float  # Utility: Buy and it's useful
    u_buy_not_useful: float  # Utility: Buy but it's not useful
    u_not_buy_useful: float  # Utility: Don't buy but would be useful
    u_not_buy_not_useful: float  # Utility: Don't buy and not useful


def calculate_utilities(purchase_data: PurchaseData) -> UtilityMetrics:
    price = purchase_data["price"]
    income_level = purchase_data["income_level"]
    life_areas = purchase_data["life_areas"]
    necessity = purchase_data["necessity"]
    time_use = purchase_data["time_use"]
    use_probability = purchase_data["use_probability"]
    life_span = purchase_data["life_span"]
    category = purchase_data["category"]

    # probability determination
    prob = USE_PROBABILITY_VALUES.get(use_probability, 1)

    # time calculations
    time_use_year = time_use * WEEKS_PER_YEAR
    life_span_years = life_span / MONTHS_PER_YEAR
    total_time_use = time_use_year * life_span_years * prob

    # Calculate quality multipliers from constants
    category_mult = CATEGORY_MULTIPLIERS.get(category, 1.0)
    necessity_mult = NECESSITY_SCORES.get(necessity, 0.8)

    # Average life area weights if multiple areas are affected
    life_area_mult = 1.0
    if life_areas:
        life_area_mult = sum(
            LIFE_AREA_WEIGHTS.get(area, 1.0) for area in life_areas
        ) / len(life_areas)

    # Calculate benefit with quality multipliers
    benefit = total_time_use * category_mult * necessity_mult * life_area_mult

    income_weights = INCOME_WEIGHTS.get(income_level, DEFAULT_INCOME_WEIGHTS)
    # Calculate use_factor (hours per dollar spent)
    use_factor = (
        total_time_use / price if price > 0 else DEFAULT_USE_FACTOR_ZERO_PRICE
    )

    benefit_factor = benefit / price

    # Calculate utilities for each scenario
    U_buy_useful = benefit_factor * income_weights["buy"][0]
    U_buy_not_useful = benefit_factor * income_weights["buy"][1]
    U_not_buy_useful = benefit_factor * income_weights["not_buy"][0]
    U_not_buy_not_useful = benefit_factor * income_weights["not_buy"][1]

    return {
        "use_factor": use_factor,
        "u_buy_useful": U_buy_useful,
        "u_buy_not_useful": U_buy_not_useful,
        "u_not_buy_useful": U_not_buy_useful,
        "u_not_buy_not_useful": U_not_buy_not_useful,
    }


def calculate_expected_utility_buy(
    p_useful_if_buy: float, results: UtilityMetrics
) -> float:
    return (
        p_useful_if_buy * results["u_buy_useful"]
        + (1 - p_useful_if_buy) * results["u_buy_not_useful"]
    )


def calculate_expected_utility_not_buy(
    p_useful_if_not_buy: float, results: UtilityMetrics
) -> float:

    return (
        p_useful_if_not_buy * results["u_not_buy_useful"]
        + (1 - p_useful_if_not_buy) * results["u_not_buy_not_useful"]
    )


def calculate_breakeven_probability(
    results: UtilityMetrics, p_useful_if_not_buy: float
) -> float:
    eu_not_buy = calculate_expected_utility_not_buy(p_useful_if_not_buy, results)

    numerator = eu_not_buy - results["u_buy_not_useful"]
    denominator = results["u_buy_useful"] - results["u_buy_not_useful"]

    if denominator == 0:
        return DEFAULT_BREAKEVEN_PROBABILITY  # Neutral case

    breakeven = numerator / denominator
    return max(0.0, min(1.0, breakeven))  # Clamp to [0, 1]
