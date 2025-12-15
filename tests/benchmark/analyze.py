import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_regression(df: pd.DataFrame, ref_col: str, method: str, basedir: str = "tests/benchmark") -> None:
    """Generate scatter plot + linear regression for one segmentation method."""

    # Ensure output directory exists
    os.makedirs(basedir, exist_ok=True)

    # Data
    x = df[ref_col].values
    y = df[method].values

    # Linear regression (y = ax + b)
    a, b = np.polyfit(x, y, deg=1)
    y_pred = a * x + b

    # Regression line extended to full range
    x_line = np.linspace(0, 4000, 200)
    y_line = a * x_line + b

    # Metrics
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    pearson_r = np.corrcoef(x, y)[0, 1]

    # Plot
    plt.figure(figsize=(6, 5))
    plt.scatter(x, y, s=10, alpha=0.7)
    plt.plot(x_line, y_line, linewidth=1.0)

    # Identity line (y = x)
    identity = np.linspace(0, 4000, 100)
    plt.plot(identity, identity, "--", linewidth=1, color="red", label="y = x")

    plt.xlabel(ref_col)
    plt.ylabel(method)
    # plt.title(f"{method} vs {ref_col}")  # opcional

    # Axes limits
    plt.xlim(0, 4000)
    plt.ylim(0, 4000)

    plt.grid(alpha=0.3)
    plt.legend()

    # Stats box
    plt.text(
        0.025,
        0.98,
        f"$\\rho$ = {pearson_r:.4f}\nRMSE = {rmse:.1f}",
        transform=plt.gca().transAxes,
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "alpha": 0.7, "edgecolor": "none"},
    )

    plt.tight_layout()

    # Save plot
    filename = method.replace(" ", "_").replace("(", "").replace(")", "")
    filepath = f"{basedir}/{filename}.png"

    plt.savefig(filepath, dpi=500)
    plt.close()


if __name__ == "__main__":
    # Load benchmark results
    cp3 = pd.read_csv("tests/benchmark/cellpose3.csv", index_col=0)
    cp4 = pd.read_csv("tests/benchmark/cellpose4.csv", index_col=0)
    sd = pd.read_csv("tests/benchmark/stardist.csv", index_col=0)

    # Load reference results
    reference = pd.read_csv("tests/benchmark/fixtures/SLEV/S1/reference.txt", sep="\t")

    # Normalize well names (A1 → A01)
    reference["well"] = reference["WellName"].str.replace(
        r"^([A-P])(\d{1,2})$", lambda m: f"{m.group(1)}{int(m.group(2)):02d}", regex=True
    )

    # Build unified dataframe
    df = reference.set_index("well")[["Nuclei Selected - Number of Objects"]].rename(
        columns={"Nuclei Selected - Number of Objects": "Columbus (v2.4.0.104236)"}
    )
    df["Cellpose (3.1.1.2)"] = cp3["cellcount"]
    df["Cellpose (4.0.7)"] = cp4["cellcount"]
    df["StarDist (0.9.1)"] = sd["cellcount"]

    df.to_csv("tests/benchmark/cellcount.csv")

    # Methods to compare
    ref_col = "Columbus (v2.4.0.104236)"
    methods = ["Cellpose (3.1.1.2)", "Cellpose (4.0.7)", "StarDist (0.9.1)"]

    for method in methods:
        plot_regression(df, ref_col, method, basedir="tests/benchmark")
