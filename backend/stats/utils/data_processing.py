"""
@author: Joseph A.
Description: Utility functions for processing and transforming DataFrame data
"""
import pandas as pd

def count_split_data(df:pd.DataFrame, column_name:str):
    """Count occurrences of values in a comma-separated column.

    Args:
        df (pd.DataFrame): Input DataFrame containing the data
        column_name (str): Name of the column containing comma-separated values

    Raises:
        ValueError: If the specified column doesn't exist in the DataFrame

    Returns:
        pd.Series: Series containing value counts, where:
            - Index: unique values from the split column
            - Values: count of occurrences for each value
    """
    # Check if columns exist
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' doesn't exist in the Dataframe")

    split_values = df[column_name].fillna('').str.split(',\s*')
    flattened_values = [value.strip() for sublist in split_values if isinstance(sublist, list)
                    for value in sublist if value.strip()]
    return pd.Series(flattened_values).value_counts()

def explode_split_data(df:pd.DataFrame, column_name:str):
    """Explode a DataFrame based on a comma-separated column.

    Args:
        df (pd.DataFrame):  Input DataFrame containing the data
        column_name (str): Name of the column containing comma-separated values

    Raises:
        ValueError: If the specified column doesn't exist in the DataFrame

    Returns:
        pd.DataFrame: Exploded DataFrame where:
            - Each comma-separated value gets its own row
            - Original row data is duplicated for each split value
            - Empty values are removed
            - Index is reset
    """
    # Check if columns exist
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' doesn't exist in the Dataframe")

    df_copy = df.copy()

    df_copy[column_name] = df_copy[column_name].fillna('').str.split(',\s*')

    df_exploded = df_copy.explode(column_name)
    df_exploded[column_name] = df_exploded[column_name].str.strip()
    df_exploded = df_exploded[df_exploded[column_name] != '']

    return df_exploded.reset_index(drop=True)
