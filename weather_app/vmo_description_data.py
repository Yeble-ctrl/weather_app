from pathlib import Path
import json

def getVmoDataDesc():
    """Function for getting VMO Data descriptions"""
    path = Path("weather_app/descriptions.json")
    contents = Path.read_text(path)
    vmo_description_data = json.loads(contents)

    # Add the url path to the corresponding weather symbol
    for desc in vmo_description_data.values():
        desc["day"]["image"] = (f'airy/{desc["day"]["description"]}.png').replace(" ", "-").lower()
        desc["night"]["image"] = (f'airy/{desc["day"]["description"]}.png').replace(" ", "-").lower()

    return vmo_description_data

VMO_DESCRIPTION_DATA = getVmoDataDesc()