from vk import * # import __all__
import os.path # os.path.exists
#from termcolor import colored # colored console

vk = None # cvk object

def print_help():
    """
    prints help info
    """
    print("commands")
    print("- exit ~ break cycle and end code implementation")
    cvk_help()

if __name__ == "__main__": # launched as main file
    # check&create files
    if os.path.exists("vkf.txt") == False:
        open("vkf.txt", "tw", encoding="utf-8").close()

    print("---------------------------")
    print("music transfer")
    print("- github ~ https://github.com/XaRex1337/music_transfer")
    print("! for commands enter 'help'")

    print("---------------------------")    
    uinput = str(input("command: ")).lower()
    while uinput != "exit":
        if uinput == "help":
            print_help()

        if uinput.__contains__("vk"):
            if uinput == "vk":
                vk = cvk_from_input()

            if uinput == "vkf":
                vk = cvk_from_file()
                
            # can't do anything w/o cvk
            while vk == None or vk.api == None:
                vk = cvk_on_need(vk)
                if vk == 'e':
                    break

            if uinput == "vk show a":
                n = int(input("amount of albums: "))
                albums = vk.albums(n)
                print("+ got album list")
                for a in albums:
                    print(str(a))

            if uinput == "vk show at":
                a = str(input("enter album title: "))
                album = vk.get_album(a) # searching for correct album
                print("+ got album")
                print(str(album))
                if album != None:
                    n = int(input("amount of tracks: "))
                    tracks = vk.album_tracks(album.vk_owner_id, album.vk_album_id, n)
                    print("+ got track list")
                    for b in list(tracks):
                        print(str(b))

            if uinput == "vk show at repeat":
                a = str(input("album title: "))
                album = vk.get_album(a) # searching for correct album
                print("+ got album")
                print(str(album))
                if album != None:
                    tracks = vk.album_tracks(album.vk_owner_id, album.vk_album_id, 0)
                    print("+ got track list")
                    show_at_repeat(tracks)
                    
        print("---------------------------")
        uinput = input("command: ")
