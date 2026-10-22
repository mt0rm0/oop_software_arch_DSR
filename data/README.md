# Data

## `raw/telco_churn.csv`

The IBM Telco Customer Churn sample: 7,043 customers of a fictional telecom company, one row per customer.
About 26.5% of them cancelled their contract in the observed month (`Churn = Yes`).

- **Source:** [IBM/telco-customer-churn-on-icp4d](https://github.com/IBM/telco-customer-churn-on-icp4d), file `data/Telco-Customer-Churn.csv`
- **License:** Apache License 2.0 (the license of that repository)
- **Status:** read-only. Never edit this file. Every cleaning step lives in code (`src/churn/data.py`), so it can be reviewed, tested and repeated.

It is committed to git so the workshop runs offline. In your own projects, keep raw data out of git and version it with DVC instead (see notebook `X1_git_dvc_mlflow`).

### Columns

| Column | Type in the file | Meaning |
| --- | --- | --- |
| `customerID` | text | Unique customer identifier. Not a feature. |
| `gender` | Female / Male | |
| `SeniorCitizen` | 0 / 1 | 1 if the customer is 65 or older |
| `Partner`, `Dependents` | Yes / No | Household information |
| `tenure` | integer | Months the customer has been with the company. 0 means they joined this month. |
| `PhoneService` | Yes / No | |
| `MultipleLines` | Yes / No / No phone service | |
| `InternetService` | DSL / Fiber optic / No | |
| `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies` | Yes / No / No internet service | Add-on services |
| `Contract` | Month-to-month / One year / Two year | The strongest single predictor of churn |
| `PaperlessBilling` | Yes / No | |
| `PaymentMethod` | Electronic check / Mailed check / Bank transfer (automatic) / Credit card (automatic) | |
| `MonthlyCharges` | float | Current monthly bill in USD |
| `TotalCharges` | **text** | Total billed so far. Exported as text, and blank (`" "`) for the 11 customers with `tenure = 0`, who have not been billed yet. The correct value for them is 0, not "missing". |
| `Churn` | Yes / No | Target: did the customer leave? |

### Quirks worth knowing

- `TotalCharges` must be converted to a number. `pd.to_numeric(..., errors="coerce")` turns the 11 blanks into NaN. Dropping those rows (as the warm-up notebook does) silently removes every brand-new customer from the data.
- Churn depends strongly on the contract: about 43% for month-to-month, 11% for one-year and 3% for two-year contracts. Any batch of new customers can easily contain only some of the categories, which is why encoders must learn their categories on the training data (notebook 04).
