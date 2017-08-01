#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script accepts one input file (e.g. input.py) with the RMG-Py model to generate, 
optional parameters `--original [folder of original rmg model] ` can allow using 
a starting RMG model. A special path can be added  with the argument `--output` for the
path to output the final files.
"""

import argparse
import logging
import os
import os.path

from rmgpy.rmg.main import initializeLog
from rmgpy.tools.isotopes import run

################################################################################


def parseCommandLineArguments():
    """
    Parse the command-line arguments being passed to RMG-Py. This uses the
    :mod:`argparse` module, which ensures that the command-line arguments are
    sensible, parses them, and returns them.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='RMG input file')
    parser.add_argument('--output', type=str, nargs=1, default='',help='Output folder')
    parser.add_argument('--original', type=str, nargs=1, default='', 
                        help='Location of the isotopeless mechanism')
    parser.add_argument('--maximumIsotopicAtoms', type=int, nargs=1, default=[1000000],
                        help='The maxuminum number of isotopes you allow in a specific molecule')
    parser.add_argument('--useOriginalReactions' , action='store_true', default=False,
                        help='use reactions from the original rmgpy generated chem_annotated.inp file')

    args = parser.parse_args()
    
    return args

def main():

    args = parseCommandLineArguments()
    if args.useOriginalReactions and not args.original:
        raise AttributeError('Cannot use original reactions without a previously run RMG job')
    maximumIsotopicAtoms = args.maximumIsotopicAtoms[0]
    useOriginalReactions = args.useOriginalReactions
    inputFile = args.input
    outputdir = os.path.abspath(args.output[0]) if args.output else os.path.abspath('.')
    original = os.path.abspath(args.original[0]) if args.original else None

    initializeLog(logging.INFO, os.path.join(os.getcwd(), 'RMG.log'))
    run(inputFile, outputdir, original=original, 
        maximumIsotopicAtoms=maximumIsotopicAtoms,
        useOriginalReactions=useOriginalReactions)

if __name__ == '__main__':
    main()