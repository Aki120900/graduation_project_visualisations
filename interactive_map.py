import pandas as pd
import folium
import os
from datetime import datetime

# File paths
earthquake_files = {
    "Chile": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_Chile.csv",
    "Japan": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_Japan.csv",
    "Turkey": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_Turkey.csv",
    "California": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/earthquakes_California.csv"
}

tsunami_files = {
    "Alaska": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Alaska.csv",
    "Indonesia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Indonesia.csv",
    "Japan": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Japan.csv",
    "Russia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/tsunamis_Russia.csv"
}

volcano_files = {
    "Hawaii": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Hawaii.csv",
    "Iceland": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Iceland.csv",
    "Indonesia": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Indonesia.csv",
    "Italy": "/Users/alexandrapastouchova/Desktop/UAL/Year 3/Graduation project/Graduation project /Visualisations/Interactive_map/volcano_Italy.csv"
}



# Helper to parse date
def parse_date(row):
    try:
        return datetime(int(row['year']), int(row.get('mo', 1) or 1), int(row.get('dy', 1) or 1))
    except:
        return pd.NaT

#  Load Earthquakes 
earthquakes = []
for country, file in earthquake_files.items():
    if not os.path.exists(file):
        print(f"Missing file: {file}")
        continue
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"latitude": "lat", "longitude": "lon", "magnitude": "mag"})
    df["country"] = country
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["mag"] = pd.to_numeric(df["mag"], errors="coerce")
    df["date"] = df.apply(parse_date, axis=1)
    df["type"] = "Earthquake"
    df = df[["lat", "lon", "mag", "date", "country", "type"]]
    earthquakes.append(df.dropna(subset=["lat", "lon", "mag"]))

earthquakes_df = pd.concat(earthquakes)

# Load Tsunamis 
tsunamis = []
for country, file in tsunami_files.items():
    if not os.path.exists(file):
        print(f"Missing file: {file}")
        continue
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        "latitude": "lat",
        "longitude": "lon",
        "maximum water height (m)": "height",
        "earthquake magnitude": "mag"
    })
    df["country"] = country
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["height"] = pd.to_numeric(df["height"], errors="coerce")
    df["date"] = df.apply(parse_date, axis=1)
    df["type"] = "Tsunami"
    df = df[["lat", "lon", "height", "date", "country", "type"]]
    tsunamis.append(df.dropna(subset=["lat", "lon", "height"]))

tsunamis_df = pd.concat(tsunamis)

# Load Volcanoes
volcanoes = []
for country, file in volcano_files.items():
    if not os.path.exists(file):
        print(f"Missing file: {file}")
        continue
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
    df["country"] = country
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["vei"] = pd.to_numeric(df["vei"], errors="coerce")
    df["date"] = df.apply(parse_date, axis=1)
    df["type"] = "Volcano"
    df = df[["lat", "lon", "vei", "date", "country", "type"]]
    volcanoes.append(df.dropna(subset=["lat", "lon", "vei"]))

volcanoes_df = pd.concat(volcanoes)

# Create the map 
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

# Earthquake markers
for _, row in earthquakes_df.iterrows():
    color = 'red' if row['mag'] >= 7 else 'green'
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(f"""
            <b>Type:</b> Earthquake<br>
            <b>Country:</b> {row['country']}<br>
            <b>Date:</b> {row['date'].date() if pd.notnull(row['date']) else 'Unknown'}<br>
            <b>Magnitude:</b> {row['mag']}
        """, max_width=300)
    ).add_to(m)

# Tsunami markers
for _, row in tsunamis_df.iterrows():
    color = '#00008B' if row['height'] >= 30 else '#ADD8E6'
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(f"""
            <b>Type:</b> Tsunami<br>
            <b>Country:</b> {row['country']}<br>
            <b>Date:</b> {row['date'].date() if pd.notnull(row['date']) else 'Unknown'}<br>
            <b>Wave Height:</b> {row['height']} m
        """, max_width=300)
    ).add_to(m)

# Volcano markers 
for _, row in volcanoes_df.iterrows():
    color = '#FF8C00' if row['vei'] >= 4 else '#FFD580'  # Dark orange / light orange
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=folium.Popup(f"""
            <b>Type:</b> Volcano<br>
            <b>Country:</b> {row['country']}<br>
            <b>Date:</b> {row['date'].date() if pd.notnull(row['date']) else 'Unknown'}<br>
            <b>VEI:</b> {row['vei']}
        """, max_width=300)
    ).add_to(m)

# Updated Natural Disasters 
natural_disasters_html = '''
<div style="
    position: fixed; 
    bottom: 20px; left: 20px; width: 250px; 
    background-color: white; 
    border: 2px solid grey; 
    padding: 10px; 
    font-size: 14px;
    z-index: 9999;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    border-radius: 5px;">
    <b>Natural Disasters</b><br>
    <u>Earthquakes</u><br>
    <span style="color:red;">●</span> Magnitude ≥ 7.0<br>
    <span style="color:green;">●</span> Magnitude &lt; 7.0<br>
    <u>Tsunamis</u><br>
    <span style="color:#00008B;">●</span> Height ≥ 30 m<br>
    <span style="color:#ADD8E6;">●</span> Height &lt; 30 m<br>
    <u>Volcanoes</u><br>
    <span style="color:#FF8C00;">●</span> VEI ≥ 4<br>
    <span style="color:#FFD580;">●</span> VEI &lt; 4
</div>
'''
m.get_root().html.add_child(folium.Element(natural_disasters_html))

# Save to HTML
m.save("interactive_map.html")
print("Map saved to: interactive_map.html")