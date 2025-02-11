import folium
import geopy.geocoders

geolocator = geopy.geocoders.Nominatim(user_agent="data_route_app")


def generate_map(data):
    addresses = [row[4] for row in data[1:] if row[4]]

    if not addresses:
        return None

    map_center = geolocator.geocode(addresses[0])
    if not map_center:
        return None

    my_map = folium.Map(location=[map_center.latitude, map_center.longitude], zoom_start=12)

    for address in addresses:
        location = geolocator.geocode(address)
        if location:
            folium.Marker(
                [location.latitude, location.longitude], popup=address
            ).add_to(my_map)

    map_file = "generated_map.html"
    my_map.save(map_file)
    return map_file
