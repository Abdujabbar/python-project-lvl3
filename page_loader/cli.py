import argparse
import os


def get_cmd_args(argv=[]):
    parser = argparse.ArgumentParser(description='Page loader tool.')
    parser.add_argument('url', metavar='url')

    parser.add_argument('-o', '--output',
                        help='set path to store', default=os.getcwd())

    return parser.parse_args(argv)
