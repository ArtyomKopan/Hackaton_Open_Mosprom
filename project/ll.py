import  pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


#data.columns = data.columns.str.lower().str.replace(' ', '_')

# Отфильтруем только числовые столбцы



def find_by_column(column):
    data = pd.read_csv('industrial_registry.csv', encoding="utf-8", sep=',')
    # Выбираем только нужные колонки из списка
    columns = data.columns
    # Оставляем только те колонки, которые есть в числовых данных
    cols_to_use = [col for col in columns if col == column]

    # Создаем подтаблицу с числовыми данными
    subset_data = data[cols_to_use]
    return data[column]






