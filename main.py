import argparse

from Interpreter import Interpreter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Befunge file for execute')
    parser.add_argument('file', type=str, help='Name of Befunge file')
    args = parser.parse_args()

    Interpreter(args.file)
