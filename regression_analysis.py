import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import logging
from config import attributes, display_names
from visualization import plot_relative_importance
from data_utils import dataframe_to_string
from simplified_analysis import simplified_analysis

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def btl_model(params, X, y):
    linear_predictor = np.dot(X, params)
    p = 1 / (1 + np.exp(-linear_predictor))
    log_likelihood = np.sum(
        y * np.log(p + 1e-10) + (1 - y) * np.log(1 - p + 1e-10)
    )
    return -log_likelihood


def try_regression_analysis(df):
    try:
        logger.info("Starting BTL regression analysis")
        X, y = prepare_data_for_regression(df)
        logger.info(f"Data prepared. X shape: {X.shape}, y shape: {y.shape}")

        initial_params = np.zeros(X.shape[1])
        logger.info(f"Initial parameters: {initial_params}")

        result = minimize(
            btl_model, initial_params, args=(X, y), method="BFGS"
        )
        logger.info(f"Model fitting complete. Success: {result.success}")

        if not result.success:
            logger.warning(
                f"Model fitting did not converge. Message: {result.message}"
            )

        st.write("Bradley-Terry-Luce Model Coefficient Estimates:")
        coef_df = pd.DataFrame(
            {
                "Attribute": [display_names[attr] for attr in attributes],
                "Coefficient": result.x,
            }
        )
        st.code(dataframe_to_string(coef_df))
        logger.info(f"Coefficients:\n{coef_df}")

        relative_importance = calculate_relative_importance(result.x)
        plot_relative_importance(relative_importance)

        st.write("Model Summary:")
        final_log_likelihood = -btl_model(result.x, X, y)
        st.code(f"Final log-likelihood: {final_log_likelihood:.2f}")
        logger.info(f"Final log-likelihood: {final_log_likelihood:.2f}")

        simplified_analysis(df)

        return True

    except Exception as e:
        logger.error(f"BTL model analysis failed: {str(e)}", exc_info=True)
        st.warning(
            f"BTL model analysis failed: {str(e)}. Using simplified analysis only."
        )
        simplified_analysis(df)
        return False


def prepare_data_for_regression(df):
    logger.info("Preparing data for regression")
    X = (
        df[[f"{attr}_1" for attr in attributes]].values
        - df[[f"{attr}_2" for attr in attributes]].values
    )
    y = (df["choice"] == 1).astype(int).values
    logger.info(
        f"Data preparation complete. X shape: {X.shape}, y shape: {y.shape}"
    )
    return X, y


def calculate_relative_importance(coef):
    logger.info("Calculating relative importance")
    abs_coef = np.abs(coef)
    relative_importance = abs_coef / abs_coef.sum()

    st.write("Relative Importance of Attributes (from BTL Model):")
    importance_df = pd.DataFrame(
        {
            "Attribute": [display_names[attr] for attr in attributes],
            "Importance": relative_importance,
        }
    )
    st.code(dataframe_to_string(importance_df))
    logger.info(f"Relative importance:\n{importance_df}")

    return dict(zip(attributes, relative_importance))


def log_state():
    logger.info("Current state:")
    for key, value in st.session_state.items():
        if isinstance(value, (int, float, str, bool)):
            logger.info(f"{key}: {value}")
        elif isinstance(value, list) and len(value) > 0:
            logger.info(
                f"{key}: List with {len(value)} items. First item: {value[0]}"
            )
        else:
            logger.info(f"{key}: {type(value)}")


log_state()
