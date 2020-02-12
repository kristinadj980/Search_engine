import sys
import os
from library.parser import Parser
from os import path
from trie import Trie, TrieNode
from document import Document
from query import Query


def main():
    filepaths = None
    trie = None

    while True:
        print("##################################")
        print("Menu")
        print("1. Choose directory")
        print("2. Create trie")
        print("3. Enter query")
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

            graph = create_graph(links_dict)

            # for g in graph:
            #     print(g.document_path)
            #     print(g.parents)
            #     print(g.children)
            #     print("-----------")

        elif option == 2:
            create_trie()
        elif option == 3:
            create_query()
        elif option == 0:
            sys.exit('Bye')
        else:
            print('No option with that number')


def choose_directory():
    # temp = "C:\\Users\\Lenovo\\Desktop\\oisisi_python\\test-skup\\faq"
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


def create_graph(links_dict):
    documents = []

    for html_path in links_dict:
        document = Document()
        document.document_path = html_path
        document.children = links_dict[html_path]
        document.parents = []

        for html_path1 in links_dict:
            for link1 in links_dict[html_path1]:
                if link1 == html_path:
                    document.parents.append(html_path1)

        documents.append(document)

    return documents


def create_query():
    while True:
        query = input("Enter query: ")

        if query.count("AND") > 1 or query.count("OR") > 1 or query.count("NOT") > 1:
            print("Only one logical operator allowed")
            continue

        query_first = ""
        query_second = ""

        query_object = Query()

        if "AND" in query:
            query_object.operator = "AND"
            splited = query.split("AND")
            query_first = splited[0]
            query_second = splited[1]
        elif "OR" in query:
            query_object.operator = "OR"
            splited = query.split("OR")
            query_first = splited[0]
            query_second = splited[1]
        elif "NOT" in query:
            query_object.operator = "NOT"
            splited = query.split("NOT")
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

    # print("operator", query_object.operator)
    # print("first", query_object.query_first)
    # print("second", query_object.query_second)

    return query_object

main()