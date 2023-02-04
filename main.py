"""Business scenarios with streamlit."""

import pandas as pd
import streamlit as st


FUND = 80_000
SPENDING_2_PERSONS = 12_000
SPENDING_3_PERSONS = 20_000


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
    df = pd.DataFrame({"fund": fund}, index=range(months))
    # add a column variation per month
    df['variation'] = df.diff().fillna(0)
    return df, df.iloc[-1][0]


if __name__ == "__main__":
    period1, fund = model(
        npersons=2,
        ndays_subcontract=8.5,
        ndays_direct=1.6,
        ndays_outsourced=0,
        starting_fund=70000,
        months=7
    )
    period2, fund = model(
        npersons=2,
        ndays_subcontract=8.5,
        ndays_direct=4.6,
        ndays_outsourced=0,
        starting_fund=fund,
        months=7
    )
    period3, fund = model(
        npersons=3,
        ndays_subcontract=8.5,
        ndays_direct=8.6,
        ndays_outsourced=0,
        starting_fund=fund,
        months=7
    )
    result = pd.concat([period1, period2.iloc[1:], period3.iloc[1:]], ignore_index=True, axis='index')
    print(period1)
    print()
    print(result)
