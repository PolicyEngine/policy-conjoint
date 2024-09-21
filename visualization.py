import streamlit as st
import plotly.graph_objects as go
from config import display_names


def plot_relative_importance(relative_importance):
    # Convert the dictionary to lists for plotting
    attributes = list(relative_importance.keys())
    importances = list(relative_importance.values())

    # Create the bar plot
    fig = go.Figure(
        data=[
            go.Bar(
                x=[display_names[attr] for attr in attributes],
                y=importances,
                text=[f"{imp:.2%}" for imp in importances],
                textposition="auto",
            )
        ]
    )

    # Update the layout
    fig.update_layout(
        title="Relative Importance of Attributes",
        xaxis_title="Attributes",
        yaxis_title="Relative Importance",
        yaxis_tickformat=".2%",
    )

    # Display the plot
    st.plotly_chart(fig)
