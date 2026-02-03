import os
from collections import defaultdict


def count_file_types(root_directory):
    file_type_count = defaultdict(int)
    for root, _, files in os.walk(root_directory):
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext:
                file_type_count[ext] += 1
            else:
                file_type_count["No Extension"] += 1

    return dict(file_type_count)

root_directory = r"\\ARS-DATA\Archive\HarmelExit\riesel"

file_counts = count_file_types(root_directory)
for ext, count in file_counts.items():
    print(f"* `{ext}`: {count} file(s)")