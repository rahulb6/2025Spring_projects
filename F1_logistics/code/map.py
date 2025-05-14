import folium
from gen_circuit_details import circuits

if __name__ == "__main__":
    # Create the map
    f1_map = folium.Map(location=[10, 20], zoom_start=2, tiles="CartoDB positron")

    # Coordinates for the connecting line
    coordinates = []

    # Add markers with number + name + date in same box
    for idx, (name, lat, lon, _, date) in enumerate(circuits, start=1):
        coordinates.append((lat, lon))

        folium.map.Marker(
            [lat + 0.25, lon + 0.25],  # Offset so it doesn't overlap the line
            icon=folium.DivIcon(
                html=f"""
                    <div style="
                        font-size:12px;
                        color:black;
                        background-color:white;
                        border:1px solid grey;
                        border-radius:6px;
                        padding:3px;
                        width:150px;
                        line-height:1.4;
                        box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
                        white-space: normal;
                        word-wrap: break-word;
                        ">
                        <b style='color:red;'>#{idx}</b><br>
                        <span>{name}</span><br>
                        <span>{date}</span>
                    </div>
                """
            )
        ).add_to(f1_map)

    # Draw polyline to connect all races
    folium.PolyLine(
        coordinates,
        color="green",
        weight=2.5,
        opacity=0.8
    ).add_to(f1_map)

    # Save the map
    f1_map.save("f1_2025_clean_map.html")
    print("Map saved as f1_2025_clean_map.html in the folder where this program exists. open in browser to view.")

