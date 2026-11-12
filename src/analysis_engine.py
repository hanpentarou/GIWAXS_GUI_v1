
import pandas as pd
import numpy as np

from data_loader import load_giwaxs

from background import (
    subtract_background
)

from peak_detection import (
    detect_peaks_profile
)

from peak_fitting import (
    fit_peaks,
    pseudo_voigt,
    fwhm_pseudo_voigt,
    peak_area,
    calculate_r_squared,
    calculate_chi_square,
    calculate_reduced_chi_square
)

from export import (
    export_background_result,
    export_peak_fit,
    export_fit_curve_df,
    save_background_plots,
    export_peak_list,
    save_fit_plots,
    save_peak_components_plot,
    export_peak_components,
    export_peak_report,
    make_raw_background_df,
    make_fit_curve_df,
    make_peak_components_df,
    save_area_distribution_plot
)

def run_analysis(filename):

    print()
    print(f"Running analysis: {filename}")

    df = load_giwaxs(
        filename
    )

    df = df[
        df["Q"] >= 0.18
    ].copy()

    q = df["Q"].values

    raw = df["Intensity"].values

    error = df["Error"].values
    bg, corrected = subtract_background(
        q,
        raw
    )

    print(
        "Exporting ..."
    )

    export_background_result(
        q,
        raw,
        bg,
        corrected
    )

    save_background_plots(
        q,
        raw,
        bg,
        corrected
    )

    print(
        "Detecting peaks ..."
    )

    peak_df = detect_peaks_profile(
        q,
        corrected
    )

    export_peak_list(
        peak_df
    )


    print(
        "Pseudo-Voigt fitting ..."
    )

    popt, pcov, fit_curve, residual = fit_peaks(
        q,
        corrected,
        peak_df,
        error
    )

    fit_results = []

    n = len(popt) // 4

    for i in range(n):

        amp = popt[i * 4]

        center = popt[i * 4 + 1]

        sigma = popt[i * 4 + 2]

        eta = popt[i * 4 + 3]

        component = pseudo_voigt(
            q,
            amp,
            center,
            sigma,
            eta
        )

        area_numerical = np.trapezoid(
            component,
            q
        )

        fit_results.append({

        "Peak": i + 1,

        "Q": center,

        "d": 2 * np.pi / center,

        "FWHM": fwhm_pseudo_voigt(
            sigma,
            eta
        ),

        "Area_Analytical": peak_area(
            amp,
            sigma,
            eta
        ),

        "Area_Numerical": area_numerical,

        "Height": amp,

        "Eta": eta

})

    fit_df = pd.DataFrame(
    fit_results
)

    total_area = fit_df[
        "Area_Numerical"
    ].sum()

    fit_df[
        "Area_Percent"
    ] = (

        fit_df["Area_Numerical"]

        /

        total_area

        *

        100

    )

    r_squared = calculate_r_squared(
        corrected,
        fit_curve
    )

    chi_square = calculate_chi_square(
        corrected,
        fit_curve,
        error
    )

    reduced_chi_square = (
        calculate_reduced_chi_square(
            corrected,
            fit_curve,
            error,
            len(popt)
        )
    )

    print()

    print(
        f"Global Fit R² = "
        f"{r_squared:.6f}"
    )

    print(
        f"Chi² = "
        f"{chi_square:.2f}"
    )

    print(
        f"Reduced Chi² = "
        f"{reduced_chi_square:.2f}"
    )

    export_peak_fit(
        fit_df
    )

    raw_bg_df = make_raw_background_df(
        q,
        raw,
        bg,
        corrected
    )

    fit_curve_df = make_fit_curve_df(
        q,
        corrected,
        fit_curve,
        residual
    )

    component_df = make_peak_components_df(
        q,
        corrected,
        fit_curve,
        popt
    )

    export_peak_report(

        fit_df,

        component_df,

        fit_curve_df,

        raw_bg_df,

        r_squared,

        chi_square,

        reduced_chi_square

    )

    export_fit_curve_df(
        fit_curve_df
    )

    save_fit_plots(
        q,
        corrected,
        fit_curve,
        residual
    ) 

    save_peak_components_plot(
        q,
        corrected,
        popt,
        fit_curve
    )

    export_peak_components(
        component_df
    )

    save_area_distribution_plot(
        fit_df
    )

    print()
    print("Fit Results")
    print(fit_df)


    print()

    print(
        "Finished."
    )

    print(
        "Results saved in output/"
    )

    print()

    return {

        "r2": r_squared,

        "chi2": chi_square,

        "reduced_chi2": reduced_chi_square

    }

if __name__ == "__main__":

    run_analysis(
        "../data/2026-08-06_Selenium1_GIWAXS_ICA_0.2_28s_7h_Qz_Q.dat_counts.txt"
    )

