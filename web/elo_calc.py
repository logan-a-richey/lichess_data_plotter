import math

def update_elo(
    rating_a: int, 
    rating_b: int, 
    result: float,  
    k_factor: int = 10
) -> float:
    """
    Updates the Elo ratings for two players based on a match result.

    Args:
        rating_a (int): The current Elo rating of player A.
        rating_b (int): The current Elo rating of player B.
        k_factor (int): The maximum rating change possible (e.g., 32 for chess).
        result (str): The outcome of the match from player A's perspective.
                      'win' for a win, 'loss' for a loss, or 'draw' for a tie.

    Returns:
        tuple: A tuple containing the new ratings for player A and player B.
    """
    # Step 1: Calculate the expected scores for each player.
    expected_a = 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))
    expected_b = 1 / (1 + math.pow(10, (rating_a - rating_b) / 400))

    # Step 2: Determine the actual score based on the match result.
    if result == 'win':
        score_a = 1
        score_b = 0
    elif result == 'loss':
        score_a = 0
        score_b = 1
    elif result == 'draw':
        score_a = 0.5
        score_b = 0.5
    else:
        raise ValueError("Invalid result. Use 'win', 'loss', or 'draw'.")

    # Step 3: Calculate the new ratings.
    new_rating_a = rating_a + k_factor * (score_a - expected_a)
    new_rating_b = rating_b + k_factor * (score_b - expected_b)
    
    return round(new_rating_a), round(new_rating_b)
