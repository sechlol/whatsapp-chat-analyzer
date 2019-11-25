import csv
import json

from typing import List


def write_json(file_name, data):
    with open(file_name + "_data.json", 'w') as f:
        json.dump(data, f)


def write_csv(file_name, data):
    with open(file_name + "_data.csv", 'wb') as f:
        csv_file = csv.writer(f)
        csv_file.writerow(data[0].keys())
        for entry in data:
            csv_file.writerow(entry.values())


def read_json(file_name: str) -> List[str]:
    with open(file_name, mode='r', encoding="utf8") as file:
        return file.readlines()
