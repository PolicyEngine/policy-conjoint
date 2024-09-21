import streamlit as st
import pandas as pd
from config import attributes, display_names


def dataframe_to_string(df):
    return df.to_string()


def prepare_data(df):
    # Prepare data for analysis
    df_long = pd.melt(
        df,
        id_vars=["choice"],
        value_vars=[f"{attr}_{i}" for attr in attributes for i in [1, 2]],
        var_name="attribute",
        value_name="value",
    )
    df_long["chosen"] = (
        (df_long["attribute"].str.endswith("_1") & (df_long["choice"] == 1))
        | (df_long["attribute"].str.endswith("_2") & (df_long["choice"] == 2))
    ).astype(int)
    df_long["attribute"] = (
        df_long["attribute"].str.replace("_1", "").str.replace("_2", "")
    )

    # Pivot the dataframe to have attributes as columns
    df_wide = df_long.pivot(columns="attribute", values="value")
    df_wide["chosen"] = df_long["chosen"]

    return df_long, df_wide


def log_data_statistics(df):
    st.write("Data Statistics:")
    stats_df = df.groupby("attribute")["value"].describe()
    stats_df = stats_df.rename(index=display_names)
    st.code(dataframe_to_string(stats_df))
