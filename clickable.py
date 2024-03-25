# %%
import folium
from branca.element import Figure

# Create a new map centered at some location
m = folium.Map(
    location=[-33.91611178427029, 151.2636983190627],
    zoom_start=17,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Esri Satellite",
)

# Create a new Figure, add the map to it
fig = Figure()
fig.add_child(m)

# Add a click marker functionality
m.add_child(folium.ClickForMarker(popup="Coordinates"))

# Add custom JavaScript
custom_js = """
<script>
window.addEventListener("load", (event) => {
    console.log("page is fully loaded");
    var mapDiv = document.querySelector(".folium-map");
    var map = L.map(mapDiv.id).setView([51.505, -0.09], 13);
    mapDiv.dataset.map = map;
    map.whenReady(function() {
        map.on('click', function(e) {
            console.log("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng)
        });
    });
});
</script>
"""
fig.get_root().header.add_child(folium.Element(custom_js))
# Save it to a file
fig.save("clickmap.html")

print("done")
