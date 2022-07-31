""" This module showcase that how can we use generators to efficiently loop over resources.
"""
from pprint import pprint
from typing import Dict, List, Any
import httpx


def get_pokemon_all_abilities(endpoint_url):
    """This function is used to generate a page of pokemons containing name and urls for ability


    Args:
        endpoint_url (str): url for ability endpoint containing offset and limit

    Raises:
        httpx.RequestError: if request produce status code other than 200

    Returns:
        resonse dictionary
    """
    try:
        req = httpx.get(endpoint_url)
        return req.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
        raise exc


def get_ability(res: List[Any]):
    """produce generator for given list object of ability urls

    Args:
        res (List[Any]): list object of ability urls

    Yields:
        generator for given list object of ability urls
    """
    for item in res:
        print(f"name: {item.get('name')} url: {item.get('url')}")
        try:
            ability = httpx.get(item.get("url"))
            yield ability
        except httpx.RequestError:
            print("invalid request")
            continue


def main():
    """main function which serves a starting point"""
    initial_offeset = 0
    initial_limit = 20
    endpoint_url = f"https://pokeapi.co/api/v2/ability/?offset={initial_offeset}&limit={initial_limit}"
    while True:
        res: Dict = get_pokemon_all_abilities(endpoint_url)
        next: str = res.get("next")
        ability_response = get_ability(res.get("results"))
        for ability in ability_response:
            pprint(ability.json())
        if next is not None:
            endpoint_url = next
        else:
            break


if __name__ == "__main__":
    main()
