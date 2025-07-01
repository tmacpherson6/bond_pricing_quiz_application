"""
This is a python script that will generate a .CSV file containing data for
corporate or govenment bonds. It should contain all pertinent information so
that we can calculate the present and future value of the bonds. The data will
be generated randomly so that we can practice our present and future value
calculations.
"""

import numpy as np
import pandas as pd


# Create a function that will do this for us.
def create_bond_data(seed: int = 6, n_bonds: int = 15) -> pd.DataFrame:
    """
    This is a function that will allow us to genearte data for zero-coupon
    bonds which will allow us to try our present and future value pricing
    functions against a dataset with varying interest rates and times to
    expiry.

    Parameters:
    seed: int - Set the random seed for reproducibility (default = 6)
    n_bonds: int - Set the number of bonds you want to practice with

    Output:
    pd.DataFrame - Containing bond data
    """

    # Let's set the seed so that we can generate different data or recheck data.
    np.random.seed(int(seed))

    # Define how many bonds we want and create a dataframne
    n_bonds = int(n_bonds)

    # Let's give some custom values of bond parameters
    face_values = [100, 1000, 10000, 100000]
    coupon_payment = [4, 2, 1]  # 4 is quarterly (4 payments/year), 1 is yearly

    df = pd.DataFrame(
        {
            "question_id": [f"Question {i + 1}" for i in range(n_bonds)],
            "face_value": np.random.choice(face_values, size=n_bonds),
            "years_to_maturity": np.random.randint(1, 30, size=n_bonds),
            "coupon_payment_schedule": np.random.choice(coupon_payment, size=n_bonds),
            "coupon_rate": np.round(np.random.uniform(0.01, 0.10, size=n_bonds), 4),
        }
    )

    return df


# Create a function to import a .CSV file if we aren't running the whole
# pipeline.
def read_file(file_path: str) -> pd.DataFrame:
    """
    Simple function to read in a previously saved checkpoint .CSV file

    parameters:
    file_path: str - String that contains the file path

    output:
    pd.DataFrame - Containing bond data
    """
    df = pd.read_csv(file_path)
    return df


# Create a checkpoint file if file is run seperately.
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("seed", help="Integer to set random seed")
    parser.add_argument("bonds", help="How many bonds do you want to calculate")
    parser.add_argument("output", help="Name of output file")
    args = parser.parse_args()

    data = create_bond_data(args.seed, args.bonds)
    data.to_csv(args.output, index=False)
