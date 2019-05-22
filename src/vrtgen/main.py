"""
Command-line interface for vrtpktgen.
"""
import logging
import argparse
import sys

from vrtgen.parser import FileParser
from vrtgen.backend import Generator

from . import version

class NullGenerator(Generator):
    def generate(self, packet):
        pass

def main():
    logging.basicConfig()

    arg_parser = argparse.ArgumentParser(description='Generate VITA 49.2 packet classes.')
    arg_parser.add_argument('filename', nargs='+', help='VRT YAML definition file')
    arg_parser.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='display debug messages')
    arg_parser.add_argument('--version', action='version', version='%(prog)s '+version.__version__)
    arg_parser.add_argument('-b', '--backend', help='code generator backend to target')
    arg_parser.add_argument('-o', '--option', action='append', default=[],
                            help='options for code generator backend')

    args = arg_parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.backend == 'bindump':
        from vrtgen.backend.bindump import BinaryDumper
        generator = BinaryDumper()
    elif args.backend == 'cpp':
        from vrtgen.backend.cpp import CppGenerator
        generator = CppGenerator()
    elif args.backend is None:
        generator = NullGenerator()
    else:
        raise SystemExit("invalid backend '"+args.backend+"'")

    for option in args.option:
        if '=' in option:
            name, value = option.split('=', 1)
        else:
            name = option
            value = True
        try:
            generator.set_option(name, value)
        except Exception as exc:
            raise SystemExit(str(exc))

    for filename in args.filename:
        logging.debug('Parsing %s', filename)
        for packet in FileParser().parse(filename):
            generator.generate(packet)
