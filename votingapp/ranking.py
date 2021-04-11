from functools import reduce

# placeholder code for schulze ranking
# taken from evote_ranking for testing purposes
# ballots should be received here like this to be processed
# preferences = [['A', 'B', 'C'], ['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C']]


def cmp(a, b):
    return (a > b) - (a < b)


def cmp_to_key(mycmp):
    "Convert a cmp= function into a key= function"

    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


def assert_valid(preference):
    """check no repeated candidate names in preference"""
    if len(preference) != len(set(preference)):
        raise ValueError("Invalid preference. Candidate name is repeated")


def schulze(preferences):
    """schulze ranking algorithm"""
    d = {}
    p = {}
    candidates = list(
        reduce(lambda a, b: a & b, [set(preference) for preference in preferences])
    )
    map_candid = dict((k, i) for (i, k) in enumerate(candidates))
    n = len(candidates)
    for i in range(n):
        for j in range(n):
            d[i, j] = p[i, j] = 0
    for preference in preferences:
        assert_valid(preference)
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                key = (map_candid[preference[i]], map_candid[preference[j]])
                d[key] += 1
    for i in range(n):
        for j in range(n):
            if i != j:
                p[i, j] = d[i, j] if d[i, j] > d[j, i] else 0
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(n):
                    if k != i and k != j:
                        p[j, k] = max(p[j, k], min(p[j, i], p[i, k]))
    winners = list(range(n))
    winners.sort(key=cmp_to_key(lambda i, j: cmp(p[i, j], p[j, i])))
    winners = [(i, candidates[k]) for (i, k) in enumerate(winners)]
    winners.reverse()
    return winners
