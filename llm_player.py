from __future__ import annotations
from rating_entity import RatingEntity
from abc import ABC, abstractmethod

INITIAL_PLAYER_K = 4 #32
FINAL_PLAYER_K = 4 #16
INITIAL_LLMPLAYER_RATING = 1000

class Player(RatingEntity, ABC):
    """Represents a large language model which is a player with Elo rating.
    
    This class also defines a strategy to handle the evolution of the K factor.
    """
    def __init__(self, rating: float, K: int):
        super().__init__(rating, K)
        
    def update_K(self):
        """Define the strategy to evolve K over time."""
        # self.K = max(FINAL_PLAYER_K, self.K -1)
        # turn off K evolving temporally
        return self.K
    
class LLMPlayer(Player):
    def __init__(self, id: str, K: int = INITIAL_PLAYER_K):
        self.id = id
        super().__init__(INITIAL_LLMPLAYER_RATING, K)
            
    def __str__(self):
        return f'model_id:{self.id} rating:{self.rating}'
    
    def __repr__(self) -> str:
        return f'model_id:{self.id} rating:{self.rating}'