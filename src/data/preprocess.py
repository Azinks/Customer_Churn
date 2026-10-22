import pandas as pd

def preprocess_data(df: pd.DataFrame , target_column: str = "Churn") -> pd.DataFrame:
    """
    Preprocess the input DataFrame by handling missing values, encoding categorical variables,
    and separating features from the target variable.

    Parameters:
    df (pd.DataFrame): The input DataFrame to preprocess.
    target_column (str): The name of the target column. Default is "Churn".

    Returns:
    pd.DataFrame: The preprocessed DataFrame with features and target variable separated.
    """
    df.columns = df.columns.str.strip()  # Strip whitespace from column names

    # remove unwanted columns / drop columns that are not needed for modeling
    for col in ["CustomerID","CustomerId","customerID"]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
            break
    # normalise the target column to binary values (0 and 1)
    if target_column in df.columns and df[target_column].dtype == 'object':
        df[target_column] = df[target_column].str.strip().map({'Yes': 1, 'No': 0})

    # Handle missing values
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
        df.dropna(subset=["TotalCharges"], inplace=True)  # Drop rows where TotalCharges is NaN

    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].fillna(0).astype(int)  # Ensure SeniorCitizen is integer

    num_cols = df.select_dtypes(include=["number"]).columns
    df[num_cols] = df[num_cols].fillna(0)  # Fill missing numeric values with zero
    return df