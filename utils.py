def get_perfects(attempt, solution):
    perfects = 0
    for i in range(len(solution)):
        if solution[i] == attempt[i]:
            perfects += 1
    return perfects

def get_corrects(attempt, solution):
    perfects = get_perfects(attempt, solution)
    attempt = list(attempt)
    for i, x in enumerate(solution):
        for j, y in enumerate(attempt):
            if x == y:
                attempt.pop(j)
                break
    return len(solution) - len(attempt) - perfects