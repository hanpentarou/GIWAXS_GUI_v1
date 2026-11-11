"""
export.py
"""

import pandas as pd
import matplotlib.pyplot as plt


def export_background_result(
    q,
    raw,
    bg,
    corrected
):

    raw_df = pd.DataFrame({
        "Q": q,
        "Raw": raw
    })

    bg_df = pd.DataFrame({
        "Q": q,
        "Background": bg
    })

    corrected_df = pd.DataFrame({
        "Q": q,
        "Corrected": corrected
    })

    raw_df.to_excel(
        "../output/Raw_Data.xlsx",
        index=False
    )

    bg_df.to_excel(
        "../output/Background.xlsx",
        index=False
    )

    corrected_df.to_excel(
        "../output/Corrected.xlsx",
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