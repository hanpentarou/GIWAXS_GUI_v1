"""
background.py

GIWAXS background correction

Default:
    SNIP + Spline
"""

from pybaselines import Baseline
from scipy.interpolate import UnivariateSpline


def snip_spline_background(
    q,
    intensity,
    window=40,
    smooth_scale=1e5
):
    """
    SNIP + spline smoothing

    Parameters
    ----------
    q : ndarray
    intensity : ndarray

    Returns
    -------
    background : ndarray
    """

    baseline = Baseline(
        x_data=q
    )

    snip_bg, _ = baseline.snip(
        intensity,
        max_half_window=window
    )

    spline = UnivariateSpline(
        q,
        snip_bg,
        s=len(q) * smooth_scale
    )

    background = spline(q)

    return background


def subtract_background(
    q,
    intensity,
    window=40,
    smooth_scale=1e5
):

    bg = snip_spline_background(
        q,
        intensity,
        window=window,
        smooth_scale=smooth_scale
    )

    corrected = intensity - bg

    return bg, corrected