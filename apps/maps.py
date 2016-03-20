""" Get transit directions via Google Maps. """

import requests



def pretty_directions(city, start, destination):
    """pretty_directions(string, string, string) -> string

    Returns a string with step-by-step transit directions from
    start to destination in the given city, or a description of
    the error that occured.
    """
    try:
        result = get_directions(city, start, destination)
    except requests.exceptions.ConnectionError:
        result = "Sorry, couldn't connect to Google Maps."
    except LocationError:
        template = "Sorry, couldn't get directions from {start} to {dest} in {city}."
        result = template.format(start=start, dest=destination, city=city)
    return result



def get_directions(city, origin, destination):
    """
    route JSON example at:
    https://maps.googleapis.com/maps/api/directions/json?
    origin=Centrum,Warsaw,Poland&destination=Plac+Zbawiciela,
    Warsaw,Poland&mode=transit
    """

    url="https://maps.googleapis.com/maps/api/directions/json?origin="+origin+","+city+",Poland&destination="+destination+","+city+",Poland&mode=transit"


    google_maps_raw=requests.get(url)
    google_maps_json=google_maps_raw.json()

    all_instructions="Your directions are:\t"

    if google_maps_json["geocoded_waypoints"][0]["geocoder_status"]=="OK":
        step_number=0
        steps_amount=len(google_maps_json["routes"][0]["legs"][0]["steps"])

        while(step_number<steps_amount):
            for item in google_maps_json["routes"][0]["legs"][0]["steps"][step_number]:
                if item=="html_instructions":
                    instruction=google_maps_json["routes"][0]["legs"][0]["steps"][step_number]["html_instructions"].lower()
                    path=google_maps_json["routes"][0]["legs"][0]["steps"][step_number]
                    if "walk" in instruction:
                        all_instructions = all_instructions + "\n" + path["html_instructions"]+""+"("+path["distance"]["text"]+")"
                    elif "tram" in instruction or "bus" in instruction or "subway" in instruction:
                        all_instructions = all_instructions + "\n" + path["html_instructions"]
                        all_instructions = all_instructions + "\n" + "\tLine: "+path["transit_details"]["line"]["short_name"]
                        all_instructions = all_instructions + "\n" + "\tFrom: "+path["transit_details"]["departure_stop"]["name"]
                        all_instructions = all_instructions + "\n" + "\tTo: "+path["transit_details"]["arrival_stop"]["name"]
                    else:
                        print (instruction)
            step_number=step_number+1
    else:
        raise LocationError
        
    return all_instructions

    #for item in google_maps_json["geocoded_waypoints"][0]["geocoder_status"]:
    #    print (item)


class LocationError(Exception):
    pass