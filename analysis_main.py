import streamlit as st
import pandas as pd
import logging
from config import attributes, display_names
from regression_analysis import try_regression_analysis
from simplified_analysis import simplified_analysis
from data_utils import prepare_data, log_data_statistics, dataframe_to_string

logger = logging.getLogger(__name__)


def analyze_results(data):
    st.write("Analysis of Results")

    if len(data) < 2:
        st.warning(
            f"Not enough data for analysis. Please complete at least 2 comparisons. Current: {len(data)}"
        )
        return

    try:
        df = pd.DataFrame(data)
        logger.debug(f"Raw dataframe:\n{dataframe_to_string(df)}")

        df_long, df_wide = prepare_data(df)

        # Attempt Conditional Logit model analysis
        st.write("Conditional Logit Model Analysis:")
        cl_success = try_regression_analysis(df)

        # Perform simplified analysis
        st.write("Simplified Analysis:")
        simplified_analysis(df_long)

        # Interactive data table
        st.write("Raw Data:")
        df_display = df.copy()
        df_display.columns = [
            (
                f"{display_names.get(col.replace('_1', '').replace('_2', ''), col)} (Option {col[-1]})"
                if col != "choice"
                else col
            )
            for col in df.columns
        ]
        st.code(dataframe_to_string(df_display))

        # Log additional statistics
        log_data_statistics(df_long)

        if not cl_success:
            st.warning(
                "Note: The Conditional Logit model analysis failed. Please interpret the simplified analysis results with caution."
            )
        else:
            st.success(
                "Conditional Logit model analysis was successful. You can interpret both the model results and the simplified analysis."
            )

        st.write("Interpretation Guide:")
        st.write(
            "1. The Conditional Logit model provides a more robust analysis of the paired comparison data."
        )
        st.write(
            "2. Positive coefficients indicate that higher values of that attribute increase the likelihood of being chosen."
        )
        st.write(
            "3. The relative importance shows which attributes have the strongest influence on choices."
        )
        st.write(
            "4. The simplified analysis provides an alternative view and can be used as a sanity check."
        )
        st.write(
            "5. If the results from both methods align, it strengthens our confidence in the findings."
        )

    except Exception as e:
        logger.error(
            f"An error occurred during analysis: {str(e)}", exc_info=True
        )
        st.error(
            f"An error occurred during analysis: {str(e)}. Please check your input data and try again."
        )
