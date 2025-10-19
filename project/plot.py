import pandas as pd
import re
import plotly.graph_objects as go
from matplotlib import pyplot as plt

# Ключевые слова для поиска колонок
keywords = [
    'Фонд оплаты труда',
    'численность персонала',
    'выручка',
    'налоги'
    # 'территориальное расположение'
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
def extract_year(column_name, start_year, end_year):
    match = re.search(r'(\d{4})', column_name)
    if match:
        year = int(match.group(1))
        if int(start_year) <= int(year) <= int(end_year):
            return year
    return None


def filter_values(df: pd.DataFrame, filter_column: str, filter_value: str) -> pd.DataFrame:
    return df[df[filter_column] == filter_value]


def build_plot(data: pd.DataFrame, start_year, end_year):
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
            year = extract_year(col, start_year, end_year)
            if year:
                value = data.iloc[0][col]
                if pd.notnull(value):
                    x_points.append(year)
                    y_points.append(value)

        # Строим линию, соединяющую все точки этой категории
        fig.add_trace(go.Scatter(
            x=x_points,
            y=y_points,
            mode='lines+markers',
            name=key
        ))

    return fig.write_image('static/plot.png')


def build_plot2(ind, start_year, end_year, selected_industry):
    import pandas as pd
    import matplotlib.pyplot as plt

    # Загрузка данных
    df = pd.read_csv('industrial_registry.csv', encoding='utf-8')

    # Выбор отрасли
    industry_df = df[df['Основная отрасль'] == selected_industry]

    # Извлечение данных по годам
    years = [i for i in range(start_year, end_year + 1)]

    # Создаем словарь для хранения всех показателей
    metrics = {
        'Налоги': [],
        'Выручка': [],
        'Прибыль': [],
        'ФОТ': [],
        'Численность': []
    }

    for year in years:
        # Налоги
        tax_col = f'Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. {year}'
        if tax_col in df.columns:
            year_tax = industry_df[tax_col].sum() / 1000  # в млн
            metrics['Налоги'].append(year_tax)
        else:
            metrics['Налоги'].append(0)

        # Выручка
        revenue_col = f'Выручка предприятия, тыс. руб. {year}'
        if revenue_col in df.columns:
            year_revenue = industry_df[revenue_col].sum() / 1000000  # в млрд
            metrics['Выручка'].append(year_revenue)
        else:
            metrics['Выручка'].append(0)

        # Прибыль
        profit_col = f'Чистая прибыль (убыток),тыс. руб. {year}'
        if profit_col in df.columns:
            year_profit = industry_df[profit_col].sum() / 1000  # в млн
            metrics['Прибыль'].append(year_profit)
        else:
            metrics['Прибыль'].append(0)

        # Фонд оплаты труда
        salary_col = f'Фонд оплаты труда всех сотрудников организации, тыс. руб {year}'
        if salary_col in df.columns:
            year_salary = industry_df[salary_col].sum() / 1000  # в млн
            metrics['ФОТ'].append(year_salary)
        else:
            metrics['ФОТ'].append(0)

        # Численность персонала
        staff_col = f'Среднесписочная численность персонала (всего по компании), чел {year}'
        if staff_col in df.columns:
            year_staff = industry_df[staff_col].sum()
            metrics['Численность'].append(year_staff)
        else:
            metrics['Численность'].append(0)

    # Создаем отдельные графики для лучшей читаемости
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(f'Показатели предприятий отрасли: {selected_industry}', fontsize=16, y=1.)

    # Цвета для графиков
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # Графики для каждого показателя
    titles = [
        'Налоги, уплаченные\nв бюджет Москвы (млн руб)',
        'Выручка предприятий\n(млрд руб)',
        'Чистая прибыль\n(млн руб)',
        'Фонд оплаты труда\n(млн руб)',
        'Численность персонала\n(человек)'
    ]

    data_keys = ['Налоги', 'Выручка', 'Прибыль', 'ФОТ', 'Численность']

    for i, (key, title, color) in enumerate(zip(data_keys, titles, colors)):
        row = i // 3
        col = i % 3
        ax = axes[row, col]

        data = metrics[key]
        bars = ax.bar(years, data, color=color, width=0.6, alpha=0.8)

        ax.set_title(title, fontsize=12, pad=15)
        ax.set_xticks(years)
        ax.set_xticklabels(years, fontsize=9)

        # Убираем оси как в оригинальном примере
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_alpha(0.3)
        ax.set_yticks([])

        # Добавляем подписи значений с адаптивным позиционированием
        max_value = max(data) if data else 1
        for bar, value in zip(bars, data):
            height = bar.get_height()

            # Форматируем подпись в зависимости от показателя
            if key == 'Выручка':
                label = f'{value:.1f}'
            elif key == 'Численность':
                label = f'{value:.0f}'
            else:
                label = f'{value:.0f}'

            # Позиция текста - выше столбца
            text_y = height + max_value * 0.03
            ax.text(bar.get_x() + bar.get_width() / 2., text_y,
                    label, ha='center', va='bottom', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

    # Убираем последний пустой subplot
    axes[1, 2].set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('static/plot2.png')

#
# build_plot(pd.read_csv("industrial_registry.csv"), 2017, 2019)
# build_plot2(pd.read_csv("industrial_registry.csv"), 2017, 2019)


def build_plot3(industry_name, start_year, end_year):

    # Загрузка данных
    df = pd.read_csv('industrial_registry.csv', encoding='utf-8')

    # Создание графиков
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(f'Показатели предприятия: {industry_name}', fontsize=16, y=1, fontweight='bold')

    # Цветовая схема
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3BB273', '#7768AE']

    # 1. Налоги, уплаченные в бюджет Москвы (млн руб)
    tax_columns = [f'Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. {year}' for year in range(start_year, end_year)]
    tax_data = df[tax_columns].sum() / 1000000  # Конвертация в млн руб

    bars1 = axes[0, 0].bar(range(start_year, end_year), tax_data.values, color=colors[0], edgecolor='white', linewidth=2)
    axes[0, 0].set_title('Налоги, уплаченные в бюджет Москвы (млн руб)', fontweight='bold', pad=20)
    axes[0, 0].set_xticks(range(start_year, end_year))
    # Установка подходящих пределов оси Y для лучшей видимости
    y_min, y_max = tax_data.min(), tax_data.max()
    axes[0, 0].set_ylim(0, y_max * 1.15)
    for i, v in enumerate(tax_data.values):
        axes[0, 0].text(i + 2017, v + y_max * 0.01, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')

    # 2. Выручка предприятия (млрд руб)
    revenue_columns = [f'Выручка предприятия, тыс. руб. {year}' for year in range(start_year, end_year)]
    revenue_data = df[revenue_columns].sum() / 1000000000  # Конвертация в млрд руб

    bars2 = axes[0, 1].bar(range(start_year, end_year), revenue_data.values, color=colors[1], edgecolor='white', linewidth=2)
    axes[0, 1].set_title('Выручка предприятий (млрд руб)', fontweight='bold', pad=20)
    axes[0, 1].set_xticks(range(start_year, end_year))
    y_min, y_max = revenue_data.min(), revenue_data.max()
    axes[0, 1].set_ylim(0, y_max * 1.15)
    for i, v in enumerate(revenue_data.values):
        axes[0, 1].text(i + start_year, v + y_max * 0.01, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')

    # 3. Чистая прибыль (млн руб)
    profit_columns = [f'Чистая прибыль (убыток),тыс. руб. {year}' for year in range(start_year, end_year)]
    profit_data = df[profit_columns].sum() / 1000000  # Конвертация в млн руб

    bars3 = axes[0, 2].bar(range(start_year, end_year), profit_data.values, color=colors[2], edgecolor='white', linewidth=2)
    axes[0, 2].set_title('Чистая прибыль (млн руб)', fontweight='bold', pad=20)
    axes[0, 2].set_xticks(range(start_year, end_year))
    y_min, y_max = profit_data.min(), profit_data.max()
    axes[0, 2].set_ylim(0, y_max * 1.15)
    for i, v in enumerate(profit_data.values):
        axes[0, 2].text(i + start_year, v + y_max * 0.01, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')

    # 4. Фонд оплаты труда (млн руб)
    salary_columns = [f'Фонд оплаты труда всех сотрудников организации, тыс. руб {year}' for year in range(start_year, end_year)]
    salary_data = df[salary_columns].sum() / 1000000  # Конвертация в млн руб

    bars4 = axes[1, 0].bar(range(start_year, end_year), salary_data.values, color=colors[3], edgecolor='white', linewidth=2)
    axes[1, 0].set_title('Фонд оплаты труда (млн руб)', fontweight='bold', pad=20)
    axes[1, 0].set_xticks(range(start_year, end_year))
    y_min, y_max = salary_data.min(), salary_data.max()
    axes[1, 0].set_ylim(0, y_max * 1.15)
    for i, v in enumerate(salary_data.values):
        axes[1, 0].text(i + start_year, v + y_max * 0.01, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')

    # 5. Численность персонала (человек)
    staff_columns = [f'Среднесписочная численность персонала (всего по компании), чел {year}' for year in
                     range(start_year, end_year)]
    staff_data = df[staff_columns].sum()

    bars5 = axes[1, 1].bar(range(start_year, end_year), staff_data.values, color=colors[4], edgecolor='white', linewidth=2)
    axes[1, 1].set_title('Численность персонала (человек)', fontweight='bold', pad=20)
    axes[1, 1].set_xticks(range(start_year, end_year))
    y_min, y_max = staff_data.min(), staff_data.max()
    axes[1, 1].set_ylim(0, y_max * 1.15)
    for i, v in enumerate(staff_data.values):
        axes[1, 1].text(i + start_year, v + y_max * 0.01, f'{v:.0f}', ha='center', va='bottom', fontweight='bold')

    # 6. Средняя зарплата (тыс. руб)
    avg_salary_columns = [f'Средняя з.п. всех сотрудников организации,  тыс.руб. {year}' for year in range(start_year, end_year)]
    avg_salary_data = df[avg_salary_columns].mean()

    bars6 = axes[1, 2].bar(range(start_year, end_year), avg_salary_data.values, color=colors[5], edgecolor='white', linewidth=2)
    axes[1, 2].set_title('Средняя зарплата (тыс. руб)', fontweight='bold', pad=20)
    axes[1, 2].set_xticks(range(start_year, end_year))
    y_min, y_max = avg_salary_data.min(), avg_salary_data.max()
    axes[1, 2].set_ylim(0, y_max * 1.15)
    for i, v in enumerate(avg_salary_data.values):
        axes[1, 2].text(i + 2017, v + y_max * 0.01, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')

    for ax in axes.flat:
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#dddddd')
        ax.spines['bottom'].set_color('#dddddd')
        ax.set_xlabel('Год', fontweight='bold')
        ax.tick_params(axis='x', rotation=0)
        ax.tick_params(axis='y', colors='#666666')

    plt.tight_layout()
    plt.subplots_adjust(top=0.93)
    plt.savefig("static/plot3.png")



def build_plot4():

    # Чтение данных
    df = pd.read_csv('industrial_registry.csv', encoding='utf-8')

    # Создаем график в стиле вашего примера
    fig, ax = plt.subplots(figsize=(12, 8))

    # Группируем данные по основной отрасли и вычисляем среднюю прибыль за 2023 год
    sector_profit = df.groupby('Основная отрасль')['Чистая прибыль (убыток),тыс. руб. 2023'].mean()

    # Сортируем по убыванию прибыли
    sector_profit = sector_profit.sort_values(ascending=False)

    # Цвета для секторов (аналогичные вашему примеру)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']

    # Создаем столбчатую диаграмму
    bars = ax.bar(sector_profit.index, sector_profit.values / 1000, color=colors[:len(sector_profit)])

    # Настройка внешнего вида
    ax.set_ylabel('млн руб.', fontsize=12, fontweight='bold')
    ax.set_xlabel('Отрасли', fontsize=12, fontweight='bold')
    ax.set_title('Прибыль по отраслям', fontsize=16, fontweight='bold', pad=20)

    # Добавляем значения на столбцы
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 5,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')

    # Улучшаем читаемость подписей
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')

    # Убираем рамки
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig("static/plot4.png")

    # Альтернативный вариант - круговая диаграмма (как в вашем примере)
    fig, ax = plt.subplots(figsize=(10, 8))

    # Берем топ-4 отрасли для круговой диаграммы (как в примере)
    top_sectors = sector_profit.head(4)

    # Создаем круговую диаграмму
    wedges, texts, autotexts = ax.pie(top_sectors.values,
                                      labels=top_sectors.index,
                                      autopct='%1.1f%%',
                                      colors=colors[:4],
                                      startangle=90,
                                      textprops={'fontsize': 11})

    # Увеличиваем шрифт для процентов
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    ax.set_title('Распределение прибыли по основным отраслям за выбранный год',
                 fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig("static/plot5.png")

    # Выводим статистику
    print("=== СТАТИСТИКА ПРИБЫЛИ ПО ОТРАСЛЯМ (2023) ===")
    for i, (sector, profit) in enumerate(sector_profit.items(), 1):
        print(f"{i}. {sector}: {profit / 1000:.1f} млн руб.")

    print(
        f"\nОбщая прибыль всех предприятий: {df['Чистая прибыль (убыток),тыс. руб. 2023'].sum() / 1000000:.2f} млн руб.")

build_plot4()