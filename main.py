import streamlit as st
import pandas as pd
import logging
from data_handling import (
    record_choice,
    initialize_experiment,
    get_next_comparison,
)
from analysis_main import analyze_results
from config import attributes, display_names

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run_conjoint_experiment():
    st.title("TCJA Conjoint Analysis Tool")

    if "data" not in st.session_state:
        st.session_state.data = []

    if "num_comparisons" not in st.session_state:
        st.session_state.num_comparisons = 0

    # Initialize the experiment design
    initialize_experiment(20)  # Increased to 20 comparisons

    # Display current analysis if there's data
    if st.session_state.data:
        with st.expander("Current Analysis", expanded=False):
            analyze_results(st.session_state.data)

    profile1, profile2 = get_next_comparison()

    if profile1 and profile2:
        st.write(
            f"Comparison {st.session_state.num_comparisons + 1} of 20"
        )  # Updated to 20

        col1, col2 = st.columns(2)

        with col1:
            st.write("Option 1")
            for attr, value in profile1.items():
                st.write(f"{display_names[attr]}: {value:.2f}")
            if st.button("Choose Option 1"):
                record_choice(profile1, profile2, 1)

        with col2:
            st.write("Option 2")
            for attr, value in profile2.items():
                st.write(f"{display_names[attr]}: {value:.2f}")
            if st.button("Choose Option 2"):
                record_choice(profile1, profile2, 2)

    else:
        st.write("All comparisons completed. Final analysis:")
        analyze_results(st.session_state.data)

    # Add a button to force analysis even if less than 20 comparisons
    if (
        st.session_state.num_comparisons >= 10
        and st.session_state.num_comparisons < 20
    ):
        if st.button("Finish and Analyze Results"):
            st.write("Final analysis:")
            analyze_results(st.session_state.data)


if __name__ == "__main__":
    run_conjoint_experiment()
