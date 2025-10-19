import pandas as pd
import re
import plotly.graph_objects as go

# Ключевые слова для поиска колонок
keywords = [
    'Фонд оплаты труда',
    'численность персонала',
    'выручка',
    'налоги',
    'территориальное расположение'
]


# Функция поиска колонок по ключевым словам
def find_columns_by_keywords(df, keywords):
    matched_columns = {}
    for keyword in keywords:
        matched_columns[keyword] = []
        for col in df.columns:
            col_lower = col.lower()
            if keyword.lower() in col_lower:
                matched_columns[keyword].append(col)
    return matched_columns


# Функция для извлечения года из названия колонки
def extract_year(column_name):
    match = re.search(r'(\d{4})', column_name)
    if match:
        year = int(match.group(1))
        if 2000 <= year <= 2025:
            return year
    return None


def filter_values(df: pd.DataFrame, filter_column: str, filter_value: str) -> pd.DataFrame:
    return df[df[filter_column] == filter_value]


def build_plot(data: pd.DataFrame, min_year: int = 2017, max_year: int = 2025):
    # Заполняем пропуски в числовых колонках средним значением соседних
    for column in data.select_dtypes(include='number').columns:
        values = data[column].values
        for idx in range(len(data)):
            if pd.isnull(values[idx]):
                # ищем слева
                left_idx = idx - 1
                while left_idx >= 0 and pd.isnull(values[left_idx]):
                    left_idx -= 1
                # ищем справа
                right_idx = idx + 1
                while right_idx < len(values) and pd.isnull(values[right_idx]):
                    right_idx += 1

                left_value = values[left_idx] if left_idx >= 0 else None
                right_value = values[right_idx] if right_idx < len(values) else None

                # если есть оба значения, берём среднее
                if left_value is not None and right_value is not None:
                    values[idx] = (left_value + right_value) / 2
                elif left_value is not None:
                    values[idx] = left_value
                elif right_value is not None:
                    values[idx] = right_value
        data[column] = values

    # Получаем колонки по ключевым словам
    columns_by_keyword = find_columns_by_keywords(data, keywords)

    fig = go.Figure()
    # Построение графиков с Plotly, соединяя все точки линиями по каждому ключу
    for key, cols in columns_by_keyword.items():
        x_points = []
        y_points = []

        for col in cols:
            year = extract_year(col)
            if year:
                value = data.iloc[0][col]
                if pd.notnull(value):
                    x_points.append(year)
                    y_points.append(value)

        # Фильтруем x_points и y_points по годам
        try:
            min_year = max(min_year, x_points[0])
            max_year = min(max_year, x_points[-1])
            min_year_idx, max_year_idx = x_points.index(min_year), x_points.index(max_year)
            x_points = x_points[min_year_idx:max_year_idx + 1]
            y_points = y_points[min_year_idx:max_year_idx + 1]

            # Строим линию, соединяющую все точки этой категории
            fig.add_trace(go.Scatter(
                x=x_points,
                y=y_points,
                mode='lines+markers',
                name=key
            ))
        except:
            continue

    fig.write_image('plot.png')
