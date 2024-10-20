import requests

UNSPLASH_API_KEY = "F9EYXmwQEJ0fXZXpkjzx0mi_F8c9qgYhYC9qv7MWr1g"

# Unsplash API endpoint
UNSPLASH_API_URL = 'https://api.unsplash.com/search/photos'

def generate_image(name):
    # name[0].replace(' ','%20')
    response = requests.get(UNSPLASH_API_URL, 
                            params={'query': name, 'per_page': 1},
                            headers={'Authorization': f'Client-ID {UNSPLASH_API_KEY}'})
    data = response.json()

    # print(data.keys())
    return data['results'][0]['urls']['raw']

