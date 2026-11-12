"""
peak_detection.py
"""

import numpy as np
import pandas as pd

from scipy.signal import (
    find_peaks,
    peak_widths
)


def detect_peaks_profile(
    q,
    corrected,
    prominence=500,
    width=2,
    distance=5
):

    peaks, properties = find_peaks(
        corrected,
        prominence=prominence,
        width=width,
        distance=distance
    )

    widths = peak_widths(
        corrected,
        peaks,
        rel_height=0.5
    )[0]

    results = []

    for i, p in enumerate(peaks):

        q_peak = q[p]

        results.append({

            "Peak": i + 1,

            "Q": q_peak,

            "d": 2 * np.pi / q_peak,

            "Height": corrected[p],

            "FWHM_pts": widths[i]

        })

    return pd.DataFrame(results)