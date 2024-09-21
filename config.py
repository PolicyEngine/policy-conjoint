# Define attributes and their ranges
attributes = {
    "deficit_impact": (-500, 500),  # in billions of dollars
    "poverty_reduction": (-5, 5),  # percentage points
    "inequality": (
        -5,
        5,
    ),  # change in Gini coefficient (multiplied by 100 for easier interpretation)
    "economic_growth": (-2, 5),  # percentage points of GDP growth
}

# Define display names for attributes
display_names = {
    "deficit_impact": "Deficit Impact (billions $)",
    "poverty_reduction": "Poverty Reduction (%)",
    "inequality": "Change in Inequality",
    "economic_growth": "Economic Growth (%)",
}
