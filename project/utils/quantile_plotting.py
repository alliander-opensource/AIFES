import pandas as pd
import plotly 
import plotly.graph_objects as go


def get_quantile_fill_color_code_blue(quantile, opacity=None):
    if opacity:
        return f"rgba(0, 0, 255, {opacity})"    
    else:
        return f"rgba(0, 0, 255, {(1 - (abs(quantile - 50) * 2 / 100)) / 2 + 0.2})"

def get_quantile_fill_color_code_plasma(quantile, opacity=0.5):
    plasma_hex_color = plotly.colors.sequential.Plasma[int(abs(quantile - 50) * 2 / 10)]
    red = int(plasma_hex_color[1:3], 16)
    green = int(plasma_hex_color[3:5], 16)
    blue = int(plasma_hex_color[5:7], 16)

    return f"rgba({red}, {green}, {blue}, {opacity})"

def filter_quantile_columns(columns: list[str]):
    quantile_columns = [column for column in columns if column[:8] == "quantile"]
    return quantile_columns

def infer_quantiles(columns: list[str]) -> list[int]:
    quantile_columns = filter_quantile_columns(columns)
    quantiles = [int(quantile_column[-2:]) for quantile_column in quantile_columns]
    return quantiles

def shade_area_between_two_quantiles(fig, outer_quantile, inner_quantile, 
                                 outer_quantile_percentage, inner_quantile_percentage):
    if outer_quantile_percentage > inner_quantile_percentage:
        name = f"{inner_quantile_percentage}%-{outer_quantile_percentage}% percentile"
    else: 
        name = f"{outer_quantile_percentage}%-{inner_quantile_percentage}% percentile"

    fig.add_trace(go.Scatter(
        x=pd.concat([outer_quantile.index.to_series(), inner_quantile.index.to_series()[::-1]]),
        y=pd.concat([outer_quantile, inner_quantile[::-1]]),
        mode="lines",
        fill="toself",
        fillcolor=get_quantile_fill_color_code_plasma(int(outer_quantile_percentage)),
        line_color='rgba(255,255,255,0)',
        showlegend=True,
        name=name,
    ))

def plot_realized_and_forecast_lines(realized, forecast, horizon):
    # Plot realized and forecast lines
    fig = pd.concat([forecast, realized], axis=1).plot(
        title=f"Realized load and forecasted load (forecasting horizon: {horizon} hours)", labels=dict(value="Load (MW)", 
                                                 index="Datetime (UTC)",
                                                 variable="")
    )
    fig.update_traces(
         line=dict(color=get_quantile_fill_color_code_plasma(quantile=50, opacity=1), width=2),
         selector=lambda x: 'forecast' in x.name)
    fig.update_traces(
         line=dict(color="red", width=1.5),
         selector=lambda x: 'realised' in x.name)
    
    return fig

def visualize_quantiles(fig, quantiles: pd.DataFrame):
    # Visualize quantiles
    quantile_percentages = infer_quantiles(quantiles.columns)
    n_quantiles = len(quantile_percentages)
    
    # Both lists below include the 50th quantile
    bottom_quantiles = [q for q in quantile_percentages if q <= 50]
    top_quantiles = [q for q in quantile_percentages if q >= 50]

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