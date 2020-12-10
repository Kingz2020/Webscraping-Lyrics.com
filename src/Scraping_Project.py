import re
import requests
import time
from bs4 import BeautifulSoup
import os
import pandas as pd


def cleaner(str):
    '''
    cleans the string leaving just the name of the song
    Input:  'asasas/geseg/csac/xxxxx'
    Output: 'xxxx'
    '''
    pos = 1
    while pos > 0:
        pos = str.find('/')
        str = str[pos+1:]
        pos = str.find('/')
    return str


def scrapes_raw_artist_html(source_path, artist):
    '''
    cleans the raw artist html page from lyrics.com
    output: the matches of songs
    '''
    regex = r"\/lyric/[\w\/\+%]+"

    with open(source_path, 'r') as file:
        text = file.read()
    print(text)
    matches = re.finditer(regex, text, re.MULTILINE)

    return matches


def stores_lyrics_from_artist(matches, artist, dest_path):
    '''
    gets the lyrics of an artist from lyrics.com and stores it to a destination
    input: matches, artist, dest_path
    '''
    for matchNum, match in enumerate(matches, start=1):
        print("{} track: {match}".format(matchNum, match=match.group()))
        url = 'https://www.lyrics.com/' + match.group()
        lyrics = requests.get(url)
        time.sleep(0.2)
        # print(match.group())
        # print(cleaner(match.group()))
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
        with open(dest_path + cleaner(match.group()) + '.html', 'w') as file:
            file.write(lyrics.text)
    return print('data stored')


def gets_artists_page_to_destination(dest_path, artist, artist_code):
    '''
    gets the artists main page from lyrics.com to a given destination
    '''
    url = 'https://www.lyrics.com/artist/' + artist + '/' + artist_code
    resp = requests.get(url)
    time.sleep(0.2)
    print('********** ' + dest_path + artist + '/ **************')
    if not os.path.exists(dest_path + artist + '/'):
        os.mkdir(dest_path + artist + '/')
    with open(dest_path + artist + '.html', 'w') as file:
        file.write(resp.text)
    return print('lyrics destined!')


def raw_to_clean(artist, raw_path, clean_path):
    '''
    takes all the raw files in a source path, cleans it, and stores it in dest_path
    '''
    for fn in os.listdir(raw_path + artist+'/'):
        inh = open(raw_path + artist+'/' + fn).read()
        soup = BeautifulSoup(inh)
        song = soup.find('pre', class_='lyric-body').text
        song_title = soup.find(class_='lyric-title').text
        song_title = song_title.replace(' ', '_')
        song_title = song_title.replace('/', '_')
        print(song_title)
        if not os.path.exists(clean_path + artist+'/'):
            os.mkdir(clean_path + artist+'/')
        with open(clean_path + artist+'/' + song_title + '.html', 'w') as file:
            file.write(song)

    return print('cleaning done')


def html_2_dataframe(source_path, name, artist):
    '''
    converts html file to the dataframe
    '''
    df = pd.DataFrame()

    for fn in os.listdir(source_path + artist):
        inh = open(source_path + artist + '/' + fn).read()
        df = df.append({'Lyrics': inh, 'Artist': artist}, ignore_index=True)

    return print('conversion completed for {}!'.format(artist))


# -----------------------------------------------------------------------------------------

Artist = ['Bob Marley', 'Led Zeppelin']  # , 'Michael Jackson', 'Radiohead']
Artist_Code = ['2907', '4739']  # , '4576', '41092']
raw_path = '../data/raw/'
clean_path = '../data/clean/'

# creation of raw artist lyrics files
for i in range(len(Artist)):
    gets_artists_page_to_destination(raw_path, Artist[i], Artist_Code[i])

# filtering the lyrics from the files and storing the raw songs in the raw path
for i in range(len(Artist)):
    matches = scrapes_raw_artist_html(
        raw_path + Artist[i] + '.html', Artist[i])
    stores_lyrics_from_artist(matches, Artist[i], raw_path + Artist[i] + '/')

# raw to clean
for i in range(len(Artist)):
    raw_to_clean(Artist[i], raw_path, clean_path)

# html file to df
for i in range(len(Artist)):
    html_2_dataframe(clean_path, Artist[i]+'_songs', Artist[i])
