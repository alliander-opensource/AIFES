import pandas as pd
import plotly 
import plotly.graph_objects as go


def get_quantile_fill_color_code_blue(quantile, opacity=None):
    if opacity:
        return f"rgba(0, 0, 255, {opacity})"    
    else:
        return f"rgba(0, 0, 255, {(9 - (abs(quantile - 50) * 2 / 100)) / 2 + 0.2})"

def get_quantile_fill_color_code_plasma(quantile, opacity=0.5):
    plasma_hex_color = plotly.colors.sequential.Plasma[int(round(9 - 9 * abs(quantile - 50) * 2 / 100))]
    red = int(plasma_hex_color[1:3], 16)
    green = int(plasma_hex_color[3:5], 16)
    blue = int(plasma_hex_color[5:7], 16)

    return f"rgba({red}, {green}, {blue}, {opacity})"

def filter_quantile_columns(columns: list[str]):
    quantile_columns = [column for column in columns if column[:8] == "quantile"]
    return quantile_columns

def infer_quantiles(columns: list[str]) -> list[int]:
    quantile_columns = filter_quantile_columns(columns)
    quantiles = [quantile_column[-2:] for quantile_column in quantile_columns]
    return quantiles

def shade_area_between_two_quantiles(fig, outer_quantile, inner_quantile, 
                                 outer_quantile_percentage, inner_quantile_percentage):
    if int(outer_quantile_percentage) > int(inner_quantile_percentage):
        name = f"{int(inner_quantile_percentage)}%-{int(outer_quantile_percentage)}% Percentile"
    else: 
        name = f"{int(outer_quantile_percentage)}%-{int(inner_quantile_percentage)}% Percentile"

    fig.add_trace(go.Scatter(
        x=outer_quantile.index.to_series(),
        y=outer_quantile,
        mode="lines",       
        line_color='rgba(255,255,255,0)',
        line_shape="vh",
        showlegend=False
        # name=""
    ))

    fig.add_trace(go.Scatter(
        x=inner_quantile.index.to_series(),
        y=inner_quantile,
        mode="lines",
        fill="tonexty",
        fillcolor=get_quantile_fill_color_code_plasma(int(outer_quantile_percentage)),
        line_color='rgba(255,255,255,0)',
        line_shape="vh",
        showlegend=True,
        name=name,
    ))

def plot_realized_and_forecast_lines(realized, forecast, horizon):
    # Plot realized and forecast lines
    fig = pd.DataFrame(dict(Forecast=forecast, Realized=realized)).plot(
        title=f"Realized load and forecasted load (forecasting horizon: {horizon} hours)", 
        labels=dict(value="Load [MW]", index="Datetime [UTC]", variable=""),
        template="simple_white",
    )
    fig.update_traces(
         line=dict(color=get_quantile_fill_color_code_plasma(quantile=50, opacity=1), width=2, shape="vh"),
         selector=lambda x: 'Forecast' in x.name)
    fig.update_traces(
         line=dict(color="red", width=1.5, shape="vh"),
         selector=lambda x: 'Realized' in x.name)
    
    return fig

def visualize_quantiles(fig, quantiles: pd.DataFrame):
    # Visualize quantiles
    quantile_percentages = infer_quantiles(quantiles.columns)
    quantile_percentages.sort()
    n_quantiles = len(quantile_percentages)
    
    # The 50th quantile is excluded from the visualization
    bottom_quantiles = [q for q in quantile_percentages if int(q) < 50]
    top_quantiles = [q for q in quantile_percentages if int(q) > 50]
    middle_quantiles = [bottom_quantiles[-1], top_quantiles[0]] 

    # Vizualize top quantiles
    for i in range(0, len(bottom_quantiles) - 1):
        outer_quantile_percentage = bottom_quantiles[i]
        inner_quantile_percentage = bottom_quantiles[i + 1]

        shade_area_between_two_quantiles(
            fig=fig, 
            outer_quantile=quantiles[f"quantile_P{outer_quantile_percentage}"],
            inner_quantile=quantiles[f"quantile_P{inner_quantile_percentage}"],
            outer_quantile_percentage=outer_quantile_percentage,
            inner_quantile_percentage=inner_quantile_percentage,
        )

    # Shade area between middle quantiles
    inner_quantile_percentage = middle_quantiles[0]
    outer_quantile_percentage = middle_quantiles[1]

    shade_area_between_two_quantiles(
        fig=fig, 
        outer_quantile=quantiles[f"quantile_P{outer_quantile_percentage}"],
        inner_quantile=quantiles[f"quantile_P{inner_quantile_percentage}"],
        outer_quantile_percentage=outer_quantile_percentage,
        inner_quantile_percentage=inner_quantile_percentage,
    )

    # Vizualize bottom quantiles
    for i in range(0, len(top_quantiles) - 1):
        inner_quantile_percentage = top_quantiles[i]
        outer_quantile_percentage = top_quantiles[i + 1]

        shade_area_between_two_quantiles(
            fig=fig, 
            outer_quantile=quantiles[f"quantile_P{outer_quantile_percentage}"],
            inner_quantile=quantiles[f"quantile_P{inner_quantile_percentage}"],
            outer_quantile_percentage=outer_quantile_percentage,
            inner_quantile_percentage=inner_quantile_percentage,
        )

    

def plot_quantile_forecasts_and_realized(realized: pd.Series, 
                                         forecast: pd.Series, 
                                         quantiles: pd.DataFrame,
                                         horizon: float):
      
    fig = plot_realized_and_forecast_lines(realized, forecast, horizon)
    visualize_quantiles(fig, quantiles)

    fig.show()