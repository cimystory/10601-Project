import sys
import dbLib
from collections import Counter
from math import log


distribution = {1:[], 2:[], 3:[], 4:[], 5:[]}
movie_genres = get_all_genres()

def train_user(user):
    [movies, ratings] = zip(*get_movies(user))
    genres = [get_genres(movie) for movie in movies]

    ratingCounter = Counter(ratings)
    genreCounter = {}

    for i in xrange(len(ratings)):
        rating = ratings[i]
        genre = genres[i]
        if rating not in genreCounter:
            genreCounter[rating] = Counter()
        genreCounter[rating].update(genre)
    return (ratingCounter, genreCounter)

def prepare_user((ratingCounter, genreCounter)):
    den = log(len(tagCounter) + sum(tagCounter.values()))
    ratingLogs = {}
    for rating in ratingCounter:
        ratingLogs[rating] = log(ratingCounter[rating] + 1) - den

    genreLogs = {}
    ratingDefaults = {}
    for rating in genreCounter:
        genreLogs[rating] = {}
        den = log(len(genreCounter[rating]) + sum(genreCounter[rating].values()))

        ratingDefaults[rating] = -den
        for genre in genreCounter[rating]:
            genreLogs[rating][genre] = log(genreCounter[rating][genre] + 1) - den

    return (ratingLogs, genreLogs, ratingDefaults)


def train(users):
    result = [(user, train_user(user)) for user in users]
    return dict(result)


def compute_rating_prob(result, user, rating, genres):
    (ratingLogs, genreLogs, ratingDefault) = result[user]
    n = ratingLogs[rating]
    for genre in genres:
        n += genreLogs[rating].get(genre, ratingDefault[rating])
    return n

def classify_user(result, user, genres):
    probs = [compute_rating_prob(result, user, i, genres) for i in range(1,6)]
    return results.index(max(probs)) + 1

def classify(result, users, movie_id):
    global distribution

    target_genres = get_genres(movie_id)
    for user in users:
        rating = classify_user(result, user, target_genres)
        distribution[rating].append(user)
    return distribution












def main():
    movie_id = int(argv[0])
    users = get_users(2000)
    #feature_list = get_features(movie_name)
    trainning_result = train(users)
    distribution = classify(trainning_result, users, movie_id)

    total = len(distribution[1]) + \
            len(distribution[2]) + \
            len(distribution[3]) + \
            len(distribution[4]) + \
            len(distribution[5])

    for i in range(1,6):
        print ("Rating 1: \%%0.2f of the users." % (100.0 * len(distribution[i]) / total))


if __name__ == '__main__':
    main()
