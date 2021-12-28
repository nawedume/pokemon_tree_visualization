from flask import Flask, render_template, request, Blueprint
import json
import pandas as pd
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.dirname(dir_path) + "/data/%s"
pokemon_info = pd.read_csv(DATA_PATH % 'pokemon_all_info.csv', header=None)
bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route("/")
def main():
    '''
    Render the main template.
    '''
    return render_template('index.html')


@bp.route("/get_tree_data")
def get_tree_data():
    '''
    Return the tree data for the visualization.
    '''
    with open(DATA_PATH % 'tree_data.json', 'r') as f:
        return json.load(f)


@bp.route("/get_poke_data/<poke_id>")
def get_pokemon_data(poke_id):
    '''
    Return the pokemon information for the given pokemon ID.
    '''
    with open(DATA_PATH % '%s.json' % poke_id, 'r') as f:
        return json.load(f)

@bp.route("/get_filtered_ids", methods=["POST"])
def get_filtered_ids():
    '''
    Get the IDs for the requested filters.
    poke_ids: The pokemon IDs which to filter for.
    type_ids: The type of pokemon to filter for.
    move_ids: The moves of pokemon to filter for.
    '''
    request_params = request.json
    poke_ids = request_params['poke_ids']
    type_ids = request_params['type_ids']
    move_ids = request_params['move_ids']

    completed_data = pokemon_info

    if (len(poke_ids) > 0):
        completed_data = completed_data[completed_data[1].isin(poke_ids)]

    if (len(type_ids) > 0):
        completed_data = completed_data[completed_data[3].isin(type_ids)
                                        | completed_data[4].isin(type_ids)]

    if (len(move_ids) > 0):
        sum_col = pokemon_info[move_ids[0] + 4]

        for i in range(1, len(move_ids)):
            move_id = move_ids[i]
            sum_col += pokemon_info[move_id + 4]

        completed_data = completed_data[sum_col > 0]

    return {'ids': list(completed_data[1])}


@bp.route("/get_meta_data")
def get_meta_data():

    pokemons = [[int(pokemon_info.loc[i][1]), pokemon_info.loc[i][2]]
                for i in range(pokemon_info.shape[0])]
    types = [
        'grass', 'fire', 'water', 'bug', 'normal', 'poison', 'electric',
        'ground', 'fairy', 'fighting', 'psychic', 'rock', 'ghost', 'ice',
        'dragon', 'dark', 'steel'
    ]

    with open(DATA_PATH % 'moves.json', 'r') as f:
        moves = json.load(f)

        return {
            'pokemons': pokemons,
            'types': types,
            'moves': moves
        } 


