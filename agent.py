import random
import itertools
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()

COLORS = os.getenv("COLORS")
VOID_CHAR = os.getenv("VOID_CHAR")

class Agent:
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
            _c, _p = self.get_corrects(condition, possibility), self.get_perfects(condition, possibility)
            if _c == corrects and _p == perfects:
                new_possibilities.append(possibility)
        self.possibilities = new_possibilities

    @staticmethod
    def get_perfects(attempt, solution):
        perfects = 0
        for i in range(len(solution)):
            if solution[i] == attempt[i]:
                perfects += 1
        return perfects

    @staticmethod
    def get_corrects(attempt, solution):
        perfects = Agent.get_perfects(attempt, solution)
        attempt = list(attempt)
        for i, x in enumerate(solution):
            for j, y in enumerate(attempt):
                if x == y:
                    attempt.pop(j)
                    break
        return len(solution) - len(attempt) - perfects

    def guess(self, history):
        self.initialize_possibilities()
        for i, attempt in enumerate(history['attempts']):
            perfects, corrects = history['perfects'][i], history['corrects'][i]
            self.filter_possibilities(attempt, perfects, corrects)
        return random.sample(self.possibilities, 1)[0]
