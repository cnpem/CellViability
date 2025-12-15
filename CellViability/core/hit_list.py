import os

import pandas

__all__ = ["hit_list"]


def hit_list(
    filename: str,
    controls: dict | list,
    z_threshold: float = 0.5,
    incp_threshold: float = 0.3,
    zscore_column: str = "zscore",
    plate_column: str = "plate",
    well_column: str = "well",
    incp_column: str = "inCPE",
):
    """
    Process a screening summary file and extract plates and hits based on Z-score
    and inCPE thresholds.

    Workflow
    --------
    1. Identify:
        - Z-positive plates  (Z-score >= 0)
        - Z-strict plates    (Z-score >= z_threshold)

    2. Remove control wells (provided by user/JSON config).

    3. Identify hits:
        - Any well with inCPE >= incp_threshold.
        - Hits are not separated by plate; instead, all hits from qualifying plates
          are concatenated into two global tables:
            - hits_z_positive
            - hits_z_strict

    4. Save results into an Excel file containing:
        - z_positive          (Z >= 0)
        - z_strict            (Z >= z_threshold)
        - hits_z_positive
        - hits_z_strict

    Parameters
    ----------
    filename : str
        Path to the Excel summary file.

    controls : dict or list
        Dictionary with named control groups, each containing a list of control wells.

    z_threshold : float
        Minimum Z-score to classify a plate as "strict".

    incp_threshold : float
        Minimum inCPE value to classify a well as a hit.

    zscore_column : str
        Column name used for Z-score values within the Z-score sheet.

    plate_column : str
        Column name identifying plates in the Z-score sheet.

    well_column : str
        Column name identifying wells in plate sheets.

    incp_column : str
        Column name identifying inCPE values in plate sheets.

    Returns
    -------
    dict
        A dictionary with:
        - "z_positive_plates": list of plates with Z >= 0
        - "z_strict_plates": list of plates with Z >= z_threshold
        - "output": path to the saved Excel file
    """

    # ------------------------------------------------------------
    # 1. Read all sheets
    # ------------------------------------------------------------
    sheets = pandas.read_excel(filename, sheet_name=None)

    if "Z-score" not in sheets:
        raise ValueError("Sheet 'Z-score' does not exist.")

    zdf = sheets["Z-score"]

    # ------------------------------------------------------------
    # 2. Z-positive (Z >= 0)
    # ------------------------------------------------------------
    z_positive_df = zdf[zdf[zscore_column] >= 0].copy()
    z_positive_plates = z_positive_df[plate_column].unique().tolist()

    # ------------------------------------------------------------
    # 3. Z-strict (Z >= threshold)
    # ------------------------------------------------------------
    z_strict_df = zdf[zdf[zscore_column] >= z_threshold].copy()
    z_strict_plates = z_strict_df[plate_column].unique().tolist()

    # ------------------------------------------------------------
    # 4. Prepare controls
    # ------------------------------------------------------------
    control_wells = set()
    for _, wells in controls.items():
        control_wells.update(wells)

    # ------------------------------------------------------------
    # 5. Collect hits for both Z categories
    # ------------------------------------------------------------
    hits_z_positive = []
    hits_z_strict = []

    for plate, pdf in sheets.items():
        # skip special sheet
        if plate == "Z-score":
            continue

        if well_column not in pdf.columns or incp_column not in pdf.columns:
            continue

        # remove control wells
        pdf_no_ctrl = pdf[~pdf[well_column].isin(control_wells)].copy()

        # hits: wells where inCPE >= threshold
        hits = pdf_no_ctrl[pdf_no_ctrl[incp_column] >= incp_threshold].copy()
        hits["plate"] = plate

        # Add to Z-positive group
        if plate in z_positive_plates:
            hits_z_positive.append(hits)

        # Add to Z-strict group
        if plate in z_strict_plates:
            hits_z_strict.append(hits)

    # concatenate
    hits_z_positive = pandas.concat(hits_z_positive, ignore_index=True) if hits_z_positive else pandas.DataFrame()

    hits_z_strict = pandas.concat(hits_z_strict, ignore_index=True) if hits_z_strict else pandas.DataFrame()

    # ------------------------------------------------------------
    # 6. Save Excel
    # ------------------------------------------------------------
    output_dir = os.path.dirname(os.path.abspath(filename))
    output_path = os.path.join(output_dir, "hits_results.xlsx")

    with pandas.ExcelWriter(output_path) as writer:
        z_positive_df.to_excel(writer, sheet_name="z_positive", index=False)
        z_strict_df.to_excel(writer, sheet_name="z_strict", index=False)
        hits_z_positive.to_excel(writer, sheet_name="hits_z_positive", index=False)
        hits_z_strict.to_excel(writer, sheet_name="hits_z_strict", index=False)

    return {
        "z_positive_plates": z_positive_plates,
        "z_strict_plates": z_strict_plates,
        "output": output_path,
    }
