from sys import argv

from .dada import generate_from_file


def main():
    if len(argv) < 2:
        print("pass file name")
        exit(-1)

    for sent in generate_from_file(argv[1]):
        print(sent)


if __name__ == '__main__':
    main()
