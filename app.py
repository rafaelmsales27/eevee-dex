from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')



# base_url = 'https://pokeapi.co/api/v2/pokemon/'

# endpoint = 'eevee'

# r = requests.get(base_url + endpoint)

# data = r.json()

# sprite_front = data['sprites']['other']['official-artwork']['front_default']

# print(sprite_front)