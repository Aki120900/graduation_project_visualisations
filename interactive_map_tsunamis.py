import pandas as pd
import folium
import os

# File paths
files = {
    "Alaska": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Alaska.csv",
    "Indonesia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Indonesia.csv",
    "Japan": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Japan.csv",
    "Russia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Russia.csv"
}

dataframes = {}

# Read and clean
for country, file in files.items():
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "latitude": "lat",
        "longitude": "lon",
        "earthquake magnitude": "mag",
        "maximum water height (m)": "height",
        "location name": "location"
    })

    required_columns = ['lat', 'lon', 'height']
    if not all(col in df.columns for col in required_columns):
        print(f"Missing required columns in {country}: {df.columns.tolist()}")
        continue

    df["country"] = country
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["height"] = pd.to_numeric(df["height"], errors="coerce")

    if all(col in df.columns for col in ["year", "mo", "dy"]):
        df["date"] = pd.to_datetime(dict(year=df["year"], month=df["mo"], day=df["dy"]), errors="coerce")
    else:
        df["date"] = pd.NaT

    df.dropna(subset=["lat", "lon", "height"], inplace=True)
    dataframes[country] = df

# Combine
if not dataframes:
    raise ValueError("No valid dataframes to display.")
tsunamis = pd.concat(dataframes.values(), ignore_index=True)

# Create map
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

# Add markers with styled popup
for _, row in tsunamis.iterrows():
    colour = '#00008B' if row['height'] >= 30 else '#ADD8E6'
    popup = f"""
        <b>Type:</b> Tsunami<br>
        <b>Country:</b> {row['country']}<br>
        <b>Location:</b> {row['location'] if 'location' in row and pd.notnull(row['location']) else 'Unknown'}<br>
        <b>Date:</b> {row['date'].date() if pd.notnull(row['date']) else 'Unknown'}<br>
        <b>Wave Height:</b> {row['height']} m
    """
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=colour,
        fill=True,
        fill_color=colour,
        fill_opacity=0.7,
        popup=folium.Popup(popup, max_width=300)
    ).add_to(m)

# Add legend
legend_html = '''
 <div style="position: fixed;
 bottom: 20px; left: 20px; width: 220px; height: 85px;
 background-color: white;
 border: 2px solid grey;
 z-index:9999;
 font-size:14px;
 padding: 10px;">
 <strong>Tsunami Height</strong><br>
 <span style="color:#00008B;">●</span> Height ≥ 30 m<br>
 <span style="color:#ADD8E6;">●</span> Height &lt; 30 m
 </div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save map
output_path = "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/interactive_tsunami_map.html"
m.save(output_path)
print(f"Map saved to: {output_path}")