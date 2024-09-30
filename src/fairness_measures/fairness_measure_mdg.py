import numpy as np
from typing import List
from utils.mdg_utils import *


def mean_discard_gap(QD: List[np.ndarray]) -> float:
    """
    Calculates the proposed Mean-Discard-Gap (MDG) Score for a set of demographic groups.

    Note:
    -----
    This particular MDG implementation is not generalizable and does consequently not work with floating point quality scores.
    To follow a “higher is better” semantic the MDG-SQFR has to be calculated as follows: 1 - MDG
    Parameters:
    ----------
    QD : List[np.ndarray]
        A list of np.ndarrays containing quality score distributions for demographic groups to be evaluated.

    Returns:
    -------
    float
        The Mean-Discard-Gap (MDG) Score.

    Example:
    -------
    group_a = np.array([76, 76, 77, 77, 78, 79, 80, 82, 82, 84])

    group_b = np.array([84, 84, 84, 84, 85, 85, 87, 87, 88, 88])

    group_c = np.array([82, 82, 82, 84, 84, 86, 87, 87, 88, 88])

    groups = [group_a, group_b, group_c]

    >>> MGD_SQFR = 1 - mean_discard_gap(groups)
    0.44999999999999996
    """
    all_quality_scores = np.concatenate(QD)
    # Ensure Quality Scores are of type int
    enforce_integer_quality_scores(all_quality_scores)
    min_threshold, max_threshold = np.min(all_quality_scores), np.max(
        all_quality_scores
    )

    min_max_distances = []

    for threshold in range(min_threshold + 1, max_threshold + 1):
        discard_percentages = [
            calculate_discard_percentage(Qdi, threshold=threshold) for Qdi in QD
        ]
        min_max_distance = calculate_min_max_distance(discard_percentages)
        min_max_distances.append(min_max_distance)

    mdg = np.mean(min_max_distances)
    return mdg
