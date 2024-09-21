import streamlit as st
import pandas as pd
import numpy as np
import logging
from config import attributes, display_names
from visualization import plot_relative_importance
from data_utils import dataframe_to_string

logger = logging.getLogger(__name__)


def simplified_analysis(df):
    try:
        st.write("Simplified Analysis:")

        # Map attribute names to column prefixes
        attr_map = {
            "deficit_impact": "Deficit Impact (billions $)",
            "poverty_reduction": "Poverty Reduction (%)",
            "inequality": "Change in Inequality",
            "economic_growth": "Economic Growth (%)",
        }

        # Check the dataframe structure and prepare data accordingly
        if set(df.columns) == set(["choice", "attribute", "value", "chosen"]):
            # Data is in long format
            df_wide = df.pivot(columns="attribute", values="value")
            df_wide["chosen"] = df["chosen"]
        elif "attribute" in df.columns and set(attr_map.keys()).issubset(
            set(df.columns)
        ):
            # Data is already in wide format
            df_wide = df
        else:
            # Prepare data for analysis
            df_long = pd.DataFrame()
            for attr, col_name in attr_map.items():
                df_temp = df[
                    [
                        f"{col_name} (Option 1)",
                        f"{col_name} (Option 2)",
                        "choice",
                    ]
                ]
                df_temp = df_temp.melt(
                    id_vars=["choice"], var_name="option", value_name=attr
                )
                df_temp["option"] = df_temp["option"].apply(
                    lambda x: "1" if "Option 1" in x else "2"
                )
                if df_long.empty:
                    df_long = df_temp
                else:
                    df_long = pd.merge(
                        df_long, df_temp, on=["choice", "option"]
                    )

            df_long["chosen"] = (df_long["choice"] == 1) & (
                df_long["option"] == "1"
            ) | (df_long["choice"] == 2) & (df_long["option"] == "2")
            df_wide = df_long

        # Calculate mean values
        mean_values = df_wide.groupby("chosen")[list(attr_map.keys())].mean()
        st.write("Mean Values for Chosen vs Not Chosen:")
        mean_values_display = mean_values.rename(columns=display_names)
        st.code(dataframe_to_string(mean_values_display))

        # Calculate relative importance
        relative_importance = (mean_values.iloc[1] - mean_values.iloc[0]).abs()
        total_importance = relative_importance.sum()
        relative_importance = (
            relative_importance / total_importance
            if total_importance != 0
            else relative_importance
        )

        st.write("Simplified Relative Importance of Attributes:")
        importance_df = pd.DataFrame(
            {
                "Attribute": [display_names[attr] for attr in attr_map.keys()],
                "Importance": relative_importance.values,
            }
        )
        st.code(dataframe_to_string(importance_df))

        plot_relative_importance(
            dict(zip(attr_map.keys(), relative_importance.values))
        )

        # Calculate direction of impact
        direction_of_impact = (
            mean_values.iloc[1] - mean_values.iloc[0]
        ).apply(
            lambda x: (
                "Positive" if x > 0 else "Negative" if x < 0 else "No impact"
            )
        )
        st.write("Direction of Impact:")
        impact_df = pd.DataFrame(
            {
                "Attribute": [display_names[attr] for attr in attr_map.keys()],
                "Direction": direction_of_impact.values,
            }
        )
        st.code(dataframe_to_string(impact_df))

    except Exception as e:
        logger.error(f"Simplified analysis failed: {str(e)}", exc_info=True)
        st.warning(
            f"An error occurred during simplified analysis: {str(e)}. Please check your input data and try again."
        )

        # Print additional debugging information
        st.write("Debugging Information:")
        st.write(f"DataFrame columns: {df.columns}")
        st.write(f"DataFrame sample:\n{df.head()}")
        st.write(
            f"df_wide sample:\n{df_wide.head() if 'df_wide' in locals() else 'df_wide not created'}"
        )
