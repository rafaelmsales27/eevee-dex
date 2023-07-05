from flask import Flask, render_template, request, redirect, url_for, flash ,session
from flask_session import Session
import requests
import random
import json

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

BASE_URL = 'https://pokeapi.co/api/v2/pokemon/'

# Define query API funciont
def pokequery(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code != 200 or response == None:
            print('ERROR???????????????????????????????????????????????????????????????????')
            return render_template('error.html', top=response.status_code, bottom='Something went wrong')
        else:
            return response
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
    
# Query to know number of pokemons on PokeAPI    
MAX_N = pokequery(BASE_URL)
MAX_N = MAX_N.json()
MAX_N = int(MAX_N['count'])
POKEDEX_PER_PAGE = 21

@app.route('/')
def index():

    # Start emmpty list to get results from PokeAPI
    list_of_poke = []

    # Choose a starter for the pokemon colection that will be displayed in index.html
    random_start = random.randint(0,(MAX_N - 6))

    # Query API and record starter info into the first position of empty list
    r = pokequery(BASE_URL + str(random_start))

    # Get data to json
    print(r)
    print(random_start)

    if r is None:
        # Get data to json
        # print('ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # return render_template('error.html', top='200', bottom='Something went wrong')
        # Read the JSON file
        with open('static/default.json') as file:
            json_data = json.load(file)

        # Convert JSON data to a dictionary
        data_dict = dict(json_data)
        list_of_poke.append(data_dict)
        return render_template('index.html', list_poke = list_of_poke)
    
    data = r.json()
    id_start = data['id']
    id_start = int(id_start)
    
    list_of_poke.append(data)

    for x in range(1,5):
        id_start += 1
        list_of_poke.append((requests.get(BASE_URL + str(id_start))).json())

    return render_template('index.html', list_poke = list_of_poke)


@app.route('/details')
def details():
    """Show result of search pokemon."""
    name = request.args["search"].lower()
    print(name)
    error = None

    if (name is None) or (name == ''):
        error = "Empty search entry."
        flash(error)
        # return render_template('error.html', top=response.status_code, bottom=error)
        return redirect(url_for('index'))
    elif len(name.split()) > 1:
        error = 'You searched more than one word.'
        flash(error)
        return redirect(url_for('index'))
    elif name.isnumeric() and not (int(name) > 0 and int(name) <= MAX_N):
        error = 'Invalid pokemon name or ID.'
        flash(error)
        return redirect(url_for('index'))

    print(name)

    if error is None:
        # Query pokeAPI
        search_url = BASE_URL + name
        response = pokequery(search_url)
        # If response is empty show flash message and return to index
        if response is None:
            flash('No pokemon was found.')
            return redirect(url_for('index'))
        resp_json = response.json()

        return render_template('details.html', pokemon_data = resp_json)
    flash(error)


@app.route('/pokedex')
def pokedex():
    # Query API and record starter info into the first position of empty list
    r = pokequery(BASE_URL + '?offset=0&limit='+str(POKEDEX_PER_PAGE)).json()

    # Start emmpty list to get results from PokeAPI
    pokedex_content = [r]

    # Define number of pages
    n_pokes = int(r['count'])
    n_pages = int(n_pokes / POKEDEX_PER_PAGE)

    # Get page number from GET argument
    current_page = request.args['page']
    if current_page or current_page.isdigit():
        current_page = int(current_page)
    else:
        current_page = 1

        
    return render_template('pokedex.html', content=pokedex_content, current_page=current_page, per_page=POKEDEX_PER_PAGE, n_pages=n_pages)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
  app.run()