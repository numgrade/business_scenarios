"""Business scenarios with streamlit."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

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
    # naming index
    df.index.name = "month"
    return df, df.iloc[-1][0]


if __name__ == "__main__":
    period1, fund = model(
        npersons=2,
        ndays_subcontract=8.5,
        ndays_direct=1.6,
        ndays_outsourced=0,
        starting_fund=70000,
        months=7,
    )
    period2, fund = model(
        npersons=2,
        ndays_subcontract=8.5,
        ndays_direct=4.6,
        ndays_outsourced=0,
        starting_fund=fund,
        months=7,
    )
    period3, fund = model(
        npersons=3,
        ndays_subcontract=8.5,
        ndays_direct=4.6,
        ndays_outsourced=0,
        starting_fund=fund,
        months=7,
    )
    result = pd.concat(
        [period1, period2.iloc[1:], period3.iloc[1:]], ignore_index=True, axis="index"
    )
    result.index.name = period1.index.name
    print(result)
    # apply red color to negative values - for display in notebook
    result_redcolor = result.style.applymap(style_negative, props="color:red;")

    # # Streamlit app
    # st.title('Business model')
    # st.write(result_redcolor)
    # st.bar_chart(result["fund"])
    # st.line_chart(result["revenue"])

    # plotly
    # result.reset_index(inplace=True)
    # fig = px.line(result, x="month", y="revenue", color=px.Constant("Revenue"))
    # fig.add_bar(result, x="month", y="fund [euros]", name="Fund")
    # fig = go.Figure()
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=result.index,
            y=result["revenue"],
            marker=dict(color="SteelBlue"),
            name="Revenue",
            # secondary_y=False,
        )
    )
    fig.add_trace(
        go.Bar(
            x=result.index,
            y=result["fund [euros]"],
            marker=dict(color="LightSalmon"),
            name="Fund",
            # secondary_y=False,
        )
    )
    fig.add_trace(
        go.Bar(
            x=result.index,
            y=result[["ndays subcontract", "ndays direct", "ndays outsourced"]],
            # marker=dict(color='LightSalmon'),
            # name='Fund',
            # secondary_y=True,
        )
    )

    # Set x-axis title
    fig.update_xaxes(title_text="months")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>fund</b> [euros]", secondary_y=False)
    fig.update_yaxes(title_text="<b># days</b>", secondary_y=True)

    fig.show()
