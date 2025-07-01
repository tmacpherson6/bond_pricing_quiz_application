"""
This is a very simple sanity check for a $100 par bond with a 6% yield and semi
annnual coupon payments. It will calculate the net present value of the bond
based on the given discount rates and periods. This is a simple example to
ensure that the calculations are working as expected.
"""

import numpy as np

periods = [0.5, 1.0, 1.5, 2.0]

discount_rates = [0.05, 0.058, 0.064, 0.068]

face_value = 100
bond_yield = 0.06

coupon_payment = 2
coupon_revenue = face_value * bond_yield / coupon_payment

present_value = 0
for i in range(4):
    if i == 3:
        present_value += (face_value + coupon_revenue) * np.exp(
            -discount_rates[i] * periods[i]
        )

    else:
        present_value += coupon_revenue * np.exp(-discount_rates[i] * periods[i])

print(f"Net Present Value is: ${np.round(present_value, 2)}")
