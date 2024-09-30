import numpy as np
from typing import List, Union


def low_weighted_mean_score(
    Qdi: Union[List[Union[float, int]], np.ndarray],
    QD: Union[List[Union[float, int]], np.ndarray],
) -> float:
    """
    Calculates the Low-Weighted-Mean (LWM) Score for a given Quality Score Distribution Qdi.

    Note:
    -----
    The obtained LWM scores for the set of demographic groups to be evaluated can be used as an alternative input for the Gini coefficient.
    The following is assuming quality scores as integers in [0, 100], i.e. 101 possible values, which means the relevant thresholds are integers in [0, 100), i.e. 100 possible values.
    If your underlying quality score range is different, you need to change the value of the variables QS_UPPER_LIMIT and N_POSSIBLE_SCORES respectively.

    Parameters:
    ----------
    Qdi : List[float], List[int] or array-like
        A quality score distribution Q for a single demographic group di

    QD : List[float], List[int] or array-like
        A list or array of all quality scores Q across the union set D of demographic groups to be evaluated.
    Returns:
    -------
    float
        The Low-Weighted-Mean (LWM) Score for a single demographic group.

    Example:
    -------
    Qd1, Qd2 = [1,2,3], [4,5,6]
    QD = np.concatenate([Qd1,Qd2])

    >>> LWM_D1 = low_weighted_mean_score([Qd1, QD])
    1.8333333333333335

    >>> LWM_D2 = low_weighted_mean_score([Qd2, QD])
    4.333333333333333

    >>> LWM_GC_SQFR = 1 - gini_coefficient([LWM_D1, LWM_D2])
    0.5945945945945946
    """
    QS_UPPER_LIMIT = 100  # Adjust if required
    N_POSSIBLE_SCORES = QS_UPPER_LIMIT + 1  # Adjust if required

    # Initialization of the quality score weight embedding
    score_embedding = np.zeros(N_POSSIBLE_SCORES, dtype=np.float64)
    # The overall min and max quality score for normalization
    min_qs, max_qs = min(QD), max(QD)

    # Calculate the weight sums for the quality_score instances in the quality_scores distribution:
    for quality_score in Qdi:
        weight = 1 - (
            (quality_score - min_qs) / (max_qs - min_qs)
        )  # Inverted min-max normalization for the possibility of generalization to quality scores on arbitrary scales
        score_embedding[quality_score] += weight

    # Normalization
    score_embedding_normalized = score_embedding / np.sum(score_embedding)

    return (
        100
        * (np.arange(QS_UPPER_LIMIT + 1) / QS_UPPER_LIMIT)
        @ score_embedding_normalized
    )
