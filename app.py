import sys
import os
from library.parser import Parser
from os import path
from trie import Trie
from graph import Graph
from query import Query
from set import Set


def main():
    filepaths = None
    trie = None
    graph = None
    query = None
    result_set = []

    links_dict = None
    words_dict = None
    all_words = None

    while True:
        print("##################################")
        print("Menu")
        print("1. Choose directory")
        print("2. Create trie")
        print("3. Create graph")
        print("4. Enter query")
        print("5. Search documents")
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
                if len(filepaths) == 0:
                    print('Path does not contain html document')
                    continue

            links_dict, words_dict = parse_documents(filepaths)

            all_words = merge_words(words_dict)

            # for g in graph:
            #     print(g.document_path)
            #     print(g.parents)
            #     print(g.children)
            #     print("-----------")

        elif option == 2:
            trie = create_trie(all_words)
        elif option == 3:
            graph = create_graph(links_dict)
        elif option == 4:
            query = create_query()
        elif option == 5:
            result_set = search_documents(trie, query)



        elif option == 0:
            sys.exit('Bye')
        else:
            print('No option with that number')


def choose_directory():
    # temp = "C:\\Users\\Lenovo\\Desktop\\oisisi_python\\test-skup\\faq"
    temp = "C:\\Users\\Maja\\Desktop\\oisisi_python\\test-skup\\faq"
    # dir = input('Enter directory absolute path: ')
    dir = temp

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
    result = dict()
    for filepath in words_dict:
        for word in words_dict[filepath]:
            word = word.lower()
            if word not in result:
                result[word] = [filepath]
            else:
                result[word].append(filepath)

    return result


def create_trie(all_words):
    trie = Trie()

    for word in all_words:
        trie.insert(word, all_words[word])

    return trie


def create_graph(links_dict):
    graph = Graph()

    for html_path in links_dict:
        graph.insert(html_path, links_dict[html_path])

    return graph


def create_query():
    while True:
        query = input("Enter query: ").lower()
        if query.count("and") > 1 or query.count("or") > 1 or query.count("not") > 1:
            print("Only one logical operator allowed")
            continue

        query_first = ""
        query_second = ""

        query_object = Query()

        if "and" in query:
            query_object.operator = "and"
            splited = query.split("and")
            query_first = splited[0]
            query_second = splited[1]
        elif "or" in query:
            query_object.operator = "or"
            splited = query.split("or")
            query_first = splited[0]
            query_second = splited[1]
        elif "not" in query:
            query_object.operator = "not"
            splited = query.split("not")
            query_first = splited[0]
            query_second = splited[1]
        else:
            query_first = query

        if query_first:
            query_first_splited = query_first.strip().split(" ")

            # preuzmi samo validne reci
            for word in query_first_splited:
                if not word == "":
                    query_object.query_first.append(word)
        if query_second:
            query_second_splited = query_second.strip().split(" ")

            #prezumi samo validne reci
            for word in query_second_splited:
                if not word == "":
                    query_object.query_second.append(word)

        if query_object.operator and (not query_object.query_first or not query_object.query_second):
            print("Query is not valid")
        else:
            break

    return query_object


def search_documents(trie, query):
    result_set = dict()

    for word in query.query_first:
        result_set[word] = trie.search(word)

    for word in query.query_second:
        result_set[word] = trie.search(word)

    return result_set

main()