import numpy as np
from typing import List, Union


def gini_coefficient(x: Union[List[Union[float, int]], np.ndarray]) -> float:
    """
    Calculates the Gini coefficient (GC) for a given input list of descriptive biometric quality scores.

    Note:
    -----
    Descriptive (e.g. mean or median) quality scores are expected as input, with each input value representing a specific demographic distribution.
    To calculate the proposed GC-SQFR and GC-CSQFR, which follow a “higher is better” semantic in the range [0,1], where a value of 1 represents maximum fairness and a value of 0 represents minimum fairness,
    one needs to calculate 1 - gini_coefficient(x) or (1 - gini_coefficient(x))**3 respecitively.

    Parameters:
    ----------
    x : List[float], List[int] or array-like
        A list or array of numerical values (e.g. mean or median) quality scores for which to calculate the Gini coefficient.
        Must contain more than one element.

    Returns:
    -------
    float
        The Gini coefficient for the input list of quality scores.

    Raises:
    ------
    ValueError
        If the input list contains a single quality score or if the denominator is zero.

    Example:
    -------
    Mean_QS_Group_A, Mean_QS_Group_B, Mean_QS_Group_C = 35, 95, 89

    >>> gini_coefficient([35, 95, 89])
    0.273972602739726

    >>> Mean_GC_SQFR = 1 - gini_coefficient([35, 95, 89])
    0.726027397260274

    >>> Mean_GC_CSQFR = (1 - gini_coefficient([35, 95, 89])**3)
    0.38270049894991737
    """
    n = len(x)
    if n <= 1:
        raise ValueError(
            "The input list must contain more than one quality score to compute the Gini coefficient."
        )

    # Calculate the numerator as the sum of absolute differences between all pairs (i, j)
    numerator = sum(abs(x[i] - x[j]) for i in range(n) for j in range(n))

    # Calculate the denominator: 2 * (n^2) * mean of x
    denominator = 2 * (n**2) * np.mean(x)

    if denominator == 0:
        raise ZeroDivisionError("Denominator is zero")

    # Compute the raw Gini coefficient
    gc = numerator / denominator

    # Correction factor N/(N-1) to account for smaller group numbers (n)
    correction_factor = n / (n - 1)

    # Return the adapted Gini coefficient
    return gc * correction_factor
