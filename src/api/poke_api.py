import requests
import json

POKEMON_API = 'https://pokeapi.co/api/v2/pokemon/%s'
RAW_DATA_PATH = 'raw_data/%s'
RAW_FILE_TEMPLATE = "%s.json"

MOVE_FILE_PATH = "moves.json"
# All gen 1 and gen 2 moves
MOVES_API = "https://pokeapi.co/api/v2/move?limit=801"

EVOLUTION_CHAIN_CSV = "evolution.csv"
EVOLUTION_CHAIN_API = "https://pokeapi.co/api/v2/evolution-chain/%s"

class RequestException(Exception):
    '''
    Request exited with non 200 status code.
    '''


def get_pokemon(id):
    '''
    Fetch and Save the pokemon data for the given ID.
    :param id int: the ID of the pokemon.
    :return: None 
    :rtype: None
    '''
    response = requests.get(POKEMON_API % id)

    if (response.status_code != 200): raise RequestException()
    json_response = response.json()
    pokemon_name = json_response['id']

    with open(RAW_DATA_PATH % (RAW_FILE_TEMPLATE % pokemon_name), 'w') as raw_data_file:
        raw_data_file.write(json.dumps(json_response))



def get_moves():
    '''
    Get the list of moves for all pokemon
    '''
    response = requests.get(MOVES_API)
    json_response = response.json()['results']
    moves = [{'name': v['name'], 'id': int(v['url'].split('/')[-2])} for v in json_response]

    with open(MOVE_FILE_PATH, 'w') as raw_moves_file:
        raw_moves_file.write(json.dumps(moves))


def get_evolution_chains(id):
    '''
    Get the evolution chain for the given evolution ID.
    :param id int: the ID of the evolution chain.
    :return: A list of tuples of which pokemon evolve into other Pokemon (by IDs).
    :rtype: list[tuple]
    '''
    response = requests.get(EVOLUTION_CHAIN_API % id)
    if (response.status_code != 200): raise RequestException()
    json_response = response.json()

    def get_id_from_url(url):
        return url.split('/')[-2]

    def extract_evolution_detail(poke_json):
        species = poke_json['species']
        poke_index = get_id_from_url(species['url'])
        evolution_array = poke_json['evolves_to']
        to_evolution = [(poke_index, get_id_from_url(evol['species']['url'])) for evol in evolution_array]
        rec_evol = [detail for evol in evolution_array for detail in extract_evolution_detail(evol)]
        return to_evolution + rec_evol

    return extract_evolution_detail(json_response['chain'])