import numpy as np
from typing import List


def calculate_discard_percentage(Qdi: np.ndarray, threshold: int = 50) -> float:
    """
    Helper function of the Mean-Discard-Gap (MDG) for calculating the discard ratio of input values for a given threshold
    """
    if not isinstance(Qdi, np.ndarray):
        raise TypeError(
            f"Expected input to be of type np.ndarray, but got {type(Qdi).__name__}."
        )

    discard_ratio = (Qdi < threshold).sum() / len(Qdi)
    return discard_ratio


def calculate_min_max_distance(discard_percentage_list: List[float]) -> float:
    """
    Helper function of the Mean-Discard-Gap (MDG) for calculating the min-max distance for a given threshold
    """
    if not isinstance(discard_percentage_list, List):
        raise TypeError(
            f"Expected input to be of type List, but got {type(discard_percentage_list).__name__}."
        )
    return max(discard_percentage_list) - min(discard_percentage_list)


def enforce_integer_quality_scores(QD: np.ndarray):
    """
    Helper function of the Mean-Discard-Gap (MDG) for type enforcing integer quality scores
    """
    # Check if any quality score is not of dtype int
    if not np.issubdtype(QD.dtype, np.integer):
        raise TypeError(
            f"The MDG Implementation expects quality scores to be of type int, but got one or more quality scores of type {type(QD.dtype).__name__}."
        )
