from arena_data.arena_helper import get_arena_battles_data, get_arena_battles_models
from llm_player import LLMPlayer
import pandas as pd
import numpy as np
from pairwise_rating_entity import PairwiseRatingEntity, PairwiseBattleScore

llm_players = {x: LLMPlayer(x) for x in get_arena_battles_models()}
print(llm_players)

arena_battles_data = get_arena_battles_data()
for rd, model_a, model_b, winner in arena_battles_data[['model_a', 'model_b', 'winner']].itertuples():
    # print(rd, model_a, model_b, winner)
    model_a_player = llm_players[model_a]
    model_b_player = llm_players[model_b]
    
    battle_winner = None
    if winner == 'model_a':
        battle_winner = PairwiseBattleScore.WINNER_IS_A
    elif winner == 'model_b':
        battle_winner = PairwiseBattleScore.WINNER_IS_B
    else:
        battle_winner = PairwiseBattleScore.TIE
        
    PairwiseRatingEntity(model_a_player, model_b_player).battle(winner=battle_winner)

print(llm_players)
      
df = pd.DataFrame([[n, llm_players[n].rating] for n in llm_players], columns=['Model', 'Elo Rating']).sort_values('Elo Rating', ascending=False).reset_index(drop=True)
df.index = df.index+1
print('rating sum:', df['Elo Rating'].sum())
print(df)