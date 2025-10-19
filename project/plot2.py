import re

import pandas as pd


def sum_revenue_for_org_in_period(df: pd.DataFrame, org_name: str, start_year: int, end_year: int, org_column="Наименование организации"):
    # Фильтруем строки по организации
    df_filtered = df[df[org_column] == org_name]
    # Находим подходящие колонки с выручкой и годом
    revenue_cols = []
    for col in df.columns:
        if 'выручка' in col.lower():
            match = re.search(r'(\d{4})', col)
            if match:
                year = int(match.group(1))
                if start_year <= year <= end_year:
                    revenue_cols.append(col)

    # Суммируем выручку по отфильтрованным колонкам
    total_revenue = df_filtered[revenue_cols].sum().sum()
    return total_revenue


def sum_revenue_for_industry_in_period(df: pd.DataFrame, industry_name: str, start_year: int, end_year: int, industry_column="Основная отрасль"):
    # Фильтрация по отрасли (индустрии)
    df_filtered = df[df[industry_column] == industry_name]
    print(df_filtered)
    # Поиск колонок с выручкой и годом
    revenue_cols = []
    for col in df.columns:
        if 'выручка' in col.lower():
            match = re.search(r'(\d{4})', col)
            if match:
                year = int(match.group(1))
                if start_year <= year <= end_year:
                    revenue_cols.append(col)

    # Суммирование значений выручки по выбранным колонкам и отфильтрованным строкам
    total_revenue = df_filtered[revenue_cols].sum().sum()
    print(total_revenue)
    return total_revenue


def universal_search(df: pd.DataFrame, industry_name: str, start_year: int, end_year: int, typeof_column="", metric=''):
    # Фильтрация по отрасли (индустрии)
    df_filtered = df[df[typeof_column] == industry_name]
    print(df_filtered)
    # Поиск колонок с выручкой и годом
    revenue_cols = []
    for col in df.columns:
        if metric in col.lower():
            match = re.search(r'(\d{4})', col)
            if match:
                year = int(match.group(1))
                if start_year <= year <= end_year:
                    revenue_cols.append(col)

    # Суммирование значений выручки по выбранным колонкам и отфильтрованным строкам
    total_revenue = df_filtered[revenue_cols].sum().sum()
    print(total_revenue)
    return total_revenue


def sum_column(column):
    df = pd.read_csv("industrial_registry.csv")
    revenue_cols = []
    for col in df.columns:
        if column in col.lower():
            revenue_cols.append(col)
    return df[revenue_cols].sum().sum()


# print(sum_revenue_for_industry_in_period(pd.read_csv("industrial_registry.csv"), "Машиностроение", 2015, 2019))
# print(sum_revenue_for_org_in_period(pd.read_csv("industrial_registry.csv"), "ООО «ВстатьПром»", 2015, 2019))



