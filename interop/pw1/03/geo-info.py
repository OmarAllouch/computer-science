import csv
import math

def haversine(lat1, lon1, lat2, lon2):
    """Function to calculate the distance between two points on the Earth's surface using the Haversine formula
    Generated by ChatGPT to avoid using external libraries"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371
    return r * c

def load_admin1(file_path='03/admin1CodesASCII.txt'):
    admin1 = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            code = row[0]
            name = row[1]
            admin1[code] = name
    return admin1 # FIPS code to name

def load_admin2(file_path='03/admin2Codes.txt'):
    admin2 = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            code = row[0]
            name = row[1]
            admin2[code] = name
    return admin2 # FIPS code to name

def load_france_places(file_path='03/FR/FR.txt'):
    places = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) > 14:
                geonameid = row[0]
                name = row[1]
                lat, lon = float(row[4]), float(row[5])
                feature_code = row[7]
                admin1_code = row[10]
                admin2_code = row[11]
                population = int(row[14]) if row[14] else 0
                places.append({'id': geonameid, 'name': name, 'coords': (lat, lon), 
                               'feature_code': feature_code, 'admin1_code': admin1_code, 
                               'admin2_code': admin2_code, 'population': population})
    return places

def find_closest_airport(lat, lon, places):
    airports = [p for p in places if p['feature_code'] == 'AIRP'] # AIRP is the feature code for airports (per the docs)
    closest_airport = min(airports, key=lambda x: haversine(lat, lon, x['coords'][0], x['coords'][1]))
    airport_name = closest_airport['name']
    distance = round(haversine(lat, lon, closest_airport['coords'][0], closest_airport['coords'][1]), 2)
    return airport_name, distance

def find_closest_cities(lat, lon, places):
    cities = [p for p in places if p['feature_code'] == "PPL"] # PPL is the feature code for a city, town, village, or other agglomeration of buildings where people live and work (per the docs)
    sorted_cities = sorted(cities, key=lambda x: haversine(lat, lon, x['coords'][0], x['coords'][1]))
    return sorted_cities[:5]

places = [
    "Gare de Saint-Étienne-Châteaucreux",
    "Gare de Lyon-Part-Dieu",
]

def display_places(places):
    print("Select a place by entering its number:")
    for i, place in enumerate(places, start=1):
        print(f"{i}. {place}")

def get_user_selection(places):
    display_places(places)
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(places):
                return places[choice - 1]
            else:
                print("Invalid selection. Please choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Load data
    admin1 = load_admin1()
    admin2 = load_admin2()
    france_places = load_france_places()

    # Example
    selected_place = get_user_selection(places)
    place_name = selected_place
    place_lat, place_lon = 0, 0
    for place in france_places:
        if place['name'] == place_name:
            place_lat, place_lon = place['coords']
            print(f"Location: {place_name}, Latitude: {place_lat}, Longitude: {place_lon}")
            break

    # Closest airport
    airport_name, airport_distance = find_closest_airport(place_lat, place_lon, france_places)
    print(f"Closest Airport: {airport_name}, Distance: {airport_distance} km")

    # FIPScode, admin Divisions, and population
    target_place = next((p for p in france_places if p['name'] == place_name), None)
    
    if target_place:
        admin1_display_name = admin1.get(f"FR.{target_place['admin1_code']}", "Unknown")
        admin2_display_name = admin2.get(f"FR.{target_place['admin1_code']}.{target_place['admin2_code']}", "Unknown")
        admin2_population = sum(p['population'] for p in france_places if p['admin2_code'] == target_place['admin2_code'])
        print(f"Admin1 Division: {admin1_display_name}")
        print(f"Admin2 Division: {admin2_display_name}, Population: {admin2_population}")

    # Closest cities
    closest_cities = find_closest_cities(place_lat, place_lon, france_places)
    print("Five Closest Cities:")
    for city in closest_cities:
        distance = round(haversine(place_lat, place_lon, city['coords'][0], city['coords'][1]), 2)
        print(f"  {city['name']} - {distance} km")

if __name__ == "__main__":
    main()
