# spotify-gdpr-dump-analysis

Local analysis of complete spotify streaming dataset (endsong_*.json). Made in 3 hours alongside with chatGPT, fixing bugs as they appeared.

Ask for [your GDPR streaming data dump here](https://www.spotify.com/account/privacy/). It take a couple days to come.

That's a whole lot of data 👀

``` sh
# deps
$ pip install geoip2 basemap pandas matplotlib

# get geodb for local ip lookup
$ curl -L -o city.mmdb https://github.com/lysenkobv/maxmind-geolite2-database/raw/master/city.mmdb

# create sqlite3 database from json dump
$ python makedb.py datafolder/

# run analysis !
$ python map-ips-city.py
```

![a](https://user-images.githubusercontent.com/760637/230715992-3dd94060-c129-43a5-9af7-a35a09c4b8ea.png)

```
$ python top-cities.py
df                     city         country  count
20                   Berlin         Germany   2629
...
```

```
$ python top-songs-per-country.py
DE                                                 La femme d'argent                        Air
DE  Piano Concerto No. 3 in D Minor, Op. 30: I. Allegro ma non tanto        Sergei Rachmaninoff
DE                                La mer, L. 109: II. Jeux de vagues             Claude Debussy
DE                                                   Samba da Bencao             Bebel Gilberto
DE                                      Merry Christmas Mr. Lawrence           Ryuichi Sakamoto
DE                                                        WEIGHT OFF                 KAYTRANADA
...
```
