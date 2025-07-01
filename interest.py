"""
This is a python script that contains functions to calculate continuous interest as well as discrete interest for compounding questions. Not all functions are currently used in the pipeline, but they are available for futures use as the practice database is expanded.
"""

import numpy as np
import pandas as pd


def continuous_interest_calculation(
    interest_rate: float, compounding_frequency: float
) -> float:
    """
    This function is used to calculate continuous interest from a bond
    yield with discrete interest

    Parameters:
    interest_rate: compounding frequency interest rate
    compounding_frequency: Compounding frequency per annum

    Output:
    continuous_interest: adjusted interest rate for continuous compounding
    """
    # Calculate continuous interest rates.
    continuous_interest = np.round(
        compounding_frequency * np.log(1 + interest_rate / compounding_frequency), 6
    )
    return continuous_interest


def compounding_interest(continuous_rate: float, compounding_frequency: float) -> float:
    """
    This function is used to calculate discrete compounding interest from a bond
    yield with continuous interest

    Parameters:
    continuous_rate: Continuous interest rate
    compounding_frequency: Number of times value will be compounded per year

    Output:
    compounding_interest: adjusted interest rate for discrete interest rate
    """
    discrete_rate = np.round(
        compounding_frequency * (np.exp(continuous_rate / compounding_frequency) - 1), 6
    )
    return discrete_rate


def add_continuous_interest(df: pd.DataFrame):
    """
    This is a function that will calculate the continuous interest rate and add
    it to the dataframe

    Parameters:
    df: pd.DataFrame - Pandas DataFrame containing bond information

    Output:
    pd.DataFrame - Containing additional column with continuous interest
    """

    df["continuous_rate"] = df.apply(
        lambda row: continuous_interest_calculation(
            row["coupon_rate"], row["coupon_payment_schedule"]
        ),
        axis=1,
    )

    return df


# Calculate continuous interest and create a checkpoint file if run individually.
if __name__ == "__main__":
    from data_generation import read_file
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_path", help="Indicate the path to the file you wish to open"
    )
    args = parser.parse_args()

    # Load in the data file
    data = read_file(args.file_path)

    # Add the continuous interest rate to the dataframe and save
    data = add_continuous_interest(data)

    # We are just going to update the file here however it should be a new
    # file in production
    data.to_csv(args.file_path, index=False)
