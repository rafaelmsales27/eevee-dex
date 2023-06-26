import requests

# base_url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}/"

base_url = 'https://pokeapi.co/api/v2/pokemon/'

endpoint = 'eevee'

r = requests.get(base_url + endpoint)

data = r.json()

sprite_front = data['sprites']['other']['official-artwork']['front_default']

print(sprite_front)