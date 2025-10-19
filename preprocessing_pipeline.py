import pandas as pd


def read_csv_data(filename: str) -> Optional[pd.DataFrame]:
    for sep in [',', ';', '\t']:
        for encoding in ['utf-8', '1251']:
            try:
                csv_data = pd.read_csv(filename, sep=sep, encoding=encoding)
                return csv_data
            except:
                continue

    return None


def remove_columns_without_values(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_remove = []
    for column in df.columns:
        column_values = set(df[column])
        if len(column_values) == 1 and list(column_values)[0] == 'ДАННЫЕ ОТСУТСТВУЮТ В API':
            columns_to_remove.append(column)

    df = df.drop(columns_to_remove, axis=1)

    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_columns_without_values(df)
    df = df.drop_duplicates()

    return df
