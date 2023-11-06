import unittest
from arena_data import get_arena_battles_data, get_arena_battles_models
from llm_player import LLMPlayer
from pairwise_rating_entity import PairwiseBattleScore, PairwiseRatingEntity
import pandas as pd
import math
import logging

logging.basicConfig(level=logging.INFO)

class TestEloRating(unittest.TestCase):
    def test_zerosum_withdifferentK(self):
        arena_battles_data = get_arena_battles_data()
            
        def do_arena_battle(K):
            llm_players = {x: LLMPlayer(x, K) for x in get_arena_battles_models()}
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

            df = pd.DataFrame([[n, llm_players[n].rating] for n in llm_players], columns=['Model', 'Elo Rating']).sort_values('Elo Rating', ascending=False).reset_index(drop=True)
            df.index = df.index+1
            
            return df
        
        def get_rating_sum(df: pd.DataFrame):
            rating_sum = df['Elo Rating'].sum()
            return rating_sum
        
        rating_sums = [get_rating_sum(do_arena_battle(k)) for k in [4, 8, 16, 32]]
        logging.info('rating sum:', rating_sums)
        
        # checking zero-sum of elo rating: {sum of rating} is consistant(n*initial rating) on different Ks
        self.assertTrue(all(math.isclose(x, rating_sums[0], rel_tol=0.1) for x in rating_sums))