from preprocessing_pipeline import preprocess_data, read_csv_data
from join_data import join_csv_and_api_data
import pandas as pd
import sys

"""
Параметры программы:
python.exe main_pipeline.py csv_file_name api_file_name
если какой-то файл отсутствует, то вместо его имени передаётся строка "None"
"""
if __name__ == 'main':
    csv_file_name, api_file_name = sys.argv[1], sys.argv[2]
    csv_file_name = None if csv_file_name == "None" else csv_file_name
    api_file_name = None if api_file_name == "None" else api_file_name

    if csv_file_name is not None:
        if '.xls' in csv_file_name or '.xlsx' in csv_file_name:
            csv_data = pd.read_excel(csv_file_name)
        else:
            csv_data = read_csv_data(csv_file_name)
    else:
        csv_data = None

    if api_file_name is not None:
        if '.xls' in api_file_name or '.xlsx' in api_file_name:
            api_data = pd.read_excel(api_file_name)
        else:
            api_data = read_csv_data(api_file_name)
    else:
        api_data = None

    merged_data = join_csv_and_api_data(csv_data, api_data)
    merged_data = preprocess_data(merged_data)

    """
    датафрейм merged_data лежит в оперативке.
    когда мы строим графики, мы не хотим каждый раз заново читать этот 
    файл из csv. Поэтому его не надо сохранять в csv.
    Значит, функции для построения графиков нужно вызывать тоже из этого 
    файла (main_pipeline). Как сделать так, чтобы эта функция вызывалась 
    только после нажатия на кнопку "Построить график"?
    """

