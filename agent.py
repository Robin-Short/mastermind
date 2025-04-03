import random
import itertools
from tqdm import tqdm
from dotenv import load_dotenv
import os
from utils import get_perfects, get_corrects

load_dotenv()

COLORS = os.getenv("COLORS")
VOID_CHAR = os.getenv("VOID_CHAR")

class NaiveAgent:
    def __init__(self, colors=6, solution_length=4):
        self.colors = COLORS[:colors]
        self.solution_length = solution_length
        self.possibilities = []
        self.initialize_possibilities()

    def initialize_possibilities(self):
        self.possibilities = []
        for p in itertools.product(self.colors, repeat=self.solution_length):
            self.possibilities.append(''.join(p))

    def filter_possibilities(self, condition, perfects, corrects, progress_bar=False):
        new_possibilities = []
        iterable = tqdm(self.possibilities, "Calculating possibilities") if progress_bar else self.possibilities
        for possibility in iterable:
            _c, _p = get_corrects(condition, possibility), get_perfects(condition, possibility)
            if _c == corrects and _p == perfects:
                new_possibilities.append(possibility)
        self.possibilities = new_possibilities

    def guess(self, history, remember=False):
        if not remember:
            self.initialize_possibilities()
            iterable = enumerate(history['attempts'])
        else:
            iterable = (len(history['attempts']) - 1, [history['attempts'][-1]]) if history['attempts'] else []
        for i, attempt in iterable:
            perfects, corrects = history['perfects'][i], history['corrects'][i]
            self.filter_possibilities(attempt, perfects, corrects)
        return random.sample(self.possibilities, 1)[0]
