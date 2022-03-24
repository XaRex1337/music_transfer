__all__ = [ # import *
    "cvk",
    "cvk_from_input",
    "cvk_from_file",
    "cvk_on_need",
    "cvk_help"
]

import vk_api
from vk_api.audio import VkAudio
import json # to handle incoming information
import datetime as dt # to handle song/album time

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
    
    print("didn't get vk, enter data")
    uinput = input("enter anything to enter data or f to use data from file\ntype:")
    if uinput == "f":
        return cvk_from_file()
    return cvk_from_input()

def cvk_help():
    print("- vk ~ for accessing vk music / use 'vkf' to use login&password from file")
    print("     - show albums")

class csong:
    length = None
    author = None
    name = None

    def __init__(self, length, author, name):
        self.length = length
        self.author = author
        self.name = name

class calbum:
    title = None
    plays = None

    def __init__(self, title, plays):
        self.title = str(title)
        if plays == None: # TODO: some playlists have None at "plays" in dict, their "owner_id" < 0
            self.plays = -1
        else:
            self.plays = str(plays)

    def __str__(self):
        return str(self.title + " / plays: " + str(self.plays))

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

    def connect(self, login, password):
        """
        connects with user account
        ! access only to audio
        - input ~ login&password for entry
        - output ~ VkApi object
        """
        return vk_api.VkApi(login, password, scope=vk_api.VkUserPermissions.AUDIO)

    def albums(self): # TODO: some playlists have None at "plays" in dict, their "owner_id" < 0
        """
        get albums on user account
        output - list of calbum objects.
        """
        if (self.api == None):
            print("! no VkApi was accessed")
            return list()

        audio = VkAudio(self.api) # making VkAudio object
        # creating list of own calbum objects
        albums = list()
        for album in audio.get_albums():
            albums.append(calbum(album["title"], album["plays"]))
        return audio.get_albums()