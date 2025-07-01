
# Bond Pricing Practice App

This is a Python-based educational tool designed to help students and 
professionals practice bond pricing questions. The program randomly generates 
bond characteristics and asks users to calculate values like the 
**Net Present Value**, **Face Value**, or **Annual Yield** based on real 
financial formulas. Files can be run seperately to update the .CSV record of 
bond data or the 'main.py' can be run independently to create quiz questions.

## Features

- Generates random bond data (e.g., face value, coupon rate, maturity)
- Calculate Continuous Compounding Interest Rates
- Calculates present value with and without coupons
- Asks users a mix of multiple question types
- Immediate feedback on correctness

## How It Works (Scripts)

1. `data_geneartion.py` - Random data is generated for a number of bonds and 
saved to a .CSV file titled bond_data.csv 
2. `interest.py` - Key financial metrics are calculated (continuous/discrete
interest rates) and are added to the .CSV file.
3. `value.py` - Present value with coupon and without coupon payments are 
calculated and added to the .CSV file
4. `main.py` - A generator function yields a question and correct answer. 
Allowing for participant intercation with the questions.


## Example Question

> You want to buy a corporate bond with a face value of $100.00. There are 
still 13 years to maturity. The current market interest rate is 5.66%. The 
bond yields 1 coupon per year and has an annual interest rate of 4.88%. 
What is the current 'Net Present Value' of the corporate bond?

## Getting Started

### Prerequisites

- Python 3.8+
- NumPy
- Pandas

### Create Conda Environment

```bash
git clone https://github.com/mads643v2/convert-tmacpherson6.git
conda env create -f environment.yml
```

### Run the Script

```bash
python main.py <seed> <num_questions>
```

Example:

```bash
python main.py 42 10
```

## Project Structure

- `data_generation.py`: Creates random bond data.
- `interest.py`: Calculates continuous interest.
- `value.py`: Functions to compute bond present values.
- `main.py`: The main application logic and user interaction loop.
- `enviornment.yml`: Conda virtual environment setup
- `README.md`: This file.

## License

This project is for educational use.
