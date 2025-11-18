from FlightRadar24 import FlightRadar24API
import math

fr_api = FlightRadar24API()
mylat = 50.065930370814804
mylong = 8.785707202354097
tree_line = 10

# bounds = fr_api.get_bounds_by_point(42.446245283368356, -71.41279003817982, 15000)
bounds = fr_api.get_bounds_by_point(mylat, mylong, 10000)

flights = fr_api.get_flights(bounds=bounds)

def distance(data):
    lat_plane = data[0]
    long_plane = data[1]
    R = 6371.0
    phi1 = math.radians(lat_plane)
    phi2 = math.radians(mylat)
    delta_phi = math.radians(mylat - lat_plane)
    delta_lambda = math.radians(mylong - long_plane)
    a = (math.sin(delta_phi / 2) ** 2) + \
        (math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2) ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def above_trees(distance_km, altitude, treeline):

    if altitude == 0:
        return False
    if math.radians(treeline) < math.tan(altitude/distance_km):
         return True
    else:
        return False

def get_details(flight_details):
    current_data = flight_details['trail'][0]
    latitude = current_data.get('lat')
    longitude = current_data.get('lng')
    altitude = current_data.get('alt')
    altitude_test = altitude/3280.84
    data = [latitude,longitude]

    try:
        flight_number = flight_details['identification']['number']['default']
    except TypeError or KeyError:
        flight_number = "Unknown"
    try:
        airline_name = flight_details['airline']['name']
    except TypeError or KeyError:
        airline_name = "Unknown"
    try:
        plane_type = flight_details['aircraft']['model']['text']
    except TypeError or KeyError:
        plane_type = "Unknown"

    try:
        destination = flight_details['airport']['destination']['name']
    except TypeError or KeyError:
        destination = "Unknown"
    try:
        origin = flight_details['airport']['origin']['name']
    except TypeError or KeyError:
        origin = "Unknown"


    distance_km = distance(data)

    if not above_trees(distance_km, altitude_test, tree_line):
        return False, distance_km
    if above_trees(distance_km, altitude_test, tree_line):
        distance_km = distance_km * 10
        distance_km = math.trunc(distance_km)
        distance_km = distance_km/10

        return True, distance_km, altitude, flight_number, airline_name, plane_type, destination, origin
    


def main(): 
    no_counter = 0  
    print()  
    for i in range(len(flights)):
            flight_details = fr_api.get_flight_details(flights[i])
            deets = get_details(flight_details)
            info_tags = ["Distance(km):", "Elevation(ft):", "Flight Number:", "Airline:", "Plane Type:", "Destination:", "Origin:"]
            if deets[0]:
                    for i in range(1,8):
                        print(info_tags[i-1], deets[i])
                    print()
            else:
                no_counter+=1

    if no_counter == len(flights):
        print("No planes around :( \nCheck again later!\n")

           
main()