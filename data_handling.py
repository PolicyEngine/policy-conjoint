import streamlit as st
import numpy as np
from scipy.stats import qmc
from config import attributes


def generate_profile():
    # Create a Latin Hypercube sampler
    sampler = qmc.LatinHypercube(d=len(attributes))

    # Generate a sample
    sample = sampler.random(n=1)[0]

    # Scale the sample to the attribute ranges
    profile = {}
    for i, (attr, (low, high)) in enumerate(attributes.items()):
        profile[attr] = low + sample[i] * (high - low)

    return profile


def record_choice(profile1, profile2, choice):
    data_entry = {f"{attr}_1": value for attr, value in profile1.items()}
    data_entry.update({f"{attr}_2": value for attr, value in profile2.items()})
    data_entry["choice"] = choice
    st.session_state.data.append(data_entry)
    st.session_state.num_comparisons += 1
    st.rerun()


def generate_experiment_design(num_comparisons):
    # Create a Latin Hypercube sampler for all profiles
    sampler = qmc.LatinHypercube(d=len(attributes) * 2)

    # Generate samples for all comparisons
    samples = sampler.random(n=num_comparisons)

    # Scale the samples to the attribute ranges
    designs = []
    for sample in samples:
        profile1 = {}
        profile2 = {}
        for i, (attr, (low, high)) in enumerate(attributes.items()):
            profile1[attr] = low + sample[i] * (high - low)
            profile2[attr] = low + sample[i + len(attributes)] * (high - low)
        designs.append((profile1, profile2))

    return designs


# Add this function to initialize the experiment design
def initialize_experiment(num_comparisons=10):
    if "experiment_design" not in st.session_state:
        st.session_state.experiment_design = generate_experiment_design(
            num_comparisons
        )
    if "current_comparison" not in st.session_state:
        st.session_state.current_comparison = 0


# Modify this function to use the pre-generated design
def get_next_comparison():
    if st.session_state.current_comparison < len(
        st.session_state.experiment_design
    ):
        profile1, profile2 = st.session_state.experiment_design[
            st.session_state.current_comparison
        ]
        st.session_state.current_comparison += 1
        return profile1, profile2
    else:
        return None, None
