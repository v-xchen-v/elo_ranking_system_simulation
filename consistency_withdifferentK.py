from arena_data.arena_helper import get_arena_battles_data, get_arena_battles_models
from llm_player import LLMPlayer
import pandas as pd
import numpy as np
from pairwise_rating_entity import PairwiseRatingEntity, PairwiseBattleScore
import matplotlib.pyplot as plt

llm_players = {x: LLMPlayer(x) for x in get_arena_battles_models()}
print(llm_players)

arena_battles_data = get_arena_battles_data()

# shared test logics
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
        df['Rank'] = df['Elo Rating'].rank(ascending=False)
        
        return df
Ks = [4, 8, 16, 32]
dfs = [do_arena_battle(k) for k in Ks]

cm = plt.get_cmap('gist_rainbow')
colors = cm(np.linspace(0, 1.0, len(dfs)))
    
target='Rank'
# target='Elo Rating'
for idx, df in enumerate(dfs):
    if idx == 0:
        ax1 = df.plot.scatter(x='Model', y=target, c=colors[idx], label=f'K={Ks[idx]}')
    else:
        ax1 = df.plot.scatter(x='Model', y=target, c=colors[idx], ax=ax1, label=f'K={Ks[idx]}')
if target =='Rank':
    ax1.set_ylim(ax1.get_ylim()[::-1])
else:
    ax1.set_ylim(ax1.get_ylim())
fig = ax1.get_figure()
fig.set_size_inches(15, 5)
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.xticks(rotation=65)
plt.xticks(fontsize=8)
plt.subplots_adjust(bottom=0.15) 
plt.tight_layout()
plt.savefig(f'{target}_consistency_withdifferentK.png')