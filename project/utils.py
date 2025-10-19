import pandas as pd
def parse_file(file):
    """Улучшенная функция для чтения файлов с проверкой формата"""
    try:
        print(f"🔍 Попытка чтения файла: {file}")

        # Определяем расширение файла
        file_extension = file.filename.lower().split('.')[-1]
        print(f"📄 Расширение файла: {file_extension}")

        print(file_extension == "xlsx")
        # Пробуем разные методы чтения в зависимости от расширения
        if file_extension == 'csv':
            try:
                # Пробуем читать как CSV
                df = pd.read_csv(file)
                print(df)
                print(f"✅ CSV прочитан успешно: {len(df)} строк")
                return df, f"✅ CSV файл '{file.filename}' успешно загружен! ({len(df)} строк, {len(df.columns)} столбцов)"
            except Exception as csv_error:
                return None, f"❌ Ошибка чтения CSV: {str(csv_error)}"

        elif file_extension in ['xlsx', 'xlsm']:
            print("Before error" + "xlsx")
            df = pd.read_excel(file)
            print(df)
            print(f"✅ XLSX прочитан успешно: {len(df)} строк")
            return df, f"✅ Excel файл '{file.filename}' успешно загружен! ({len(df)} строк, {len(df.columns)} столбцов)"

        elif file_extension == 'xls':
            try:
                # Пробуем читать как старый Excel
                df = pd.read_excel(file.filename, engine='xlrd')
                print(f"✅ XLS прочитан успешно: {len(df)} строк")
                return df, f"✅ Excel файл '{file.filename}' успешно загружен! ({len(df)} строк, {len(df.columns)} столбцов)"
            except Exception as xls_error:
                return None, f"❌ Ошибка чтения Excel (XLS): {str(xls_error)}"

        else:
            return None, f"❌ Неподдерживаемый формат: .{file_extension}"

    except Exception as e:
        error_msg = f"❌ Общая ошибка при чтении файла: {str(e)}"
        print(error_msg)
        return None, error_msg


def sum_by_period(row_name, organization_name, start_year, end_year):
    """
    Вычисляет выручку заданной организации за указанный период.

    Args:
        filename: путь к файлу с данными (например, CSV)
        organization_name: название организации (строка, частичное совпадение)
        start_year: год начала периода (int)
        end_year: год конца периода (int)

    Returns:
        float: сумма выручки за период
    """
    import pandas as pd
    import re
    df = pd.read_csv("industrial_registry.csv", encoding='cp1251', sep=";")

    # Фильтруем строку по частичному совпадению названия организации
    org_row = df[df['Наименование организации'].str.contains(organization_name, case=False, na=False)]

    if org_row.empty:
        return 0  # Организация не найдена

    total_revenue = 0

    # Ищем колонки по годам с упоминанием выручки
    for column_name in df.columns:
        year_match = re.search(r'(20\\d{2})', str(column_name))
        if not year_match:
            continue
        year_value = int(year_match.group(1))

        if start_year <= year_value <= end_year and row_name in column_name.lower():
            column_values = pd.to_numeric(org_row[column_name], errors='coerce').dropna()
            total_revenue += column_values.sum()

    return total_revenue