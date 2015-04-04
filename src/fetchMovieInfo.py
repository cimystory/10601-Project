import urllib2
import urllib
import json
import multiprocessing
import sqlite3
import httplib
import sys

pool = multiprocessing.Pool()
conn = sqlite3.connect('proj.db')
c = conn.cursor()

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

def getOMDBUrl(title, year):
    url = "http://omdbapi.com/?t=%s&y=%s&plot=short&r=json" \
            %(urllib.quote_plus(title), urllib.quote_plus(str(year)))
    return url

def getInfoObj(str):
    mList = str.split(",")
    mID = int(mList[0])
    print(mID)
    if (mID % 300 == 0):
        conn.commit()
    try:
        mYear = int(mList[1])
    except ValueError:
        mYear = 0
    mTitle = mList[2]
    url = getOMDBUrl(mTitle, mYear)
    if (mID == 6483):
        url = getOMDBUrl("Smokey Joe's Cafe", mYear)
    response = urllib2.urlopen(url).read()
    try:
        obj = json.loads(response)
    except ValueError:
        obj = {}
        obj[u"Response"] = u"False"

    obj[u"Movie_ID"] = mID
    obj[u"Year"] = mYear
    obj[u"Title"] = mTitle
    return obj

def fetchInfo(path):
    with open(path) as f:
        result = []
        lines = f.read().splitlines()
        for l in lines:
            try:
                obj = getInfoObj(l)
            except httplib.BadStatusLine:
                continue
            finally:
                if (obj[u"Response"] != u"False"):
                    length = obj[u"Runtime"].split(" min")[0]
                    meta = obj[u"Metascore"]
                    imdbr = obj[u"imdbRating"]
                    imdbv = obj[u"imdbVotes"].replace(',', '')
                    if (length.isnumeric()):
                        length = int(length)
                    else:
                        length = -1
                    if (meta.isnumeric()):
                        meta = int(meta)
                    else:
                        meta = -1
                    try:
                        imdbr = float(imdbr)
                    except ValueError:
                        imdbr = -1.0
                    if (imdbv.isnumeric()):
                        v = int(imdbv)
                    else:
                        v = -1
                    query = u"INSERT OR IGNORE INTO Movies ( MOVIE_ID, MOVIE_YEAR , MOVIE_TITLE, MOVIE_RATING, MOVIE_LENGTH, MOVIE_GENRE, MOVIE_DIRECTOR, MOVIE_WRITER, MOVIE_ACTOR, MOVIE_METASCORE, MOVIE_IMDBRATING, MOVIE_IMDBVOTES) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                    # vals = u"( %s, %s, '%s', '%s', %s, '%s', '%s', '%s', '%s', %s, %f, %s)" %  (obj[u"Movie_ID"], \
                    vals =  (obj[u"Movie_ID"], \
                                obj[u"Year"], \
                                obj[u"Title"], \
                                obj[u"Rated"], \
                                length, \
                                obj[u"Genre"], \
                                obj[u"Director"], \
                                obj[u"Writer"], \
                                obj[u"Actors"], \
                                meta, \
                                imdbr, \
                                v)
                    c.execute(query, vals)

                else:
                    query = u"INSERT OR IGNORE INTO \
                            Movies (\
                            MOVIE_ID,\
                            MOVIE_YEAR ,\
                            MOVIE_TITLE\
                            ) VALUES ( ?, ?, ?)"
                    vals = (obj[u"Movie_ID"], obj[u"Year"], obj[u"Title"])
                    c.execute(query, vals)

        conn.commit()
        return result

fetchInfo(str(sys.argv[1]))
conn.close()
print("closed")



