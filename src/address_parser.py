from geopy.geocoders import Nominatim


def extract_addresses(data):
    """Extract address components from table data."""
    addresses = []
    headers = data[0]

    try:
        street_idx = headers.index("Straße / Hausnummer")
        postal_idx = headers.index("PLZ")
        city_idx = headers.index("Ort")
    except ValueError:
        return []

    for row in data[1:]:
        address = f"{row[street_idx]}, {row[postal_idx]} {row[city_idx]}"
        addresses.append(address)

    return addresses


def geocode_addresses(addresses):
    """Convert addresses to latitude/longitude using geopy."""
    geolocator = Nominatim(user_agent="geo_mapper")
    coordinates = []

    for address in addresses:
        location = geolocator.geocode(address)
        if location:
            coordinates.append((location.latitude, location.longitude, address))

    return coordinates
