#   Copyright 2024 hidenorly
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

import os
import re
import argparse

def count_files(directory, file_pattern):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file_pattern or re.search(file_pattern, file):
                file_count += 1
    return file_count

def report_csv(file_writer, data={}):
    for key, value in data.items():
        line = f"{key},{value}"
        if file_writer:
            file_writer.write(line+"\n")
        else:
            print(line)

def report_md(file_writer, data={}):
    for key, value in data.items():
        line = f"| {key} | {value} |"
        if file_writer:
            file_writer.write(line+"\n")
        else:
            print(line)

def generate_report(directory, output_file, file_pattern, dont_output_if_zero = False, min_level=0, max_level = None, format="csv"):
    report = []
    if max_level!=None:
        max_level = max_level + 1
    for root, dirs, files in os.walk(directory):
        level = len(root.split("/"))
        if (not max_level or level<=max_level) and level>min_level:
            folder_name = os.path.relpath(root, directory)
            file_count = count_files(root, file_pattern)
            report.append((folder_name, file_count))

    file_writer = None
    if output_file:
        file_writer = open(output_file, 'w', newline='')
    reporter = report_csv
    if format=="md":
        reporter = report_md

    for folder_name, file_count in report:
        if not dont_output_if_zero or file_count:
            data = {}
            data[folder_name] = file_count
            reporter(file_writer, data)

    if file_writer:
        file_writer.close()
        file_writer = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="target_directory", default=".", help="Target Directory")
    parser.add_argument("-o", dest="output_file", help="CSV file to output the results")
    parser.add_argument("-f", dest="file_pattern", default=None, help="Regular expression pattern for file matching")
    parser.add_argument("-n", dest="no_zero", default=False, action="store_true", help="Set if excludes 0 file count directory")
    parser.add_argument("-m", dest="max_level", type=int, default=None, help="Max depth (default:infinite)")
    parser.add_argument("-i", dest="min_level", type=int, default=0, help="Min depth (default:0)")
    parser.add_argument("-r", dest="format", default="csv", help="csv or md")
    args = parser.parse_args()

    generate_report(args.target_directory, args.output_file, args.file_pattern, args.no_zero, args.min_level, args.max_level, args.format)



