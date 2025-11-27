"""
Utility calculator for analyzing purchase decisions.

This module processes form data from the DGs Utility Agency application
and calculates various utility metrics to help users make informed purchase decisions.
"""

from typing import TypedDict

from .constants import CATEGORY_MULTIPLIERS, LIFE_AREA_WEIGHTS, NECESSITY_SCORES


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
    prob = 1
    if use_probability == "low":
        prob = 0.3
    elif use_probability == "medium":
        prob = 0.6
    elif use_probability == "high":
        prob = 0.9

    # time calculations
    time_use_year = time_use * 52
    life_span_years = life_span / 12
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

    income_weights = {"buy": [1, 1], "not_buy": [1, 1]}
    if income_level == "low":
        income_weights["buy"] = [2, -8]
        income_weights["not_buy"] = [-1, 0]
    elif income_level == "medium":
        income_weights["buy"] = [2, -3]
        income_weights["not_buy"] = [-4, 2]
    elif income_level == "high":
        income_weights["buy"] = [4, -1]
        income_weights["not_buy"] = [-8, 1]
    # Calculate use_factor (hours per dollar spent)
    use_factor = total_time_use / price if price > 0 else 0

    # Calculate utilities for each scenario
    U_buy_useful = benefit * income_weights["buy"][0] - price
    U_buy_not_useful = -price * abs(income_weights["buy"][1])
    U_not_buy_useful = benefit * income_weights["not_buy"][0]
    U_not_buy_not_useful = price * income_weights["not_buy"][1] * 0.1

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
        return 0.5  # Neutral case

    breakeven = numerator / denominator
    return max(0.0, min(1.0, breakeven))  # Clamp to [0, 1]
