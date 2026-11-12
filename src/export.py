"""
export.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from peak_fitting import pseudo_voigt


def export_background_result(
    q,
    raw,
    bg,
    corrected
):

    pd.DataFrame({
        "Q": q,
        "Raw": raw
    }).to_excel(
        "../output/Raw_Data.xlsx",
        index=False
    )

    pd.DataFrame({
        "Q": q,
        "Background": bg
    }).to_excel(
        "../output/Background.xlsx",
        index=False
    )

    pd.DataFrame({
        "Q": q,
        "Corrected": corrected
    }).to_excel(
        "../output/Corrected.xlsx",
        index=False
    )


def export_peak_list(peak_df):

    peak_df.to_excel(
        "../output/Peak_List.xlsx",
        index=False
    )


def export_peak_fit(fit_df):

    fit_df.to_excel(
        "../output/Peak_Fit.xlsx",
        index=False
    )

def save_background_plots(
    q,
    raw,
    bg,
    corrected
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        q,
        raw,
        label="Raw Data"
    )

    plt.plot(
        q,
        bg,
        label="Background"
    )

    plt.xlabel("Q")
    plt.ylabel("Intensity")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "../output/Raw_vs_BG.png",
        dpi=300
    )

    plt.close()

    plt.figure(figsize=(10, 6))

    plt.plot(
        q,
        corrected,
        label="Corrected"
    )

    plt.xlabel("Q")
    plt.ylabel("Intensity")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "../output/Corrected.png",
        dpi=300
    )

    plt.close()

def save_fit_plots(
    q,
    corrected,
    fit_curve,
    residual
):

    plt.figure(figsize=(10, 6))

    plt.plot(
        q,
        corrected,
        label="Corrected Data"
    )

    plt.plot(
        q,
        fit_curve,
        label="Pseudo-Voigt Fit"
    )

    plt.legend()

    plt.xlabel("Q")
    plt.ylabel("Intensity")

    plt.tight_layout()

    plt.savefig(
        "../output/Peak_Fit.png",
        dpi=300
    )

    plt.close()

    plt.figure(figsize=(10, 4))

    plt.plot(
        q,
        residual
    )

    plt.axhline(
        0,
        linestyle="--"
    )

    plt.xlabel("Q")
    plt.ylabel("Residual")

    plt.tight_layout()

    plt.savefig(
        "../output/Residual.png",
        dpi=300
    )

    plt.close()


def save_peak_components_plot(
    q,
    corrected,
    popt,
    fit_curve
):

    plt.figure(figsize=(12, 7))

    plt.plot(
        q,
        corrected,
        color="black",
        label="Corrected Data"
    )

    plt.plot(
        q,
        fit_curve,
        color="red",
        linewidth=2,
        label="Total Fit"
    )

    n_peaks = len(popt) // 4

    colors = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:pink"
    ]

    for i in range(n_peaks):

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

        plt.plot(
            q,
            component,
            "--",
            color=colors[i % len(colors)],
            label=f"Peak {i+1}"
        )

    plt.xlabel("Q")
    plt.ylabel("Intensity")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "../output/Peak_Components.png",
        dpi=300
    )

    plt.close()

def export_peak_components(
    component_df
):

    component_df.to_excel(
        "../output/Peak_Components.xlsx",
        index=False
    )

def export_peak_report(
    fit_df,
    component_df,
    fit_curve_df,
    raw_bg_df,
    r_squared,
    chi_square,
    reduced_chi_square
):

    with pd.ExcelWriter(
        "../output/Peak_Report.xlsx"
    ) as writer:

        component_df.to_excel(
            writer,
            sheet_name="PeakComponents",
            index=False
        )

        fit_curve_df.to_excel(
            writer,
            sheet_name="Residuals",
            index=False
        )

        raw_bg_df.to_excel(
            writer,
            sheet_name="RawBackground",
            index=False
        )

        summary_df = pd.DataFrame({

            "Metric": [

                "R2",
                "ChiSquare",
                "ReducedChiSquare"

            ],

            "Value": [

                r_squared,
                chi_square,
                reduced_chi_square

            ]

        })

        summary_df.to_excel(

            writer,

            sheet_name="Summary",

            index=False

        )

        fit_df.to_excel(

            writer,

            sheet_name="PeakParameters",

            index=False

        )

def make_raw_background_df(
    q,
    raw,
    bg,
      corrected
):

    return pd.DataFrame({

        "Q": q,

        "Raw": raw,

        "Background": bg,

        "Corrected": corrected

    })

def make_fit_curve_df(
    q,
    corrected,
    fit_curve,
    residual
):

    return pd.DataFrame({

        "Q": q,

        "Corrected": corrected,

        "Fit": fit_curve,

        "Residual": residual

    })

def make_peak_components_df(
    q,
    corrected,
    fit_curve,
    popt
):

    component_df = pd.DataFrame()

    component_df["Q"] = q
    component_df["Corrected"] = corrected
    component_df["TotalFit"] = fit_curve

    n_peaks = len(popt) // 4

    for i in range(n_peaks):

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

        component_df[
            f"Peak_{i+1}"
        ] = component

    return component_df

def export_fit_curve_df(
    fit_curve_df
):

    fit_curve_df.to_excel(
        "../output/Fit_Curve_Residual.xlsx",
        index=False
    )

def save_area_distribution_plot(
    fit_df
):

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        fit_df["Peak"],
        fit_df["Area_Percent"],
        color="tab:blue"
    )

    plt.xlabel(
        "Peak Number"
    )

    plt.ylabel(
        "Area Percent (%)"
    )

    plt.title(
        "Peak Area Distribution"
    )

    plt.tight_layout()

    plt.savefig(
        "../output/Area_Distribution.png",
        dpi=300
    )

    plt.close()   