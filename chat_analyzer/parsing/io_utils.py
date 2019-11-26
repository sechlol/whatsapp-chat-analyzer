import csv
import json





def write_csv(file_name, data):
    with open(file_name + "_data.csv", 'wb') as f:
        csv_file = csv.writer(f)
        csv_file.writerow(data[0].keys())
        for entry in data:
            csv_file.writerow(entry.values())
