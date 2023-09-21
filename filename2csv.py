#   Copyright 2023 hidenorly
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import os
import re
import random
import string
import time

def expandPath(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='directory util', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('target', metavar='PATH', type=str, nargs='+', help='Target path (can specicy multiply)')
    parser.add_argument('-a', '--absolutePath', action='store_true', help='Set this if absolute path is expected')
    args = parser.parse_args()

    for aPath in args.target:
        for dirpath, dirnames, filenames in os.walk(aPath):
            if args.absolutePath:
                dirpath = expandPath(dirpath)
            for filename in filenames:
                print( dirpath+","+filename)
