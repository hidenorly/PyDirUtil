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
from duplicateFileEnumerator import DuplicatedFileUtil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='file util', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('target', metavar='PATH', type=str, nargs='+', help='Target path (can specicy multiply)')
    parser.add_argument('-d', '--actualDelete', default=False, action='store_true', help='Set if really want to delete')
    parser.add_argument('-s', '--shorter', default=False, action='store_true', help="Set if want to delete shorter dir name 's one")
    parser.add_argument('-f', '--filename', default=False, action='store_true', help="Set if want to delete shorter filename's one")
    args = parser.parse_args()

    sameFiles = DuplicatedFileUtil.getDuplicateFiles(args.target, True)

    for file, theSameFiles in sameFiles.items():
    	_sameFiles = []
    	_sameFiles.extend( theSameFiles )
    	_sameFiles.append( file )
    	if args.shorter:
    		if args.filename:
    			sortedPaths = sorted(_sameFiles, key=lambda path: (-len(os.path.basename(path)[::-1]), -len(os.path.dirname(path)[::-1])) )
    		else:
    			sortedPaths = sorted(_sameFiles, key=lambda path: (-len(os.path.dirname(path)[::-1]), -len(os.path.basename(path)[::-1])) )
    	else:
    		if args.filename:
    			sortedPaths = sorted(_sameFiles, key=lambda path: (len(os.path.basename(path)[::-1]), len(os.path.dirname(path)[::-1])) )
    		else:
    			sortedPaths = sorted(_sameFiles, key=lambda path: (len(os.path.dirname(path)[::-1]), len(os.path.basename(path)[::-1])) )
    	keepFile = sortedPaths[0]
    	for aCandidateToDelete in sortedPaths:
    		if aCandidateToDelete!=keepFile:
		    	print(f'delete {aCandidateToDelete} due to duplication with {keepFile}')
		    	if args.actualDelete:
		    		try:
			    		os.remove(aCandidateToDelete)
			    	except OSError as e:
			    		print(f'Error {e}')
