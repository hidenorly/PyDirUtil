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
from itertools import combinations

class DuplicatedFileUtil:
    DEFAULT_CHUNK_SIZE = 1024*1024*1024

    def expandPath(path):
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        return path

    def isSameFile(path1, path2, _chunkSize=DEFAULT_CHUNK_SIZE):
        isFirstRead = True
        try:
            with open(path1, 'rb') as file1:
                with open(path2, 'rb') as file2:
                    while True:
                        if isFirstRead:
                            chunkSize = 4096
                            isFirstRead = False
                        else:
                            chunkSize = _chunkSize
                        chunk1 = file1.read(chunkSize)
                        chunk2 = file2.read(chunkSize)
                        if not chunk1 or not chunk2:
                            break
                        if chunk1 != chunk2:
                            return False

            return True
        except:
            return False

    def getDuplicateFiles(targetPaths, isAbsolutePath):
        sameFiles = {}

        paths = set()
        sizesAndPaths = {}
        for aPath in targetPaths:
            for dirpath, dirnames, filenames in os.walk(aPath):
                if isAbsolutePath:
                    dirpath = DuplicatedFileUtil.expandPath( dirpath )
                for filename in filenames:
                    thePath = os.path.join( dirpath, filename )
                    paths.add( thePath )
                    size = os.path.getsize( thePath )
                    if not size in sizesAndPaths:
                        sizesAndPaths[ size ] = []
                    sizesAndPaths[size].append( thePath )

        for size, samePaths in sizesAndPaths.items():
            if len(samePaths)>=2:
                combinationsList = list(combinations(samePaths, 2))
                for combination in combinationsList:
                    if DuplicatedFileUtil.isSameFile(combination[0], combination[1]):
                        #print(f'{size}:{combination[0]}, {combination[1]}')
                        if not combination[0] in sameFiles and not combination[1] in sameFiles:
                            # not found both
                            sameFiles[ combination[0] ] = []
                            sameFiles[ combination[0] ].append( combination[1] )
                        elif not combination[0] in sameFiles and combination[1] in sameFiles:
                            # not found 0 but found 1
                            sameFiles[ combination[1] ].append( combination[0] )
                        elif combination[0] in sameFiles and not combination[1] in sameFiles:
                            # found 0 but not found 1
                            sameFiles[ combination[0] ].append( combination[1] )
                        else:
                            # both found <- error
                            pass
        return sameFiles



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='file util', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('target', metavar='PATH', type=str, nargs='+', help='Target path (can specicy multiply)')
    parser.add_argument('-a', '--absolutePath', default=False, action='store_true', help='Set this if absolute path is expected')
    args = parser.parse_args()

    sameFiles = DuplicatedFileUtil.getDuplicateFiles(args.target, args.absolutePath)

    for file, theSameFiles in sameFiles.items():
        print(f'{file},{",".join(theSameFiles)}')



