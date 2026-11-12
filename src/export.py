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

    plt.plot(q, raw, label="Raw Data")
    plt.plot(q, bg, label="Background")

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

    component_df.to_excel(
        "../output/Peak_Components.xlsx",
        index=False
    )
