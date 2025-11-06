import string

import pandas
import plotly.graph_objects

__all__ = ["plate_map"]


def plate_map(
    data: pandas.DataFrame, plate: str | int, controls: dict | list, q_rows: int = 16, q_columns: int = 24
) -> None:
    """
    Plot a microplate heatmap with control highlighting.

    Parameters
    ----------
    data : pandas.DataFrame
        Input data. Must contain a 'well' column in format 'A01', 'B12', etc.
        The last numeric column will be used for heatmap values.
    controls : dict or list
        Control wells. Can be either:
        - dict with keys {'positive': [...], 'negative': [...]}
        - list of wells treated as negative controls
    q_rows : int, optional
        Number of plate rows (default: 16)
    q_columns : int, optional
        Number of plate columns (default: 24)
    """
    property_name = data.select_dtypes(include="number").columns[-1]

    # Extract row and column from well
    data[["row", "column"]] = data["well"].str.extract(r"([A-Za-z]+)(\d+)")
    data["column"] = data["column"].astype(int)

    # Fill missing wells if plate is incomplete
    if len(data) != q_rows * q_columns:
        rows = list(string.ascii_uppercase[:q_rows])
        columns = list(range(1, q_columns + 1))
        full_grid = pandas.MultiIndex.from_product([rows, columns], names=["row", "column"]).to_frame(index=False)
        data = pandas.merge(full_grid, data, on=["row", "column"], how="left")

    # Identify the last numeric column for heatmap
    last_col = data.select_dtypes(include="number").columns[-1]

    # Pivot to plate format
    plate_matrix = data.pivot(index="row", columns="column", values=last_col)

    # Prepare numeric indices for overlays
    data["row_idx"] = data["row"].apply(lambda r: string.ascii_uppercase.index(r))
    data["col_idx"] = data["column"] - 1

    # Parse controls
    positive_wells = []
    negative_wells = []
    if isinstance(controls, dict):
        positive_wells = controls.get("positive", [])
        negative_wells = controls.get("negative", [])
    elif isinstance(controls, list):
        negative_wells = controls

    data["control_type"] = None
    data.loc[data["well"].isin(positive_wells), "control_type"] = "positive"
    data.loc[data["well"].isin(negative_wells), "control_type"] = "negative"

    # Heatmap
    fig = plotly.graph_objects.Figure(
        data=plotly.graph_objects.Heatmap(
            z=plate_matrix.values,  # NÃO inverte o array
            x=list(range(1, q_columns + 1)),
            y=list(string.ascii_uppercase[:q_rows]),  # A no topo, P embaixo
            hoverinfo="text",
            text=[
                [
                    f"Well: {r}{c:02d}<br>Value: {plate_matrix.loc[r, c] if c in plate_matrix.columns else ''}"
                    for c in plate_matrix.columns
                ]
                for r in plate_matrix.index
            ],
            colorscale="bluered",
            zmin=plate_matrix.min().min(),
            zmax=plate_matrix.max().max(),
        )
    )

    # Black borders for all wells
    for i in range(q_rows):
        for j in range(q_columns):
            fig.add_shape(
                type="rect",
                x0=j + 0.5,
                x1=j + 1.5,
                y0=i - 0.5,
                y1=i + 0.5,
                line={"color": "black", "width": 1},
                fillcolor="rgba(0,0,0,0)",
                xref="x",
                yref="y",
            )

    # Control overlays
    for _, row in data.dropna(subset=["control_type"]).iterrows():
        color = "green" if row["control_type"] == "negative" else "gray"
        fig.add_shape(
            type="rect",
            x0=row["col_idx"] + 0.5,
            x1=row["col_idx"] + 1.5,
            y0=row["row_idx"] - 0.5,
            y1=row["row_idx"] + 0.5,
            line={"color": color, "width": 4},
            fillcolor="rgba(0,0,0,0)",
            xref="x",
            yref="y",
        )
    fig.update_yaxes(autorange="reversed", scaleanchor="x", scaleratio=1)
    # Remove titles and axis labels
    fig.update_layout(
        xaxis={"showticklabels": False, "title": None},
        yaxis={"showticklabels": False, "title": None},
        plot_bgcolor="white",
        height=900,
        margin={"b": 120},
        legend={"orientation": "h", "y": -0.2},
    )

    # Legend traces for controls below heatmap
    legend_items = []
    if negative_wells:
        legend_items.append(
            plotly.graph_objects.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={"symbol": "square", "size": 14, "line": {"color": "green", "width": 4}},
                name="Negative Control",
            )
        )
    if positive_wells:
        legend_items.append(
            plotly.graph_objects.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={"symbol": "square", "size": 14, "line": {"color": "gray", "width": 4}},
                name="Positive Control",
            )
        )

    for trace in legend_items:
        fig.add_trace(trace)

    fig.write_html(f"plate_map_{plate}_{property_name}.html")
