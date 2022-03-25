__all__ = [ # import *
    "cvk",
    "cvk_from_input",
    "cvk_from_file",
    "cvk_on_need",
    "cvk_help",
    "show_at_repeat"
]

import vk_api
from vk_api.audio import VkAudio
import json # to handle incoming information
import datetime as dt # to handle song/album time

vk = None # cvk object

def cvk_from_input():
    """
    retrieves data from input and creates cvk object
    """
    login = str(input("login: "))
    password = str(input("password: "))
    return cvk(login, password)

def cvk_from_file():
    """
    retrieves data from file and creates cvk object
    """
    vkF = open("vkF.txt", 'r', encoding="utf-8")
    login = vkF.readline().replace('\n', '')
    password = vkF.readline()
    print("login: " + login)
    print("password: " + password)
    vkF.close()
    return cvk(login, password)

def cvk_on_need(vk):
    """
    if cvk object already created it skips func
    if not it is asking for information to create it
    """
    if vk != None:
        return
    
    print("---------------------------")
    print("didn't get vk, enter data")
    uinput = input("- enter anything to enter data\n- enter f to use data from file\n- enter e to exit cycle\ntype:")
    if uinput == 'f':
        return cvk_from_file()
    elif uinput == 'e':
        return 'e'
    return cvk_from_input()

def cvk_help():
    print("- vk ~ for accessing vk music / use 'vkf' to use login&password from file")
    print("     - show a / shows albums / asks for amount, enter <= 0 for all")
    print("     - show at / shows album tracks / asks for amount, enter <= 0 for all")
    print("     - show at repeat / shows album tracks repeats / if track is saved multiple times it shows amount of it")

def show_at_repeat(tracks):
    """
    shows repeats in track list
    - tracks ~ list of ctrack objects
    """
    checked = list() # already checked tracks
    for n, track1 in enumerate(tracks): # get n for indexing
        try:
            checked.index(str(track1.artist + track1.title)) # if not in list raise IOError
            continue # in other way skip this track
        except:
            pass
        repeats = 1 # how many times
        for track2 in tracks[n + 1:]: # optimizate and skip previous
            if track1.artist.lower() == track2.artist.lower() and track1.title.lower() == track2.title.lower():
                repeats += 1
        if repeats > 1:
            checked.append(str(track1.artist + track1.title)) # already checked
            print("repeats: {} / {}".format(repeats, track1))

    if len(checked) == 0:
        print("no repeats, good album")

class ctrack:
    artist = None
    title = None
    duration = None

    def __init__(self, track):
        """
        on init converts dict object to ctrack object
        - track ~ dict object from track list
        """
        self.artist = track["artist"]
        self.title = track["title"]
        self.duration = track["duration"]
    
    def __str__(self):
        """
        for str(...) usage
        """
        return "{} - {} [{}]".format(self.artist, self.title, str(dt.timedelta(seconds = self.duration)))

class calbum:
    title = None
    plays = None
    vk_owner_id = None
    vk_album_id = None

    def __init__(self, album):
        """
        on init converts dict object to calbum object
        - album ~ dict object from albums list
        """
        self.title = str(album["title"])
        if album["plays"] == None: # TODO: some playlists have None at "plays" in dict, their "owner_id" < 0
            self.plays = -1
        else:
            self.plays = int(album["plays"])

        self.vk_album_id = album["id"]
        self.vk_owner_id = album["owner_id"]

    def __str__(self):
        """
        for str(...) usage
        """
        if self.vk_album_id != None: # this is vk album
           return "/vk/ {} / plays: {} / \t\t\t\talbum_id: {}, owner_id: {}".format(self.title, self.plays, self.vk_album_id, self.vk_owner_id)
        return "/unknown/ {} / plays: {}".format(self.title, self.plays) # didn't define platform

# vk funcs
class cvk:
    api = None

    def __init__(self):
        """
        on init sets api as unaccessed VkApi
        """
        self.api = None

    def __init__(self, login, password):
        """
        on init makes an VkApi object via connect function and makes authentication
        """
        self.api = self.connect(login, password)
        try:
            self.api.auth()
        except:
            print("! wrong data, try again")
            self.api = None

    def connect(self, login, password) -> vk_api.VkApi:
        """
        connects with user account
        ! default access
        - input ~ login&password for entry
         output - VkApi object
        """
        return vk_api.VkApi(login, password)

    def albums(self, n) -> list: # TODO: some playlists have None at "plays" in dict, their "owner_id" < 0
        """
        get albums on user account
        - n (int) ~ amount of albums
        output - list of calbum objects
        """
        if (self.api == None):
            print("! no VkApi was accessed")
            return list()

        audio = VkAudio(self.api) # making VkAudio object
        api_albums = audio.get_albums()

        if n <= 0:
            n = len(api_albums)

        # creating list of own calbum objects
        albums = list()
        for album in api_albums[:n]:
            albums.append(calbum(album))
        return albums

    def get_album(self, title) -> calbum:
        """
        get first album with correct title
        - title ~ title of required album
        output - calbum object
        """
        albums = self.albums(0)
        for album in self.albums(0):
            if album.title == title:
                return album

    def album_tracks(self, owner_id, album_id, n) -> list:
        """
        get tracks from album
        - owner_id ~ owner_id for required album (calbum.owner_id)
        - album_id ~ id for required album (calbum.album_id)
        - n ~ amount of tracks
        output - list of ctrack objects
        """
        if (self.api == None):
            print("! no VkApi was accessed")
            return list()
        
        audio = VkAudio(self.api) # making VkAudio object
        api_tracks = audio.get(owner_id=owner_id, album_id=album_id)

        if n <= 0:
            n = len(api_tracks)

        # creating list of own ctrack objects
        tracks = list()
        for track in api_tracks[:n]:
            #tracks.append(ctrack(audio, track))
            tracks.append(ctrack(track))
        return tracks
