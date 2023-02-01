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
    total = []
    for month in range(months):
        total.append(
            starting_fund
            + month
            * (spending + income(ndays_subcontract, ndays_direct, ndays_outsourced))
        )
    df = pd.DataFrame({"total": total}, index=range(months))
    return df


if __name__ == "__main__":
    result = model(
        npersons=2,
        ndays_subcontract=8.5,
        ndays_direct=1.6,
        ndays_outsourced=0,
        starting_fund=70000,
    )
    print(result)
