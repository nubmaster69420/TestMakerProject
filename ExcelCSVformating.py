import csv
from pprint import pprint

import pandas as pd


# Converting Excel file to CSV
def excel2csv(path):
    read_file = pd.read_excel(path)
    read_file.to_csv(f'Data.csv', index=None, header=True)


def getdata(path, delimiter=',', quotechar=';') -> dict:
    if path.endswith('xlsx'):
        excel2csv(path)
        path = 'Data.csv'
    if path.endswith('csv'):
        with open(path, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter, quotechar=quotechar)
            data_tasks = []
            for line in reader:
                data_tasks.append(
                    {
                        'number': int(line['number']),
                        'task': line['task'],
                        'answer': line['answer']
                    }
                )
            return data_tasks
    else:
        # Exit status -1 in case of invalid format
        return -1


if __name__ == '__main__':
    data = getdata('DemoExcelData.csv')
    pprint(data)
