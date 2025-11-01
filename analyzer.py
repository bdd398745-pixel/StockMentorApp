import numpy as np

def fair_value_calc(eps, growth=0.12, years=5, pe_target=22, discount=0.10):
    """Estimate fair value using EPS growth model"""
    if eps is None or eps <= 0:
        return None
    future_eps = eps * ((1 + growth) ** years)
    fair_value = (future_eps * pe_target) / ((1 + discount) ** years)
    return round(fair_value, 2)


def buy_sell_levels(fair_value):
    """Define buy/sell zones around fair value"""
    if not fair_value:
        return None, None
    buy_price = round(fair_value * 0.75, 2)
    sell_price = round(fair_value * 1.25, 2)
    return buy_price, sell_price


def undervaluation_score(current, fair):
    """Score how undervalued a stock is"""
    if not fair or not current:
        return None
    diff = (fair - current) / fair * 100
    return round(diff, 1)
