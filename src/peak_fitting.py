import numpy as np

from scipy.optimize import curve_fit


def pseudo_voigt(
    x,
    amplitude,
    center,
    sigma,
    eta
):

    gaussian = np.exp(
        -((x - center) ** 2)
        /
        (2 * sigma ** 2)
    )

    lorentz = (
        1
        /
        (
            1
            +
            (
                (x - center)
                / sigma
            ) ** 2
        )
    )

    return amplitude * (

        eta * lorentz

        +

        (1 - eta) * gaussian

    )


def multi_pseudo_voigt(
    x,
    *params
):

    y = np.zeros_like(x)

    n_peaks = len(params) // 4

    for i in range(n_peaks):

        amp = params[i * 4]
        cen = params[i * 4 + 1]
        sig = params[i * 4 + 2]
        eta = params[i * 4 + 3]

        y += pseudo_voigt(
            x,
            amp,
            cen,
            sig,
            eta
        )

    return y

def fit_peaks(
    q,
    corrected,
    peak_df,
    error
):
    
    p0 = []
    lower_bounds = []
    upper_bounds = []

    q_step = np.median(np.diff(q))

    for _, row in peak_df.iterrows():
        q0 = float(row["Q"])

        idx = np.argmin(
            np.abs(q - q0)
        )

        amplitude0 = max(
            float(corrected[idx]),
            1.0
        )

        sigma0 = max(
            float(row["FWHM_pts"]) * q_step / 2.2,
            0.005
        )

        p0.extend([
            amplitude0,
            q0,
            sigma0,
            0.5
        ])

        lower_bounds.extend([
            0.0,          # amplitude
            q0 - 0.08,    # center
            1e-5,         # sigma
            0.0           # eta
        ])

        upper_bounds.extend([
            np.inf,       # amplitude
            q0 + 0.08,    # center
            0.50,         # sigma
            1.0           # eta
        ])

    safe_error = np.where(
        error > 0,
        error,
        np.nanmedian(error)
    )

    popt, pcov = curve_fit(

        multi_pseudo_voigt,

        q,

        corrected,

        p0=p0,

        sigma=safe_error,

        absolute_sigma=True,

        bounds=(
            lower_bounds,
            upper_bounds
        ),

        maxfev=200000
    )

    fit_curve = multi_pseudo_voigt(
        q,
        *popt
    )

    residual = corrected - fit_curve

    return (
        popt,
        pcov,
        fit_curve,
        residual
    )

def fwhm_pseudo_voigt(
    sigma,
    eta
):
    x_local = np.linspace(
        -10 * sigma,
        10 * sigma,
        20001
    )

    profile = pseudo_voigt(
        x_local,
        1.0,
        0.0,
        sigma,
        eta
    )

    half_max = 0.5

    above = np.where(
        profile >= half_max
    )[0]

    if len(above) < 2:
        return np.nan

    return (
        x_local[above[-1]]
        - x_local[above[0]]
    )


def peak_area(
    amplitude,
    sigma,
    eta
):
    gaussian_area = (
        amplitude
        * sigma
        * np.sqrt(2 * np.pi)
    )

    lorentzian_area = (
        amplitude
        * np.pi
        * sigma
    )

    return (
        (1 - eta) * gaussian_area
        + eta * lorentzian_area
    )

def calculate_r_squared(
    observed,
    fitted
):
    ss_res = np.sum(
        (observed - fitted) ** 2
    )

    ss_tot = np.sum(
        (observed - np.mean(observed)) ** 2
    )

    if ss_tot == 0:
        return np.nan

    return 1 - ss_res / ss_tot

def calculate_chi_square(
    observed,
    fitted,
    error
):

    safe_error = np.where(
        error > 0,
        error,
        np.nanmedian(error)
    )

    return np.sum(

        (
            (observed - fitted)

            /

            safe_error

        ) ** 2

    )

def calculate_reduced_chi_square(
    observed,
    fitted,
    error,
    n_parameters
):

    chi2 = calculate_chi_square(
        observed,
        fitted,
        error
    )

    dof = max(
        len(observed)
        -
        n_parameters,
        1
    )

    return chi2 / dof