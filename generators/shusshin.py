import json
import os
import random

from rikishi.models import Shusshin

DIRNAME = os.path.dirname(__file__)

JAPANESE_PROB = 0.88


def get_pref_probs():
    with open(os.path.join(DIRNAME, "data", "jp_pref_probs.json"), "r") as f:
        try:
            return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise Exception(
                "Failed to load file 'jp_pref_probs.json': " + str(e)
            ) from e


class ShusshinGenerator:
    def __init__(self) -> None:
        self.pref_probs = get_pref_probs()

    def get_japanese(self):
        population, weights = zip(*self.pref_probs.items(), strict=False)
        prefecture = random.choices(population=population, weights=weights)[0]
        return Shusshin(prefecture=prefecture)

    def get(self):
        # TODO : Add possibility to generate foreigners
        return self.get_japanese()
