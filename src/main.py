"""
GIWAXS Background Subtraction Engine
"""
import pandas as pd
import numpy as np

from peak_fitting import (
    fit_peaks,
    fwhm_pseudo_voigt,
    peak_area,
    calculate_r_squared,
    calculate_chi_square,
    calculate_reduced_chi_square
)


from peak_detection import (
    detect_peaks_profile
)

from export import (
    export_background_result,
    save_background_plots,
    export_peak_list,
    save_fit_plots,
    save_peak_components_plot,
    export_peak_components
)

from data_loader import load_giwaxs

from background import (
    subtract_background
)

INPUT_FILE = (
    "../data/"
    "2026-08-06_Selenium1_GIWAXS_ICA_0.2_28s_7h_Qz_Q.dat_counts.txt"
)


def main():

    print()

    print("Loading data ...")

    df = load_giwaxs(
        INPUT_FILE
    )

    df = df[
        df["Q"] >= 0.18
    ].copy()

    q = df["Q"].values

    raw = df["Intensity"].values

    print(
        f"Loaded {len(df)} points"
    )

    print(
        "Calculating SNIP+Spline background ..."
    )

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
        peak_df
    )

    fit_results = []

    n = len(popt) // 4

    for i in range(n):

        amp = popt[i * 4]

        center = popt[i * 4 + 1]

        sigma = popt[i * 4 + 2]

        eta = popt[i * 4 + 3]

        fit_results.append({

            "Peak": i + 1,

            "Q": center,

            "d": 2 * np.pi / center,

            "FWHM": fwhm_pseudo_voigt(
                sigma,
                eta
            ),

            "Area": peak_area(
                amp,
                sigma,
                eta
            ),

            "Height": amp,

            "Eta": eta

        })

    fit_df = pd.DataFrame(
    fit_results
)

    r_squared = calculate_r_squared(
        corrected,
        fit_curve
    )

    chi_square = calculate_chi_square(
        corrected,
        fit_curve
    )

    reduced_chi_square = (
        calculate_reduced_chi_square(
            corrected,
            fit_curve,
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

    fit_df.to_excel(
        "../output/Peak_Fit.xlsx",
        index=False
    )   

    fit_curve_df = pd.DataFrame({

    "Q": q,

    "Corrected": corrected,

    "Fit": fit_curve,

    "Residual": residual

    })

    fit_curve_df.to_excel(
        "../output/Fit_Curve_Residual.xlsx",
        index=False
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
        q,
        corrected,
        fit_curve,
        popt
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


if __name__ == "__main__":
    main()