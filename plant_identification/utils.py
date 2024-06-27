import requests


import base64

# plant_identification/utils.py

import base64

def get_image_data(image):
    # Read the content of the uploaded image
    image_data = image.read()
    
    # Encode the image data to base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    return image_base64


def identify_plant(image_data, api_key):
    # Plant.id API endpoint URL
    endpoint_url = 'https://api.plant.id/v2/identify'

    try:
        # Set up the request headers and parameters
        headers = {
            'Api-Key': api_key
        }
        files = {
            'images': ('image.jpg', image_data, 'image/jpeg')
        }
        params = {
            'includeDetails': 'true'  # Include detailed identification results
        }

        # Send a POST request to the Plant.id API for plant identification
        response = requests.post(endpoint_url, headers=headers, files=files, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract plant identification details
        if 'suggestions' in data:
            suggestions = data['suggestions']
            if suggestions:
                # Extract the first suggested plant species name
                plant_name = suggestions[0]['plant_name']
                # Extract one-line description if available
                description = " "
                if 'species' in suggestions[0]:
                    species_data = suggestions[0]['species']
                    if 'common_name' in species_data:
                        description = species_data['common_name']
                
                # Search Wikipedia for articles related to the plant species
                wikipedia_description = search_wikipedia(plant_name)
                if wikipedia_description:
                # Split the description into sentences
                    sentences = wikipedia_description.split('. ')
                # Keep only the first 5 to 6 sentences
                    wikipedia_description = '. '.join(sentences[:6]) 
                
                return f"{plant_name} Leaf {description}", wikipedia_description

            else:
                return "Unknown Plant", None
        else:
            return "Unknown Plant", None
    except Exception as e:
        print(f"Error identifying plant: {e}")
        return "Unknown Plant", None

def search_wikipedia(query):
    # Wikipedia API endpoint URL for search
    endpoint_url = 'https://en.wikipedia.org/w/api.php'

    try:
        # Set up the request parameters
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'exintro': True,  # Retrieve only the introductory section
            'explaintext': True,  # Return plain text instead of HTML
            'titles': query
        }

        # Send a GET request to the Wikipedia API for search
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract the page content (introductory section)
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            # Find the first page (there should be only one)
            page_id = list(pages.keys())[0]
            page_data = pages[page_id]
            if 'extract' in page_data:
                return page_data['extract']
        return None
    except Exception as e:
        print(f"Error searching Wikipedia: {e}")
        return None
