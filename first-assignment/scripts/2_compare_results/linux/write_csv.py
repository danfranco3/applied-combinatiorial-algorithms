#!/usr/bin/env python3
import csv
import os.path
import re


def main():
    baseline_file = "baseline.csv"
    output_file = "final_result.csv"
    result_file = "result.txt"

    write_header = True
    length = 0
    first_line_fields = ['comment', 'baseline makespan', 'your solution makespan',
                         'your solution exec. time', 'initial test', 'move test',
                         'makespan test', 'obstacle test', 'hauler test', 'charging test', 'mission test']

    if (os.path.exists(output_file)):
        write_header = False
        # file = open(output_file)
        file = open(output_file, 'r', newline='', encoding='utf-8')
        reader = csv.reader(file)
        length = len(list(reader)) - 1
        # print(length)

    # file = open(baseline_file)
    file = open(baseline_file, 'r', newline='', encoding='utf-8')
    reader = csv.reader(file)

    temp = []
    inf = []
    for i, row in enumerate(reader):
        # print(row)
        if (i == length):
            try:
                int(row[0])
                # print(row[0])
                temp = row

            except ValueError:
                inf.append(row)
                length += 1

    # print(inf)

    file = open(result_file)
    temp.extend(file.read().split("\n"))

    # print(temp)

    # csvfile=open(output_file, 'a')
    csvfile = open(output_file, 'a', newline='', encoding='utf-8')
    csvwriter = csv.writer(csvfile)
    if (write_header):
        csvwriter.writerow(first_line_fields)
    if (len(inf)):
        csvwriter.writerows(inf)
    if (len(temp)):
        csvwriter.writerow(temp)


if __name__ == "__main__":
    main()
