import sys
import os
from library.parser import Parser
from os import path


def main():
    filepaths = None

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
            else:
                filepaths = find_html_files(directory)

            parse_documents(filepaths)

        elif option == 0:
            sys.exit('Bye')
        else:
            print('No option with that number')


def choose_directory():
    # temp = "C:\\Users\\Lenovo\\Desktop\\oisisi_python\\test-skup"
    dir = input('Enter directory absolute path: ')
    # dir = temp

    if not os.path.isdir(dir):
        print('Path does not exist or it is a file, not a directory')
        return None

    return dir


def find_html_files(dir):
    filepaths = []
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(".html"):
                filepaths.append(filepath)

    return filepaths


def parse_documents(paths):
    all_words = dict()
    all_links = dict()

    for path in paths:
        parser = Parser()
        links, words = parser.parse(path)
        all_words[path] = words
        all_links[path] = links


main()