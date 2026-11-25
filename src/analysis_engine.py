
import pandas as pd
import numpy as np
import os

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

def run_analysis(
        filename,
        q_min=0.18,
        window=40,
        smooth_scale=5e4,
        log_callback=None,
        output_dir="../output"
    ):

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    def log(message):

        print(message)

        if log_callback:

            log_callback(message)

    print()
    print(f"Running analysis: {filename}")

    df = load_giwaxs(
        filename
    )

    df = df[
        df["Q"] >= q_min
    ].copy()

    q = df["Q"].values

    raw = df["Intensity"].values

    error = df["Error"].values
    bg, corrected = subtract_background(
        q,
        raw,
        window=window,
        smooth_scale=smooth_scale
    )

    log(
        "Exporting ..."
    )

    export_background_result(
        q,
        raw,
        bg,
        corrected,
        output_dir
    )

    save_background_plots(
        q,
        raw,
        bg,
        corrected,
        output_dir
    )

    log(
        "Detecting peaks ..."
    )

    peak_df = detect_peaks_profile(
        q,
        corrected
    )

    export_peak_list(
        peak_df,
        output_dir
    )


    log(
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
        fit_df,
        output_dir
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

        reduced_chi_square,

        q_min,

        window,

        smooth_scale,

        output_dir

    )

    export_fit_curve_df(
        fit_curve_df,
        output_dir
    )

    save_fit_plots(
        q,
        corrected,
        fit_curve,
        residual,
        output_dir
    ) 

    save_peak_components_plot(
        q,
        corrected,
        popt,
        fit_curve,
        output_dir
    )

    export_peak_components(
        component_df,
        output_dir
    )

    save_area_distribution_plot(
        fit_df,
        output_dir
    )

    print()
    print("Fit Results")
    print(fit_df)


    print()

    log(
        "Finished."
    )

    print(
        "Results saved in output/"
    )

    print()

    return {

        "r2": r_squared,

        "chi2": chi_square,

        "reduced_chi2": reduced_chi_square,

        "num_peaks": len(fit_df),

        "peak_table": fit_df[
            [
                "Peak",
                "Q",
                "d",
                "Area_Percent"
            ]
        ]
    }

#if __name__ == "__main__":

#    run_analysis(
#        "../data/2026-08-06_Selenium1_GIWAXS_ICA_0.2_28s_7h_Qz_Q.dat_counts.txt",
#        output_dir="../output/Test_Output"
#    )


import glob
import os


def run_batch_analysis(
    folder,
    q_min=0.18,
    window=40,
    smooth_scale=5e4,
    log_callback=None
):

    txt_files = glob.glob(
        os.path.join(
            folder,
            "*.txt"
        )
    )

    results = []

    total = len(txt_files)

    for i, filename in enumerate(txt_files):

        sample_name = os.path.splitext(
            os.path.basename(filename)
        )[0]

        output_dir = os.path.join(
            "..",
            "output",
            sample_name
        )

        if log_callback:

            log_callback(
                f"[{i+1}/{total}] {sample_name}"
            )

        result = run_analysis(

            filename,

            q_min=q_min,

            window=window,

            smooth_scale=smooth_scale,

            log_callback=log_callback,

            output_dir=output_dir

        )

        results.append({

            "Sample": sample_name,

            "R2": result["r2"],

            "Chi2": result["chi2"],

            "ReducedChi2": result["reduced_chi2"],

            "PeakCount": result["num_peaks"]

        })

    summary_df = pd.DataFrame(
        results
    )

    summary_df.to_excel(

        os.path.join(
            "..",
            "output",
            "Batch_Summary.xlsx"
        ),

        index=False

    )

    return summary_df