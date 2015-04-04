import sqlite3
import sys

def getAllGenres():
    genreString = "Short,Drama,Comedy,Documentary,Adult,Action,Romance,Thriller,Animation,Family,Horror,Crime,Music,Adventure,Fantasy,Sci-Fi,Mystery,Biography,History,Sport,Musical,War,Western,Reality-TV,News,Talk-Show,Game-Show,Film-Noir,Lifestyle,Experimental,Erotica"
    return genreString.split(",")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def getMovieFeaturesByMovieID(movieID):
    conn = sqlite3.connect('proj.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    query = "SELECT * FROM Movies WHERE MOVIE_ID is ?"
    c.execute(query, (movieID,))
    result = c.fetchone()
    conn.close()
    return result

def getMovieRatingsByUserID(userID):
    conn = sqlite3.connect('proj.db')
    c = conn.cursor()
    query = "SELECT MOVIE_ID, RATING FROM Ratings WHERE USER_ID = ?"
    c.execute(query, (userID,))
    result = c.fetchall()
    conn.close()
    return result



if __name__ == "__main__":
    print getMovieRatingsByUserID(int(sys.argv[1]))
