import os
import geopandas as gpd
import folium
from folium import FeatureGroup

# Define the path to your GDB folder (assumes gdb file is in the current working directory)
gdb_path = os.path.join(os.getcwd(), 'HeatVulnerabilityFinal.gdb')  # Replace with the actual name of your GDB file

# Function to read GDB and create the web map
def create_map():
    # List all layers (feature classes) in the GDB
    layers = gpd.read_file(f'GDB://{gdb_path}')
    
    # Create a base map centered around a default location (e.g., San Francisco)
    map_center = [37.7749, -122.4194]  # Change to your desired center
    m = folium.Map(location=map_center, zoom_start=13)
    
    # Add a base layer (OpenStreetMap)
    folium.TileLayer('openstreetmap').add_to(m)

    # Loop over all layers and add them as separate layers on the map
    layer_groups = {}  # To store layer groups for each column
    for layer_name in layers.columns:
        # Create a FeatureGroup for each layer
        layer_group = FeatureGroup(name=layer_name)
        # Add this layer to the map (as GeoJSON)
        folium.GeoJson(layers[[layer_name]].to_json()).add_to(layer_group)
        # Add this layer to the map's layers dictionary
        layer_groups[layer_name] = layer_group

    # Add layer control to toggle layers
    folium.LayerControl().add_to(m)

    # Add all layers to the map (only one will be selectable at a time due to the LayerControl)
    for layer_group in layer_groups.values():
        layer_group.add_to(m)

    # Save the map to an HTML file
    m.save("webmap.html")

# Call the function to create the map
create_map()
