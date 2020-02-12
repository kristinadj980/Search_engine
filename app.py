import sys
import os
from library.parser import Parser
from os import path
from trie import Trie, TrieNode


def main():
    filepaths = None
    trie = None

    while True:
        print("##################################")
        print("Menu")
        print("1. Choose directory")
        print("2. Create trie")
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

            links_dict, words_dict = parse_documents(filepaths)

            all_words = merge_words(words_dict)

            trie = create_trie(all_words)

        elif option == 2:
            create_trie()
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
    words_dict = dict()
    links_dict = dict()

    for path in paths:
        parser = Parser()
        links, words = parser.parse(path)
        words_dict[path] = words
        links_dict[path] = links

    return links_dict, words_dict


def merge_words(words_dict):
    result = []
    for array in words_dict:
        for word in array:
            if word not in result:
                result.append(word)

    return result


def create_trie(all_words):
    trie = Trie()

    for word in all_words:
        trie.insert(word)

    return trie

main()