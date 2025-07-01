"""
This is a python script that will calculate the present and future value of
corporate or government bonds. It will take into account whether the bond has
coupons or not, and will return the present value based on the discount rate
and time to maturity.
"""

import numpy as np
import pandas as pd
from interest import discount_rate


# Let's start by defining a function.
def present_value_no_coupon(face_value: float, duration: float = 1.0) -> float:
    """
    This function will take a bond and calculate the discounted present value

    Parameters:
    face_value: The face value of the corporate/government bond
    discount_rate: Market interest rate
    duration: The maturity of the bond in years
    coupons: Number of coupons the bond pays

    Retuns:
    present_value: Float of the current present value of the bond
    """
    # Find the discount rate for the given duration
    discounted_rate = discount_rate(duration)

    # Present value calculation
    pres_val = face_value / ((1 + discounted_rate) ** duration)

    return pres_val


def future_value_no_coupon(
    present_value: float,
    duration: float = 1.0,
) -> float:
    """
    This function will take a bond and calculate the future value based
    on interest rates

    Parameters:
    present_value: The we are currently paying for the bond
    duration: The maturity of the bond in years
    coupons: Number of coupons the bond pays

    retuns:
    future_value: Float of the expected return of the corporate/government bond
    """
    # Find the discount rate for the given duration
    discounted_rate = discount_rate(duration)
    # Future value calculations
    future_value = present_value * ((1 + discounted_rate) ** duration)
    return future_value


def present_value_with_coupon(
    face_value: float,
    coupon_rate: float,
    coupon_schedule: int = 1,
    time: float = 1.0,
) -> float:
    """
    This function will take a bond and calculate the discounted present value

    Parameters:
    face_value: The face value of the corporate/government bond
    interest_rate: Annual interest rate
    coupon_schedule: Number of coupon payments per year
    time: The maturity of the bond in years

    Retuns:
    present_value: Float of the current present value of the bond
    """
    # We need to create a list of the periods
    coupon_maturities = np.arange(1, time * coupon_schedule + 1) / coupon_schedule

    present_value = 0.0

    for coupons in coupon_maturities:
        # Calculate the discount rate for each period
        discount_rate_per_period = discount_rate(coupons)
        # Calculate the coupon value for each period
        coupon_value = face_value * (coupon_rate / coupon_schedule)
        # calculate the pressent value for each period
        if coupons == time:
            # If it's the last period, we add the face value
            present_value += (coupon_value + face_value) / (
                1 + discount_rate_per_period
            ) ** coupons
        else:
            # Otherwise, we just add the coupon value
            present_value += coupon_value / (1 + discount_rate_per_period) ** coupons

    return present_value


def add_pv_no_coupon(df: pd.DataFrame):
    """
    This function will add our present value with no coupons to our dataframe

    Parameters:
    df: Our dataframe containing corporate/government bond information

    Output:
    pd.DataFrame: containing out present value if no coupon
    """
    df["pv_no_coupon"] = df.apply(
        lambda row: present_value_no_coupon(
            row["face_value"], row["years_to_maturity"]
        ),
        axis=1,
    )
    return df


def add_pv_with_coupon(df: pd.DataFrame):
    """
    This function will add our present value accounting for coupons to our dataframe

    Parameters:
    df: Our dataframe containing corporate/government bond information

    Output:
    pd.DataFrame: containing out present value accounting for coupons
    """
    df["pv_with_coupon"] = df.apply(
        lambda row: present_value_with_coupon(
            row["face_value"],
            row["coupon_rate"],
            row["coupon_payment_schedule"],
            row["years_to_maturity"],
        ),
        axis=1,
    )
    return df


# Calculate interest and create a checkpoint file if run individually.
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

    # Add the present values with or without coupons
    data = add_pv_no_coupon(data)
    data = add_pv_with_coupon(data)

    # We are just going to update the file here however it should be a new
    # file in production
    data.to_csv(args.file_path, index=False)
