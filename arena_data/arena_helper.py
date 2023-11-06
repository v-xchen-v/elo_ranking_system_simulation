# https://colab.research.google.com/drive/1RAWb22-PFNI-X1gPVzc927SGUdfr6nsR?usp=sharing#scrollTo=2IdpT27Q8IE_

import pandas as pd

filename = 'arena_data\clean_battle_20230717.json'
def get_arena_battles_data() -> pd.DataFrame:
    raw_data = pd.read_json(filename).sort_values(ascending=True, by=["tstamp"])
    # print(raw_data)

    # print("anony battle counts:", raw_data['anony'].value_counts())
    battles = raw_data[raw_data['anony']].reset_index(drop=True)
    # print(battles)
    return battles

def get_arena_battles_models() -> list[str]:
    raw_data = pd.read_json(filename).sort_values(ascending=True, by=["tstamp"])
    battles = raw_data[raw_data['anony']].reset_index(drop=True)
    models = pd.concat([battles['model_a'], battles['model_b']]).unique()
    return models

if __name__ == '__main__':    
    print(get_arena_battles_models())