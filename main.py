from game import MasterMind
from agent import NaiveAgent
from dotenv import load_dotenv
import os
import random

load_dotenv()

COLORS = os.getenv("COLORS")
VOID_CHAR = os.getenv("VOID_CHAR")
LEVEL_KEY = os.getenv("LEVEL_KEY")

levels = {
    "medium": [8, 6, 4],
    "difficult": [12, 6, 5]
}

def play(game, agent=None):
    attempt = ''
    for i in range(game.attempts):
        # Agent move
        if not agent is None:
            attempt = agent.guess(game.history, remember=False)
            print(f"Agent move: {attempt}")
        # Player move
        else:
            print(f"Attempt: {len(game.history['attempts']) + 1}/{game.attempts}")
            while not game.is_valid(attempt):
                attempt = input(f"Colors: {game.colors}\nFind a solution of length {len(game.solution)}: ")
            if attempt == 'help':
                attempt = random.sample(game.possibilities, 1)[0]
                print(f"Word chosen automatically: {attempt}")
        # Apply move
        p, c = game.move(attempt)
        print(f"Perfects: {p}\nCorrects: {c}\n")
        if game.win():
            break
        attempt = ''
    if len(game.history["attempts"]) < game.attempts:
        print(f"Solution {game.solution} was founded in {len(game.history['attempts'])}/{game.attempts} attempts.")
    else:
        print(f"Fail, solution was {game.solution}")


if __name__ == "__main__":
    # Game
    game = MasterMind(*levels[LEVEL_KEY])
    game.set_solution()
    # Agent
    agent = NaiveAgent(*levels[LEVEL_KEY][1:])
    # Play
    play(game, agent)
    # Show results
    print(game)
