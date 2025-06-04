import pandas as pd
import plotly.express as px
import os

# Load the dataset
df = pd.read_csv("/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Value/Total_Infrastructure_Exposed_value_by_country.csv")

# Create the choropleth map
fig = px.choropleth(
    df,
    locations="country_name",
    locationmode="country names",
    color="Exposed value (Million USD)",
    hover_name="country_name",
    color_continuous_scale="Viridis",
    title="Total Infrastructure Exposed Value by Country (in Million USD)"
)

# Update layout settings
fig.update_layout(
    geo=dict(showframe=False, showcoastlines=True)
)

# Save output as HTML
base_dir = "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Value"
output_path = os.path.join(base_dir, "choropleth_map_infrastructure.html")
fig.write_html(output_path)