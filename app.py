import sys
import os
from os import path


def main():
    while True:
        print("##################################")
        print("Menu")
        print("1. Choose directory")
        print("0. Exit")

        option = input('Choose menu option: ')

        try:
            option = int(option)
        except:
            print('Numbers only')
            continue

        if option == 1:
            directory = choose_directory()

            if not directory:
                continue

        elif option == 0:
            sys.exit('Bye')
        else:
            print('No option with that number')


def choose_directory():
    dir = input('Enter directory absolute path: ')

    if not os.path.isdir(dir):
        print('Path does not exist or it is a file, not a directory')
        return None

    return dir


main()