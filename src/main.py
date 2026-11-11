"""
GIWAXS Background Subtraction Engine
"""

from data_loader import load_giwaxs

from background import (
    subtract_background
)

from export import (
    export_background_result,
    save_background_plots
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