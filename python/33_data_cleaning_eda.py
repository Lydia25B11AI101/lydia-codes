# ============================================================
# Program Title : Data Cleaning & EDA Pipeline
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Reusable EDA pipeline -- handles missing
#                 values, outlier detection, and basic stats.
# ============================================================

import pandas as pd
import numpy as np

def load_sample():
    records = [
        {"name": "Alice",  "age": 22,   "score": 88.5, "grade": "A"},
        {"name": "Bob",    "age": None, "score": 73.0, "grade": "B"},
        {"name": "Cara",   "age": 20,   "score": None, "grade": None},
        {"name": "David",  "age": 21,   "score": 95.0, "grade": "A"},
        {"name": "Eve",    "age": 23,   "score": 200.0,"grade": "A"},  # outlier
        {"name": "Frank",  "age": 19,   "score": 60.5, "grade": "C"},
        {"name": "Grace",  "age": 22,   "score": 78.0, "grade": "B"},
    ]
    return pd.DataFrame(records)

def summarise(df):
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} cols")
    print(f"Missing values:\n{df.isnull().sum()}\n")

def fill_missing(df):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df

def iqr_outliers(df, col):
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    lo, hi = Q1 - 1.5*IQR, Q3 + 1.5*IQR
    return df[(df[col] < lo) | (df[col] > hi)], lo, hi


# -- Demo ------------------------------------------------------
if __name__ == "__main__":
    df = load_sample()
    print("Before cleaning:")
    summarise(df)

    df = fill_missing(df)
    print("After filling:")
    summarise(df)

    outliers, lo, hi = iqr_outliers(df, "score")
    print(f"Score IQR bounds: [{lo:.1f}, {hi:.1f}]")
    print(f"Outliers:\n{outliers}")
    print("\nDescriptive stats:")
    print(df.describe().round(2))
