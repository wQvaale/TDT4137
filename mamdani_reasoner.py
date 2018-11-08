import matplotlib.pyplot as plt
import numpy as np

# GLOBALS
DISTANCE = 3.7
DELTA = 1.2
CLIP = 1.0


def triangle(pos, x0, x1, x2):
    global CLIP
    value = 0.0
    if (pos >= x0 and pos <= x1):
        value = (pos - x0) / (x1 - x0)
    elif (pos >= x1 and pos <= x2):
        value = (x2 - pos) / (x1 - x0)

    value = CLIP if value > CLIP else value

    return value


def grade(pos, x0, x1):
    global CLIP
    value = 0.0
    if (pos >= x1):
        value = 1.0
    elif (pos <= x0):
        value = 0.0
    else:
        value = (pos - x0) / (x1 - x0)

    value = CLIP if value > CLIP else value

    return value


def reverse_grad(pos, x0, x1):
    global CLIP
    value = 0.0
    if (pos <= x0):
        value = 1.0
    elif (pos >= x1):
        value = 0.0
    else:
        value = (x1 - pos) / (x1 - x0)

    value = CLIP if value > CLIP else value

    return value


def fuzzy_op(case, a, b=0):
    """
    Does fuzzy operations on the fuzzy sets
    :param case: String
    :param a: float
    :param b: float
    :return: float
    """
    return {
        'OR': max(a, b),    # union
        'AND': min(a, b),   # intersection
        'NOT': 1 - a        # complement
    }[case]


def evaluation(distance, delta):
    """
    Evaluates the rules after the sets have been fuzzicated
    :param distance: float
    :param delta: float
    :return: dict[String] = float
    """
    values = dict()

    # Rule 1: IF distance is SMALL AND delta is Growing THEN action is None
    values["None"] = fuzzy_op("AND", distance["Small"], delta["Growing"])

    # Rule 2: IF distance is Small AND delta is Stable THEN action is SlowDown
    values["SlowDown"] = fuzzy_op("AND", distance["Small"], delta["Stable"])

    # Rule 3: IF distance is Perfect AND delta is Growing THEN action is SpeedUp
    values["SpeedUp"] = fuzzy_op("AND", distance["Perfect"], delta["Growing"])

    # Rule 4: IF distance is VeryBig AND (delta is NOT Growing OR delta is NOT GrowingFast) THEN action is FloorIt
    values["FloorIt"] = fuzzy_op("AND", distance["VeryBig"],
                        fuzzy_op("OR",
                        fuzzy_op("NOT", delta["Growing"]), fuzzy_op("NOT", delta["GrowingFast"])))

    # Rule 5: IF distance is VerySmall THEN action BrakeHard
    values["BrakeHard"] = distance["VerySmall"]

    return values


def aggregate(evaluations, actions):
    """
    We take the membershipfunctions of alle rule consequents
    previously clipped and combine them into one signgle fuzzy set
    :param evaluations: dict[String] = float
    :param actions: dict[String] = [float]
    :return: List[String]
    """
    agg = []
    for x in range(actions["start"], actions["end"] + 1):
        value = 0
        for (action, fuzzy_set) in actions["keys"].items():
            if evaluations[action] > 0:
                if fuzzy_set[0] < x < fuzzy_set[3]:
                    value = max(value, evaluations[action])
        agg.append(value)
    return agg


def defuzzycation(agg):
    """
    Final output, as a crisp number
    :param agg: List[float]
    :return: float
    """
    numerator = 0
    denominator = 0
    for i in range(len(agg)):
        numerator += (i - 10) * agg[i]
    return numerator / sum(agg)


def decideAction(cog):
    """
    Returns the action the COG is the center of.
    :param cog: float
    :return: String
    """
    if cog > -10 and cog <= -6:
        return "None"
    elif cog > -6 and cog <= -2:
        return "SlowDown"
    elif cog > -2 and cog <= 2:
        return "None"
    elif cog > 2 and cog <= 6:
        return "SpeedUp"
    elif cog > 6 and cog <= 10:
        return "FloorIt"
    else:
        return "Undefined"


def main():
    # D A T A S E T
    # 1. Fuzzification
    """
    Take crips inputs, and determine the degree to which
    these inputs belong to each of the appropriate fuzzy sets
    """
    global DISTANCE, DELTA
    distance = {
        "start": 0,
        "end": 10,
        "VerySmall": reverse_grad(DISTANCE, 1, 2.5),
        "Small": triangle(DISTANCE, 1.5, 3, 4.5),
        "Perfect": triangle(DISTANCE, 3.5, 5, 6.5),
        "Big": triangle(DISTANCE, 5.5, 7, 8.5),
        "VeryBig": grade(DISTANCE, 7.5, 9)
    }

    delta = {
        "start": -5,
        "end": 5,
        "ShrinkingFast": reverse_grad(DELTA, -4, -2.5),
        "Shrinking": triangle(DELTA, -3.5, -2, -0.5),
        "Stable": triangle(DELTA, -1.5, 0, 1.5),
        "Growing": triangle(DELTA, 0.5, 2, 3.5),
        "GrowingFast": grade(DELTA, 2.5, 4)
    }

    actions = {
        "start": -10,
        "end": 10,
        "keys": {
            "BrakeHard": (-10, -10, -8, -5),
            "SlowDown": (-7, -4, -4, -1),
            "None": (-3, 0, 0, 3),
            "SpeedUp": (1, 4, 4, 7),
            "FloorIt": (5, 8, 10, 10)
        }
    }

    # 2. Rule Evaluation
    """
    Inference: calculate the membership function
    """
    evals = evaluation(distance, delta)

    # 3. Aggregation
    """
    Unify the outputs of all rules
    """
    agg = aggregate(evals, actions)

    # 4. Defuzzification
    """
    Centroid defuzzification method finds a point representing the centre of gravity
    of the aggregated fuzzy set A, on the interval [a, b ]
    """
    cog = defuzzycation(agg)
    act = decideAction(cog)
    print("While COG is: {}, the robot will do the following action:\n{}".format(round(cog, 4), act.upper()))

    """
    # Testing out plotting...
    plt.plot(cog, 0, marker='o', markerSize=3, color="red")     # Plot COG
    plt.plot(agg, 'g'                                           # Plot the aggregated sum
    plt.yticks(range(0,2))                                      # Set range for y-axis
    plt.xlabel('x')                                             # Set label for x-axis
    plt.ylabel('weight')                                        # Set label for y-axis
    plt.grid(True)                                              # Enable grid
    plt.legend(['COG','Aggregated'])                            # Display element mapping to color
    plt.show()                                                  # Show it.
    """


main()
