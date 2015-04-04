import multiprocessing
import sqlite3
import sys
import os


conn = sqlite3.connect('proj.db')
c = conn.cursor()

def getPathFromMovieID(movieID):
    file = "mv_%07d.txt" %(movieID)
    path = os.path.join("training_set",file)
    return path


def fetchRating(movieID):
    path = getPathFromMovieID(movieID)
    with open(path) as f:
        lines = f.read().splitlines()
        for l in lines:
            if "," in l:
                infoList = l.split(",")
                userID  = int(infoList[0])
                rating = int(infoList[1])
                dateStr = infoList[2]

                query = "INSERT INTO Ratings (MOVIE_ID, USER_ID, RATING, RATE_DATE) VALUES (?,?,?,?);"
                vals =  (movieID, userID, rating, dateStr)
                c.execute(query, vals)
        conn.commit()
        return

for i in xrange (1,17771):
    print("fetching %d") %i
    fetchRating(i)

conn.close()
print("finished, closed db")
