import random
import itertools
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv("configure.env")

COLORS = os.getenv("COLORS")
VOID_CHAR = os.getenv("VOID_CHAR")

level = {
    "medium": [8, 6, 4],
    "difficult": [12, 6, 5]
}

class MasterMind:
    def __init__(self, attempts=8, colors=6, solution_length=4):
        self.attempts = attempts
        self.colors = COLORS[:colors]
        self.history = {
            "attempts": [],
            "perfects": [],
            "corrects": [],
            "num_of_possibilities": []
        }
        self.solution = VOID_CHAR * solution_length
        self.possibilities = []
        self.initialize_possibilities()

    def __str__(self):
        txt = f"Solution: {self.solution}\n"
        txt += f"Colors: {self.colors}\n"
        txt += f"Attempts: {self.history['attempts']}\n"
        txt += f"Perfects: {self.history['perfects']}\n"
        txt += f"Corrects: {self.history['corrects']}\n"
        txt += f"#Possibilities: {self.history['num_of_possibilities']}\n"
        txt += f"#Attempts: {len(self.history['attempts'])}/{self.attempts}\n"
        txt += f"Win: {self.win()}"
        return txt

    def initialize_possibilities(self):
        self.possibilities = []
        for p in itertools.product(self.colors, repeat=len(self.solution)):
            self.possibilities.append(''.join(p))
        self.history["num_of_possibilities"].append(len(self.possibilities))

    def filter_possibilities(self, condition=None, progress_bar=False):
        conditions = self.history["attempts"] if condition is None else [condition]
        new_possibilities = []
        iterable = tqdm(self.possibilities, "Calculating possibilities") if progress_bar else self.possibilities
        c, p = self.get_cor_perf()
        for possibility in iterable:
            for cond in conditions:
                _c, _p = self.get_corrects(cond, possibility), self.get_perfects(cond, possibility)
                if _c == c and _p == p:
                    new_possibilities.append(possibility)
        self.possibilities = new_possibilities

    def set_solution(self, solution=None):
        if solution is None:
            self.solution = ''.join(random.choices(self.colors, k=len(self.solution)))
        else:
            if len(self.solution) != len(solution):
                raise ValueError(f"Solution's length must be {len(self.solution)}: {solution}")
            self.solution = solution
    @staticmethod
    def get_perfects(attempt, solution):
        perfects = 0
        for i in range(len(solution)):
            if solution[i] == attempt[i]:
                perfects += 1
        return perfects

    @staticmethod
    def get_corrects(attempt, solution):
        perfects = MasterMind.get_perfects(attempt, solution)
        attempt = list(attempt)
        for i, x in enumerate(solution):
            for j, y in enumerate(attempt):
                if x == y:
                    attempt.pop(j)
                    break
        return len(solution) - len(attempt) - perfects

    def get_cor_perf(self):
        corrects = self.get_corrects(self.history["attempts"][-1], self.solution)
        perfects = self.get_perfects(self.history["attempts"][-1], self.solution)
        return corrects, perfects

    def move(self, attempt):
        perfects, corrects = self.get_perfects(attempt, self.solution), self.get_corrects(attempt, self.solution)
        self.history["attempts"].append(attempt)
        self.history["perfects"].append(perfects)
        self.history["corrects"].append(corrects)
        self.filter_possibilities(attempt)
        self.history["num_of_possibilities"].append(len(self.possibilities))
        return perfects, corrects

    def win(self):
        return self.history["attempts"][-1] == self.solution

    def play(self, automatic=False):
        attempt = ''
        for i in range(self.attempts):
            if automatic:
                attempt = 'auto'
            print(f"Attempt: {len(self.history['attempts']) + 1}/{self.attempts}")
            while not self.is_valid(attempt):
                attempt = input(f"Colors: {self.colors}\nFind a solution of length {len(self.solution)}: ")
            if attempt == 'auto':
                attempt = random.sample(self.possibilities, 1)[0]
                print(f"Word chosen automatically: {attempt}")
            self.move(attempt)
            c, p = self.get_cor_perf()
            print(f"Perfects: {p}\nCorrects: {c}\n")
            if self.win():
                break
            attempt = ''
        if len(self.history["attempts"]) < self.attempts:
            print(f"Solution {self.solution} was founded in {len(self.history['attempts'])}/{self.attempts} attempts.")
        else:
            print(f"Fail, solution was {self.solution}")

    def is_valid(self, attempt):
        if attempt == 'auto':
            return True
        if not isinstance(attempt, str):
            return False
        if len(attempt) != len(self.solution):
            return False
        for x in attempt:
            if not x in self.colors:
                return False
        return True


if __name__ == "__main__":
    game = MasterMind(*level["difficult"])
    game.set_solution()
    game.play(automatic=True)
    print(game)