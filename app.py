import sys
import os
from library.parser import Parser
from os import path
from trie import Trie
from graph import Graph
from query import Query
from set import Set
from table import Table, TableRow
from terminaltables import AsciiTable


def main():
    filepaths = None
    trie = None
    graph = None
    query = None

    links_dict = None
    words_dict = None
    all_words = None

    result_set = None
    search_result = None
    table = None

    while True:
        print("##################################")
        print("Menu")
        print("1. Choose directory")
        print("2. Create trie")
        print("3. Create graph")
        print("4. Enter query")
        print("5. Search documents")
        print("6. Calculate rank")
        print("7. Show all results")
        print("8. Show paginated results")
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

            trie = None
            graph = None
            query = None
            result = None
            search_result = None
            table = None


        elif option == 2:
            if not words_dict or not links_dict or not all_words:
                print('No selected directory.')
                continue
            trie = create_trie(all_words)
        elif option == 3:
            if not trie:
                print('Trie is not created.')
                continue
            graph = create_graph(links_dict)
        elif option == 4:
            if not graph:
                print('Graph is not created')
                continue
            query = create_query()
        elif option == 5:
            if not query:
                print('Query is not entered.')
                continue
            result_set = search_documents(trie, query)

            proba = Set()
            search_result = proba.process_search_results(result_set, query)

        elif option == 6:
            if not search_result:
                print("Search is not executed.")
                continue
            table = calculate_rank(result_set, search_result, query, graph)

        elif option == 7:
            if not table:
                print("Rank calculation is not executed.")
                continue
            show_results_table(table)

        elif option == 8:
            if not table:
                print("Rank calculation is not executed.")
                continue
            show_results_paginated_table(table)

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
        if query.count(" and ") > 1 or query.count(" or ") > 1 or query.count(" not ") > 1:
            print("Only one logical operator allowed")
            continue

        query_first = ""
        query_second = ""

        query_object = Query()

        if " and " in query:
            query_object.operator = "and"
            splited = query.split("and")
            query_first = splited[0]
            query_second = splited[1]
        elif " or " in query:
            query_object.operator = "or"
            splited = query.split(" or ")
            query_first = splited[0]
            query_second = splited[1]
        elif " not " in query:
            query_object.operator = "not"
            splited = query.split(" not ")
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


def calculate_rank(result_set, results, query, graph):
    word_repetitions = dict()

    # racunanje ranga samo na osnovu broja ponavljanja reci u tekucem dokumentu
    for search_word in result_set:
        #u slucaju NOT operatora ne brojimo reci sa desne strane
        if query.operator == 'not' and search_word in query.query_second:
            continue

        for link in result_set[search_word]:
            if link not in word_repetitions:
                word_repetitions[link] = 1
            else:
                word_repetitions[link] += 1

    #broj ponavljanja reci od roditelja
    for link in word_repetitions:
        node = graph.search(link)

        for parent in node.parents:
            if parent in word_repetitions:
                word_repetitions[link] += word_repetitions[parent]

    # normalizovanje rezultata na opseg od 0 do 1
    max_el = max(word_repetitions.values())

    for link in word_repetitions:
        word_repetitions[link] = ((100 * word_repetitions[link]) / max_el) / 100

    #page rank
    d = 0.31
    N = len(graph.nodes)
    coeff = (1 - d) / N

    for link in word_repetitions:
        parents = graph.search(link).parents
        page_rank = 0
        for parent in parents:
            parent_children = graph.search(parent).children
            page_rank += coeff + d * (1 / N) / len(parent_children)

        word_repetitions[link] += page_rank

    #create table data
    table = Table()

    for result in results:
        table_row = TableRow()

        table_row.link = result

        try:
            table_row.rank = word_repetitions[result]
        except KeyError:
            continue

        table.rows.append(table_row)

    return table


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i].rank > R[j].rank:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def show_results_table(data):
    table_data = [
        ['Document', 'Rank']
    ]

    merge_sort(data.rows)

    for row in data.rows:
        table_row = []
        table_row.append(row.link)
        table_row.append(row.rank)
        table_data.append(table_row)

    table = AsciiTable(table_data)
    print(table.table)

def show_results_paginated_table(data):
    n = None
    while True:
        n = input("Enter number of rows per page: ")

        try:
            n = int(n)
        except:
            print('Numbers only')
            continue

        if n < 1:
            print("Number must be 1 or greater")
            continue

        break

    table_header = ['Document', 'Rank']

    merge_sort(data.rows)

    page = 1
    start = 0
    end = n

    table_rows = []
    for row in data.rows:
        table_row = []
        table_row.append(row.link)
        table_row.append(row.rank)
        table_rows.append(table_row)

    while True:
        paginated_table = table_rows[start:end]

        table_data = [table_header, *paginated_table, ["", "Page: " + str(page)]]
        table = AsciiTable(table_data)
        print(table.table)

        option = None

        while True:
            option = input("Previous(<), Next(>), Exit(x): ")

            if option not in ["<", ">", "x"]:
                print("Not a valid option")
                continue
            break

        if option == "<":
            if start - n < 0:
                print("Already on first page")
                continue
            start = start - n
            end = end - n
            page -= 1
            continue
        elif option == ">":
            if end >= len(data.rows):
                print("No more pages")
                continue
            start = start + n
            end = end + n
            page += 1
            continue
        else:
            break


main()