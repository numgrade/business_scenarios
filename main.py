"""Business scenarios with streamlit."""

import itertools as it

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from business_model.style import style_negative


def income(
    ndays_subcontract: int = 0,
    ndays_direct: int = 0,
    ndays_outsourced: int = 0,
    tj_sc: int = 650,
    tj_d: int = 1300,
    tj_out: int = 0.3 * 1300,
):
    """Earnings in function of the working days per month."""
    return ndays_subcontract * tj_sc + ndays_direct * tj_d + ndays_outsourced * tj_out


def model(
    npersons: int,
    ndays_subcontract: float,
    ndays_direct: float,
    ndays_outsourced: float,
    months: int = 36,
    starting_fund: float = 80000,
):
    """Income evolution in function of the number of persons and the number of working days per month."""
    if npersons == 2:
        spending = -11000
    elif npersons == 3:
        spending = -17500
    elif npersons > 3:
        spending = -17500 - npersons * 6000
    else:
        raise ValueError("Number of personns should be 2 or more.")
    fund = []
    for month in range(months):
        fund.append(
            starting_fund
            + month
            * (spending + income(ndays_subcontract, ndays_direct, ndays_outsourced))
        )
    df = pd.DataFrame({"fund [euros]": fund}, index=range(months))
    # add a column variation per month
    df["revenue"] = df.diff().fillna(0)
    df["ndays subcontract"] = ndays_subcontract
    df["ndays direct"] = ndays_direct
    df["ndays outsourced"] = ndays_outsourced
    df["npersons"] = npersons
    # naming index
    df.index.name = "month"
    return df, df.iloc[-1][0]


# Dashboard with Dash
app = Dash(__name__)

widgets_children = [
    [
        html.Br(),
        html.Br(),
        html.Label(f"Phase {i}"),
        html.Br(),
        html.Label("Duration [months]"),
        dcc.Slider(
            id=f"duration{i}",
            min=0,
            max=24,
            marks={i: str(i) for i in range(1, 25)},
            value=6,
        ),
        html.Br(),
        html.Label("Number of employees"),
        dcc.Slider(
            id=f"nemployees{i}",
            min=2,
            max=3,
            marks={i: str(i) for i in range(2, 4)},
            value=2,
        ),
        html.Br(),
        html.Label("Number of days - subcontract"),
        dcc.Slider(
            id=f"ndays_subcontract{i}",
            min=0,
            max=40,
            marks={i: str(i) for i in range(41)},
            value=8.5,
        ),
        html.Br(),
        html.Label("Number of days - direct"),
        dcc.Slider(
            id=f"ndays_direct{i}",
            min=0,
            max=40,
            marks={i: str(i) for i in range(41)},
            value=1.6,
        ),
        html.Br(),
        html.Label("Number of days - outsourced"),
        dcc.Slider(
            id=f"ndays_outsourced{i}",
            min=0,
            max=40,
            marks={i: str(i) for i in range(41)},
            value=0,
        ),
    ]
    for i in range(1, 4)
]

app.layout = html.Div(
    [
        html.Div(
            children=html.H1(children="Business model", style={"textAlign": "left"})
        ),
        html.Div(
            children="Fund and revenue evolutions in function of time, number of working days and number of employees.",
            style={"textAlign": "left"},
        ),
        html.Div(
            children=list(it.chain(*widgets_children)),
            style={"padding": 20, "flex": 1},
        ),
        dcc.Graph(id="business-graph", style={"height": "90vh"}),
    ]
)


