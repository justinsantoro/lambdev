import argparse
import _json
from os import subprocess
from lambdev import aws_lambda
from . import run_test

COMMANDS = ['test']


def main():
    parser = argparse.ArgumentParser(description='Interact with AWS Lambda')
    subparsers = parser.add_subparsers(dest='command')

    parser_test = subparsers.add_parser('test', help='run a test sequence on one or more lambda functions')
    parser_test.add_argument('file', help='path to yaml file outlining test procedure')

    args = vars(parser.parse_args())

    if args['command'] not in COMMANDS:
        print('command not recognized.')

    if args['command'] == 'test':
        run_test.main(args['file'])