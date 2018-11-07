DISTANCE = 3.7
DELTA = 1.2
CLIP = 1.0

def triangle(pos, x0, x1, x2):
    """

    :param pos:
    :param x0:
    :param x1:
    :param x2:
    :return:
    """
    global CLIP
    value = 0.0
    if (pos >= x0 and pos <= x1):
        value = (pos - x0) / (x1 - x0)
    elif (pos >= x1 and pos <= x2):
        value = (x2 - pos) / (x1 - x0)

    value = CLIP if value > CLIP else value
    return value

def grade(pos, x0, x1):
    """

    :param pos:
    :param x0:
    :param x1:
    :return:
    """
    global CLIP
    value = 0.0
    if (pos >= x1):
        value = (pos - x0) / (x1 - x0)
    elif (pos <= x0):
        value = value

    value = CLIP if value > CLIP else value
    return value

def reverse_grad(pos, x0, x1):
    """

    :param pos:
    :param x0:
    :param x1:
    :return:
    """
    global CLIP
    value = 0.0
    if (pos >= x0):
        value = 1.0
    elif (pos >= x1):
        value = value
    else:
        value = (x1 - pos) / (x1 - x0)

    value = CLIP if value > CLIP else value
    return value

def fuzzy_op(case, a, b):
   return {
       'OR': max(a, b),     #  union
       'AND': min(a, b),    # intersection
       'NOT': 1 - a         # complement
   }[case]


def evaluation():
    """

    :return:
    """
    values = {}

    # Rule 1: IF distance is SMALL AND delta is Growing THEN action is None
    rule1 = fuzzy_op("AND",distance["Small"], delta["Growing"])
    values[rule1] = "None"

    # Rule 2: IF distance is Small AND delta is Stable THEN action is SlowDown
    rule2 = fuzzy_op("AND",distance["Small"], delta["Stable"])
    values[rule2] = "SlowDown"

    # Rule 3: IF distance is Perfect AND delta is Growing THEN action is SpeedUp
    rule3 = fuzzy_op("AND",distance["Perfect"], delta["Growing"])
    values[rule3] = "SpeedUp"

    # Rule 4: IF distance is VeryBig AND (delta is NOT Growing OR delta is NOT GrowingFast) THEN action is FloorIt
    rule4 = fuzzy_op("AND", distance["VeryBig"], fuzzy_op("AND",
                                                 fuzzy_op("OR",
                                                 fuzzy_op("NOT", delta["Growing"]), fuzzy_op("NOT", delta["GrowingFast"]))))
    values[rule4] = "FloorIt"

    # Rule 5: IF distance is VerySmall THEN action BrakeHard
    rule5 = distance["Small"]
    values[rule5] = "BrakeHard"


def aggregate(evaluations):
    agg = 0
    for rule, action in evaluations:
        
            



# D A T A S E T
# data = dict(zip(list_with_keys, list_with_values))
distance = {
    "start": 0,
    "end": 10,
    "VerySmall": reverse_grad(DISTANCE, 0.0, 2.5),
    "Small": triangle(DISTANCE, 1.5, 3, 4.5),
    "Perfect": triangle(DISTANCE, 3.5, 5, 6.5),
    "Big": triangle(DISTANCE, 5.5, 7, 8.5),
    "VeryBig": grade(DISTANCE, 7.5, 9)
}

delta = {
    "start": -5,
    "end": 5,
    "ShrinkingFast": reverse_grad(DELTA, -4, -2.5),
    "Shrining": triangle(DELTA, -3.5, -2, -0.5),
    "Stable": triangle(DELTA, -1.5, 0, 1.5),
    "Growing": triangle(DELTA, 0.5, 2, 3.5),
    "GrowingFast": grade(DELTA, 2.5, 4)
}

action = {
    "start": -10,
    "end": 10,
    "BrakeHard": (-10, -10, -8, -5),
    "SlowDown": (-7, -4, -4, -1),
    "None": (-3, 0, 0, 3),
    "SpeedUp": (1, 4, 4, 7),
    "FloorIt": (5, 8, 10, 10)
}
