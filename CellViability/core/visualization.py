import string

import pandas
import plotly.graph_objects

__all__ = ["plate_map"]


def plate_map(
    filename: str, data: pandas.DataFrame, colname: str, controls: dict | list, q_rows: int = 16, q_columns: int = 24
) -> None:
    """
    Plot a plate heatmap with control highlighting and save to HTML.

    Parameters
    ----------
    filename : str
        Output HTML file path.
    data : pandas.DataFrame
        Input data. Must contain a 'well' column in format 'A01', 'B12', etc.
    colname : str
        Column name to use for heatmap values.
    controls : dict or list
        Control wells. Can be either:
        - dict with keys {'positive': [...], 'negative': [...]}
        - list of wells treated as negative control
    q_rows : int, optional
        Number of rows in the plate (default is 16).
    q_columns : int, optional
        Number of columns in the plate (default is 24).
    """
    if "well" not in data.columns:
        raise ValueError("Input data must contain a 'well' column")
    # Extract row and column from well
    data[["row", "column"]] = data["well"].str.extract(r"([A-Za-z]+)(\d+)")
    data["column"] = data["column"].astype(int)

    # Fill missing wells if plate is incomplete
    expected_wells = q_rows * q_columns
    if len(data) != expected_wells:
        rows = list(string.ascii_uppercase[:q_rows])
        columns = list(range(1, q_columns + 1))
        full_grid = pandas.MultiIndex.from_product([rows, columns], names=["row", "column"]).to_frame(index=False)
        data = pandas.merge(full_grid, data, on=["row", "column"], how="left")

    # Pivot to plate format
    plate_matrix = data.pivot(index="row", columns="column", values=colname)

    # Prepare numeric indices for overlays
    data["row_idx"] = data["row"].apply(lambda r: string.ascii_uppercase.index(r))
    data["col_idx"] = data["column"] - 1

    # Parse controls
    positive_wells = controls.get("positive", []) if isinstance(controls, dict) else []
    negative_wells = (
        controls.get("negative", []) if isinstance(controls, dict) else controls if isinstance(controls, list) else []
    )

    data["control_type"] = None
    data.loc[data["well"].isin(positive_wells), "control_type"] = "positive"
    data.loc[data["well"].isin(negative_wells), "control_type"] = "negative"

    # Heatmap
    fig = plotly.graph_objects.Figure(
        data=plotly.graph_objects.Heatmap(
            z=plate_matrix.values,
            x=list(range(1, q_columns + 1)),
            y=list(string.ascii_uppercase[:q_rows]),  # A on top, P at bottom
            hoverinfo="text",
            text=[
                [
                    f"Well: {r}{c:02}<br>Value: {plate_matrix.loc[r, c]:.2f}" if c in plate_matrix.columns else ""
                    for c in plate_matrix.columns
                ]
                for r in plate_matrix.index
            ],
            colorscale="bluered",
            colorbar={
                "title": colname,
                "thickness": 20,  # width of the colorbar in pixels
                "outlinewidth": 2,  # line width around the colorbar
                "outlinecolor": "black",  # line color around the colorbar
            },
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
    colors = {"negative": "green", "positive": "gray"}
    for _, row in data.dropna(subset=["control_type"]).iterrows():
        fig.add_shape(
            type="rect",
            x0=row["col_idx"] + 0.5,
            x1=row["col_idx"] + 1.5,
            y0=row["row_idx"] - 0.5,
            y1=row["row_idx"] + 0.5,
            line={"color": colors[row["control_type"]], "width": 4},
            fillcolor="rgba(0,0,0,0)",
            xref="x",
            yref="y",
        )

    # Remove titles and axis labels
    fig.update_layout(
        plot_bgcolor="white",
        autosize=False,
        width=max(600, q_columns * 50),  # set width based on number of columns
        height=900,
        margin={"b": 120, "l": 60, "r": 60, "t": 80},
        legend={"orientation": "h", "y": -0.01},
        title={"text": data["plate"].iat[0], "x": 0.5},
    )
    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1, q_columns + 1)),
        ticktext=[str(i) for i in range(1, q_columns)],  # column index
        showticklabels=True,
        side="top",
    )
    fig.update_yaxes(
        autorange="reversed",
        scaleanchor="x",
        scaleratio=1,
        tickmode="array",
        tickvals=list(string.ascii_uppercase[:q_rows]),
        ticktext=list(string.ascii_uppercase[:q_rows]),  # show row letters
        showticklabels=True,
    )

    # Legend traces for controls below heatmap
    legend_items = []
    if negative_wells:
        legend_items.append(
            plotly.graph_objects.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={"color": "white", "symbol": "square", "size": 14, "line": {"color": "gray", "width": 4}},
                name="Negative Control",
            )
        )
    if positive_wells:
        legend_items.append(
            plotly.graph_objects.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={"color": "white", "symbol": "square", "size": 14, "line": {"color": "green", "width": 4}},
                name="Positive Control",
            )
        )

    for trace in legend_items:
        fig.add_trace(trace)

    fig.write_html(filename)
