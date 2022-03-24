from vk import * # import __all__
import os.path # os.path.exists
#from termcolor import colored # colored console

vk = None # cvk object

def print_help():
    """
    prints help info
    """
    print("---------------------------")
    print("commands")
    print("- exit ~ break cycle and end code implementation")
    cvk_help()
    print("---------------------------")

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
                
            if vk == None:
                cvk_on_need(vk)
            if uinput == "vk show albums":
                for a in list(vk.albums()):
                    print(str(a))

        uinput = input("command: ")