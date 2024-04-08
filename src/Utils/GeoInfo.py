import requests
import folium

def execute_get_request(endpoint, parameters = {}):
    """
    Performs a GET request to the specified endpoint with the given parameters.

    :param endpoint: The URL endpoint to send the GET request to.
    :param parameters: A dictionary of parameters to include in the request.
    :return: The response from the GET request.

    # Example usage:
    endpoint = "https://api.example.com/data"
    parameters = {"param1": "value1", "param2": "value2"}
    """

    try:
        response = requests.get(endpoint, params=parameters)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        return response.json()  # Returns the json-encoded content of a response, if any.
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}  # Return error message in case of exception


def getCoordinatesFromAdresse(adresse:str,city_name = None):
    if city_name is not None:
        adresse = adresse + " " + city_name
    adresseAPI_endpoint = "https://api-adresse.data.gouv.fr/search/"
    adresseAPI_parameters = {
        "q":adresse,
        "limit" : "1"
    }

    response = execute_get_request(adresseAPI_endpoint, adresseAPI_parameters)['features'][0]

    coordinates = response['geometry']['coordinates']

    return coordinates

def plotFromCoordinates(coordinates):
    # Create a map centered around France
    map = folium.Map(location=[46.2276, 2.2137], zoom_start=6)

    # Add the point to the map
    folium.Marker(location=[coordinates[1], coordinates[0]],
              popup='location').add_to(map)

    # Display the map
    return map

def geoInfoPipeline(adresse:str,city_name = None):
    if city_name is not None:
        coordinates = getCoordinatesFromAdresse(adresse,city_name)
    else:
        coordinates = getCoordinatesFromAdresse(adresse)
    print(coordinates)
    
    return plotFromCoordinates(coordinates)





# FUNCTIONS BELLOW ARE DEPRECATED BUT KEPT IN CODE BASE JUST IN CASE 

def checkCommuneNamesWithMistral(town1,town2):
    api_key = "XosGJQnnWzLLAJjNU7FLJb1p8WVc2ZdM"
    model = "mistral-small-latest"

    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(role="system", content="Are these two french towns name the same? Answer with just True or False and under no circompstances do not provide further explainations."),
        ChatMessage(role="user", content="town name 1 = "+ town1 +" ; town name 2 = " + town2 )
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
        max_tokens = 1
    )
    return chat_response.choices[0].message.content


def name2postcode(city_name:str,df, top_n=5,column_name='nom_commune_complet'):
    # Try direct match
    closest_rows = df[df[column_name].isin([city_name]) | df[column_name].str.contains(city_name, case=False) ]

    if len(closest_rows) != 0:
        print("Direct match")
    else:
        print("No direct match, looking for similarities")
        # Calculer la similarité et trier les résultats
        similarities = process.extract(city_name, df[column_name], limit=top_n)
    
        # Extraire les noms des villes les plus similaires
        closest_cities = [similarity[0] for similarity in similarities]
    
        # Sélectionner les lignes correspondantes dans le DataFrame
        closest_rows = df[df[column_name].isin(closest_cities)]

    result = []

    for i in range(len(closest_rows)):
        check = checkCommuneNamesWithMistral(city_name,closest_rows.iloc[i]['nom_commune_complet'])
        if check == 'True':
            result.append(closest_rows.iloc[i])
        
    return result














