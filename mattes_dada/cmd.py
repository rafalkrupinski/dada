import argparse
import sys

from mattes_dada.model import DadaText
from .dada import load_from_file


def parse_args():
    p = argparse.ArgumentParser(prog='mdada')
    p.add_argument('--lang', type=str, default='en', choices=['en', 'pl'], help="Input language")
    p.add_argument('input_file', type=str, help='Input file, read standard input if none given', nargs='?')

    args = p.parse_args()
    return args


def main():
    args = parse_args()

    if not args.input_file or args.input_file is '-':
        dada = DadaText(sys.stdin.read(), lang=args.lang)
    else:
        dada = load_from_file(args.input_file, args.lang)

    for sent in dada.make_sentences():
        print(sent)


if __name__ == '__main__':
    main()
