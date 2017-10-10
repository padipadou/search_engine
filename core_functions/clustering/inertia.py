import core_functions.similar_docs as sd
from core_functions import Const


def compute_Total_Inertia(centreOfGravityDict, all_vectors_dict):
    sum = 0
    n = Const.CORPUS_SIZE

    for i in range(n):
        dist = 1 - sd.calculate_cosine(centreOfGravityDict, all_vectors_dict[frozenset({i})][0])
        sum += dist**2

    return (1/n) * sum


def compute_Interclass_Inertia(centreOfGravityDict, avg_vectors_dict):
    sum = 0
    n = Const.CORPUS_SIZE

    for key, value in avg_vectors_dict.items():
        try: #NEED TO BE REVIEWED
            dist = 1 - sd.calculate_cosine(centreOfGravityDict, value)
        except:
            dist = 1 - sd.calculate_cosine(centreOfGravityDict, value[0])
        sum += len(key) * dist**2

    return (1/n) * sum


def compute_Intraclass_Inertia(avg_vectors_dict, all_vectors_dict):
    sum = 0
    n = Const.CORPUS_SIZE

    for key, value in avg_vectors_dict.items():
        gk = value
        for i in key:
            try:
                dist = 1 - sd.calculate_cosine(gk, all_vectors_dict[frozenset({i})][0])
            except:
                dist = 1 - sd.calculate_cosine(gk[0], all_vectors_dict[frozenset({i})][0])
            sum += dist**2

    return (1/n)*sum


if __name__ == '__main__':
    pass