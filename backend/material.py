import random

def get_live_material_prices():
    """
    Simulated live prices (replace with API later)
    """

    prices = {
        "cement": random.uniform(320, 380),   # per bag
        "steel": random.uniform(55, 75),      # per kg
        "sand": random.uniform(40, 60),       # per cubic ft
        "aggregate": random.uniform(30, 50)
    }

    return prices

def calculate_material_index(prices):
    base_prices = {
        "cement": 350,
        "steel": 60,
        "sand": 50,
        "aggregate": 40
    }

    ratios = []

    for key in prices:
        ratios.append(prices[key] / base_prices[key])

    return sum(ratios) / len(ratios)