@app.callback(
    Output(component_id="business-graph", component_property="figure"),
    Input(component_id="duration1", component_property="value"),
    Input(component_id="nemployees1", component_property="value"),
    Input(component_id="ndays_subcontract1", component_property="value"),
    Input(component_id="ndays_direct1", component_property="value"),
    Input(component_id="ndays_outsourced1", component_property="value"),
    Input(component_id="duration2", component_property="value"),
    Input(component_id="nemployees2", component_property="value"),
    Input(component_id="ndays_subcontract2", component_property="value"),
    Input(component_id="ndays_direct2", component_property="value"),
    Input(component_id="ndays_outsourced2", component_property="value"),
    Input(component_id="duration3", component_property="value"),
    Input(component_id="nemployees3", component_property="value"),
    Input(component_id="ndays_subcontract3", component_property="value"),
    Input(component_id="ndays_direct3", component_property="value"),
    Input(component_id="ndays_outsourced3", component_property="value"),
)
def update_graph(
    duration1,
    nemployees1,
    ndays_subcontract1,
    ndays_direct1,
    ndays_outsourced1,
    duration2,
    nemployees2,
    ndays_subcontract2,
    ndays_direct2,
    ndays_outsourced2,
    duration3,
    nemployees3,
    ndays_subcontract3,
    ndays_direct3,
    ndays_outsourced3,
):
    period1, fund = model(
        npersons=nemployees1,
        ndays_subcontract=ndays_subcontract1,
        ndays_direct=ndays_direct1,
        ndays_outsourced=ndays_outsourced1,
        starting_fund=70000,
        months=duration1,
    )
    period2, fund = model(
        npersons=nemployees2,
        ndays_subcontract=ndays_subcontract2,
        ndays_direct=ndays_direct2,
        ndays_outsourced=ndays_outsourced2,
        starting_fund=fund,
        months=duration2,
    )
    period3, fund = model(
        npersons=nemployees3,
        ndays_subcontract=ndays_subcontract3,
        ndays_direct=ndays_direct3,
        ndays_outsourced=ndays_outsourced3,
        starting_fund=fund,
        months=duration3,
    )
    result = pd.concat(
        [period1, period2.iloc[1:], period3.iloc[1:]], ignore_index=True, axis="index"
    )
    # print(result)
    # apply red color to negative values - for display in notebook
    result_redcolor = result.style.applymap(style_negative, props="color:red;")

    # Create 2 subplots
    fig = make_subplots(rows=2, cols=1)

    # 1st plot
    fig.add_trace(
        go.Scatter(
            x=result.index,
            y=result["revenue"],
            marker=dict(color="SteelBlue"),
            name="Revenue",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=result.index,
            y=result["fund [euros]"],
            # marker=dict(color="LightSalmon"),
            marker=dict(color=result["fund [euros]"], coloraxis="coloraxis"),
            name="Fund",
            showlegend=False,  # already a color bar - so we remove the "normal legend"
        ),
        row=1,
        col=1,
    )

    # 2nd plot
    fig.add_trace(
        go.Bar(
            x=result.index,
            y=result["ndays subcontract"],
            width=0.3,
            base=0,
            marker=dict(color="LightBlue"),
            name="number of days subcontract",
        ),
        row=2,
        col=1,
    ),
    fig.add_trace(
        go.Bar(
            x=result.index,
            y=result["ndays direct"],
            width=0.3,
            base=0,
            marker=dict(color="Blue"),
            name="number of days direct",
        ),
        row=2,
        col=1,
    ),
    fig.add_trace(
        go.Bar(
            x=result.index,
            y=result["ndays outsourced"],
            width=0.3,
            base=0,
            marker=dict(color="Orange"),
            name="number of days outsourced",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=result.index,
            y=result["npersons"],
            marker=dict(color="Green"),
            name="number of employees",
        ),
        row=2,
        col=1,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="<b>months</b>", row=2, col=1)

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>fund / revenue</b> [euros]", row=1, col=1)
    fig.update_yaxes(title_text="<b># days / # employees</b>", row=2, col=1)

    fig.update_layout(
        # Color bar
        coloraxis=dict(colorscale="Bluered_r"),
        # legend position
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )  # , showlegend=False)

    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
    # visit http://127.0.0.1:8050/ in your web browser.
