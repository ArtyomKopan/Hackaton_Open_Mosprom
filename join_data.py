import pandas as pd
from typing import Optional
import pytest


def join_csv_and_api_data(
        df_csv: Optional[pd.DataFrame],
        df_api: Optional[pd.DataFrame],
        key: str = 'ИНН'
) -> pd.DataFrame:
    """

    Args:
        df_csv: данные, прочитанные из файла
        df_api: данные, прочитанные через api

    Returns:
        датафрейм, полученный из объединения df_csv и df_api по столбцу ИНН по следующему правилу:
        1. Если имена столбцов в df_csv и df_api совпадают, то берутся данные из df_api
        2. Столбцы, которые есть только в одном датафрейме, остаются без изменений

    """
    if df_csv is None:
        return df_api
    if df_api is None:
        return df_csv

    if key not in df_csv.columns or key not in df_api.columns:
        raise ValueError(f"Ключ '{key}' должен присутствовать в обоих датафреймах.")

    common_columns = df_csv.columns.intersection(df_api.columns).difference([key])

    df_merged = pd.merge(df_csv, df_api, on=key, how='outer', suffixes=('_left', '_right'))

    for col in common_columns:
        df_merged[col] = df_merged[f'{col}_right'].fillna(df_merged[f'{col}_left'])
        df_merged.drop(columns=[f'{col}_left', f'{col}_right'], inplace=True)

    return df_merged


