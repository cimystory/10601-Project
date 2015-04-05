import sys
import dbLib
from collections import Counter
from math import log
from random import randint



TEST_BOUND = 0
UPPER_BOUND = 17770
TEST_MOVIE = [191, 361, 468, 14240]


# Read a file
# filename is the path of the file, string type
# returns the content as a string
def readFile(filename, mode="rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents

def get_genres(movie):
    #print "Get genres for " + str(movie)
    genres = dbLib.getMovieFeaturesByMovieID(movie)['MOVIE_GENRE']
    if (genres):
        return genres.split(', ')
    else:
        return [u'Unknown']

def get_users(n):
    i = 0
    users = []
    src = "download/qualifying.txt"
    content = readFile(src).split('\n')
    while (i < n):
        index = randint(0,len(content)-1)
        line = content[index]
        if len(line) > 8:
            userID = line.split(',')[0]
            if userID not in users:
                users.append(line.split(',')[0])
                i += 1
    return users




def train_user(user):
    global TEST_BOUND, UPPER_BOUND, TEST_MOVIE

    print "Start Trainning user " + user
    stats = dbLib.getMovieRatingsByUserID(user)
    movies = []
    ratings = []
    for (movieID, rating) in stats:
        if int(movieID) not in TEST_MOVIE:
            movies.append(movieID)
            ratings.append(rating)

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
    den = log(len(ratingCounter) + sum(ratingCounter.values()))
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
    result = [(user, prepare_user(train_user(user))) for user in users]
    return dict(result)


def compute_rating_prob(result, user, rating, genres):
    (ratingLogs, genreLogs, ratingDefault) = result[user]
    if rating not in ratingLogs: return -sys.maxint

    n = ratingLogs[rating]
    for genre in genres:
        n += genreLogs[rating].get(genre, ratingDefault[rating])
    return n

def classify_user(result, user, genres):
    #print "Start classifying user " + user
    probs = [compute_rating_prob(result, user, i, genres) for i in range(1,6)]
    return probs.index(max(probs)) + 1

def classify(result, users, movie_id):
    distribution = {1:[], 2:[], 3:[], 4:[], 5:[]}
    target_genres = get_genres(movie_id)
    for user in users:
        rating = classify_user(result, user, target_genres)
        distribution[rating].append(user)
    return distribution


def report(result, users, movie_id):
    print "Reporting result for movie " + movie_id

    distribution = classify(result, users, movie_id)

    total = len(distribution[1]) + len(distribution[2]) + len(distribution[3]) + len(distribution[4]) + len(distribution[5])
    average = 0

    for i in range(1,6):
        proportion = float(len(distribution[i])) / total
        average += i * proportion
        print ("Rating %d: %0.2f of the users." % (i, proportion))

    print ("Average Rating: %0.1f" % average)
    print







def main(argv):
    global TEST_BOUND, TEST_MOVIE

    movie_id = argv[0]
    TEST_BOUND = int(argv[1])
    users = get_users(200)

    trainning_result = train(users)

    for movie in TEST_MOVIE:
        report(trainning_result, users, str(movie))




if __name__ == '__main__':
    main(sys.argv[1:])
