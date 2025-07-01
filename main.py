"""
This is a fun little python application that creates practice questions for
the pricing of corporate and government bonds. It will create some random data
and ask you to price the derivative to find either the annual yield,
present value, or face value of the bond.
"""

import numpy as np
import pandas as pd
from data_generation import create_bond_data
from interest import add_continuous_interest
from value import add_pv_no_coupon, add_pv_with_coupon


# Let's design a generator that will yield a question and answer for each line
def question_generator(df: pd.DataFrame):
    """
    This is a generator that will be used to iterate through our dataframe to
    generate questions randomly and return the question and answer so that the
    user can test their knowledge.
    """
    # Lets indicate which columns we will be using for our questiosn
    question_columns = ["face_value", "coupon_rate", "pv_no_coupon", "pv_with_coupon"]

    # Iterate through the dataframe
    for _, row in df.iterrows():
        random_column = np.random.choice(question_columns)

        # We will assign one of these values to an answer and drop it
        answer = row[random_column]
        if random_column == "coupon_rate":
            answer = answer * 100

        # Drop that value so we can generate a question
        question_data = row.copy()
        question_data[random_column] = "missing"

        question = None
        # Now, lets design questions based on what is missing
        if random_column == "pv_with_coupon":
            question = (
                f"\n{row['question_id']} - You want to buy a "
                f"corporate bond with a face value of "
                f"${row['face_value']:.2f}. There are still "
                f"{row['years_to_maturity']} years to maturity. "
                f"The current market interest rate is "
                f"{row['discount_rate']:.2%}. "
                f"The bond yields {row['coupon_payment_schedule']} coupons per "
                f"year  and has an annual interest rate of "
                f"{row['coupon_rate']:.2%}. What is the current 'Net Present "
                f"Value' of the corporate bond?"
            )
        elif random_column == "pv_no_coupon":
            question = (
                f"\n{row['question_id']} - You want to buy a "
                f"corporate bond with a face value of "
                f"${row['face_value']:.2f}.There are still "
                f"{row['years_to_maturity']} years to maturity. Assume the "
                f"corporate bond is a no-coupon bond and has an annual "
                f"interest rate of {row['coupon_rate']:.2%}. "
                f"The current market interest rate is "
                f"{row['discount_rate']:.2%}.What is the "
                f"current 'Net Present Value' of the corporate bond?"
            )
        elif random_column == "face_value":
            question = (
                f"\n{row['question_id']} - A bond has a present value "
                f"of ${row['pv_with_coupon']:.2f} and yields "
                f"{row['coupon_payment_schedule']} coupons per year. "
                f"It matures in {row['years_to_maturity']} years and has an " f"annual interest rate of {row['coupon_rate']:.2%}. "
                f"The current market interest rate is "
                f"{row['discount_rate']:.2%}. What is the estimated 'face "
                f"value' of this bond?"
            )
        elif random_column == "coupon_rate":
            question = (
                f"\n{row['question_id']} - A bond is worth "
                f"${row['pv_with_coupon']:.2f} today and has face value of "
                f"${row['face_value']}. It matures in {row['years_to_maturity']} "
                f"years and pays {row['coupon_payment_schedule']} coupons per "
                f"year. The current market interest rate is "
                f"{row['discount_rate']:.2%}. What is the bond's "
                f"'annual yield'?"
            )

        yield question.strip(), np.round(answer, 2), row


# Let's create our random question generator game
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("seed", help="Integer to set random seed")
    parser.add_argument("bonds", help="How many questions do you want? ")
    args = parser.parse_args()

    # Create a dataframe containing random bonds and accurate data
    bond_data = create_bond_data(args.seed, args.bonds)
    cont_data = add_continuous_interest(bond_data)
    pv_noc_data = add_pv_no_coupon(cont_data)
    pv_wc_data = add_pv_with_coupon(pv_noc_data)

    # Let's generate a question and answer with our generator
    quiz = question_generator(pv_wc_data)
    LEARNING = True
    while LEARNING:
        try:
            questions, answers, rows = next(quiz)
            print(questions)
            response = input("Type your answer here (rounded to two decimal points): ")
            if (float(response) < np.round(answers, 2) + 0.05) and (
                float(response) > np.round(answers, 2) - 0.05
            ):
                print("Congratulations, you are correct")
            else:
                print(f"Not quite, the answer was {answers}. Let's keep practicing.")
                print(rows)

            keep_learning = input(
                "Ready for the next question? (Type: 'yes' or 'quit') "
            )
            if keep_learning.lower() == "quit":
                print("Okay, see you next time")
                LEARNING = False
            else:
                print("Okay, let's keep going... Next Qustion: ")
        except StopIteration:
            print("Congratulations you have completed all of your questions")
            LEARNING = False
