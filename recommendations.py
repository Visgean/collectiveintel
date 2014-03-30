from math import sqrt
from data import critics

def sim_distance(preferences, person1, person2):
    """
        Returns Euclidean distance score
    """
    # list with th elements (eg movies) that both persons have in common
    common_list = set(preferences[person1].keys()) & set(preferences[person2].keys())
    if not common_list: # if there is nothing in common
        return 0

    sum_of_squares = sum([pow(preferences[person1][item] - preferences[person2][item], 2) for item in common_list])
    return 1/(1+sum_of_squares)


def sim_pearson(preferences, person1, person2):
    """
        Returns Pearson correlation score
    """

    # list with the elements (eg movies) that both persons have in common
    common_list = set(preferences[person1].keys()) & set(preferences[person2].keys())
    if not common_list:  # if there is nothing in common
        return 0

    n = len(common_list)
    # sums of the preferences:
    sum1 = sum(preferences[person1][it] for it in common_list)
    sum2 = sum(preferences[person2][it] for it in common_list)
    # sums of preferences to the second power
    sum_squared1 = sum(pow(preferences[person1][it], 2) for it in common_list)
    sum_squared2 = sum(pow(preferences[person2][it], 2) for it in common_list)

    # sum of the products of the preferences:
    sum_products = sum(preferences[person1][it] * preferences[person2][it] for it in common_list)

    num=sum_products - ((sum1*sum2)/n)
    den=sqrt((sum_squared1-pow(sum1,2)/n)*(sum_squared2-pow(sum2,2)/n))

    if den:
        return num/den
    else:
        return 0

def top_matches(preferences, person, number_of_elements = 3, similarity = sim_pearson):
    others = list(critics.keys()) # creating another instance of critics keys
    others.remove(person)

    scores = [(similarity(preferences, person, other),other) for other in  others]
    scores.sort(reverse=True)
    return scores[:number_of_elements]




def recommend(preferences, person):
    """
        Returns recommended items for 'person' based on the preferences
    """
    movies = set() # set of all the movies that we have data based on
    for critic in preferences.keys():
        movies = movies | set(preferences[critic].keys())
    movies_to_see = movies - set(preferences[person].keys()) # set of all the movies that 'person' did not see yet




#print recommend(preferences=critics, person='Toby')
