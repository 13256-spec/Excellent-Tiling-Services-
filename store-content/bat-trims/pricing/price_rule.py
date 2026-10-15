import math
def retail(cost):
    """inc-GST shelf price from BAT ex-GST cost; mirrors the store's Roberts trim markups"""
    m = 2.2 if cost < 7 else 1.75 if cost < 30 else 1.62 if cost < 100 else 1.5
    if 7 <= cost < 10:  # taper 2.2x -> 1.75x so prices keep rising with cost
        m = 2.2 - 0.15 * (cost - 7)
    p = cost * m
    # keep prices rising with cost across tier boundaries
    if cost >= 100: p = max(p, 161.95)
    elif cost >= 30: p = max(p, 52.95)
    p = math.ceil(p * 20) / 20          # up to 5c
    p = math.floor(p) + 0.95 if p - math.floor(p) > 0.95 or p >= 20 else p   # x.95 endings on $20+
    floor = cost * 1.1 * 1.25
    if p < floor: p = math.ceil(floor * 20) / 20
    return round(p, 2)
