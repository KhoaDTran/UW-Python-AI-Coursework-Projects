# Author Dylan Jergens
# This program runs the search engine, taking user input

from search_engine import SearchEngine


def main():
    print('Welcome to 6oog13!!')
    directory = input('Please enter a the name of a directory: ')

    print('Building Search Engine...')
    print()
    engine = SearchEngine(directory)

    answer = 'y'
    while (answer == 'y'):
        term = input('Search (enter a term to query): ')
        ranking = engine.search(term)
        print("Displaying results for " + "'" + term + "':")
        if ranking is None:
            print('    No results :(')
        else:
            rank = 1
            for doc in ranking:
                print('    ' + str(rank) + '. ' + doc)
                rank += 1
            print()
        answer = ''
        while not (answer == 'y' or answer == 'n'):
            answer = input('Would you like to search another term (y/n) ')


if __name__ == '__main__':
    main()
