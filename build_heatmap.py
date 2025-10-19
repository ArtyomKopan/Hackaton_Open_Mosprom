import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
import geopandas as gpd
from geopy.geocoders import Nominatim
import time
import re


# Функция для получения последнего доступного значения метрики
def get_latest_metric_value(row, metric_prefix):
    """
    Получает последнее доступное значение метрики по префиксу
    """
    years = range(2025, 2016, -1)

    for year in years:
        column_name = f"{metric_prefix} {year}"
        if column_name in row.index and pd.notna(row[column_name]):
            return row[column_name]

    return None


# Подготовка данных для тепловых карт
def prepare_heatmap_data(df, metrics_config):
    """
    Подготавливает данные для построения тепловых карт
    """
    heatmap_data = {}

    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        return

    for metric_name, metric_config in metrics_config.items():
        metric_data = []

        for idx, row in df.iterrows():
            lat, lon = row['latitude'], row['longitude']

            value = get_latest_metric_value(row, metric_config['prefix'])

            if value is not None and lat is not None and lon is not None:
                metric_data.append({
                    'lat': lat,
                    'lon': lon,
                    'value': value,
                    'organization': row['Наименование организации'],
                    'address': row['Адрес производства']
                })

        heatmap_data[metric_name] = pd.DataFrame(metric_data)

    return heatmap_data


# Функция создания тепловой карты
def create_metric_heatmap(metric_df, metric_name, metric_config, output_file):
    """
    Создает тепловую карту для конкретной метрики
    """
    if metric_df.empty:
        print(f"Нет данных для метрики: {metric_name}")
        return None

    # Создаем базовую карту Москвы
    moscow_center = [55.7558, 37.6173]
    m = folium.Map(location=moscow_center, zoom_start=10, tiles='OpenStreetMap')

    # Подготавливаем данные для тепловой карты
    heat_data = [[row['lat'], row['lon'], row['value']] for _, row in metric_df.iterrows()]

    # Нормализуем значения для лучшего отображения
    values = [point[2] for point in heat_data]
    if values:
        max_val = max(values)
        normalized_heat_data = [[point[0], point[1], point[2] / max_val] for point in heat_data]
    else:
        normalized_heat_data = heat_data

    # Добавляем тепловую карту
    HeatMap(
        normalized_heat_data,
        min_opacity=0.2,
        max_opacity=0.8,
        radius=15,
        blur=10,
        gradient={
            0.2: 'blue',
            0.4: 'cyan',
            0.6: 'lime',
            0.8: 'yellow',
            1.0: 'red'
        }
    ).add_to(m)

    # Добавляем маркеры для точек
    for _, row in metric_df.iterrows():
        # Определяем цвет маркера на основе значения
        value = row['value']
        if values:
            normalized_value = value / max_val
            if normalized_value > 0.8:
                color = 'red'
            elif normalized_value > 0.6:
                color = 'orange'
            elif normalized_value > 0.4:
                color = 'green'
            elif normalized_value > 0.2:
                color = 'lightblue'
            else:
                color = 'blue'
        else:
            color = 'blue'

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6,
            popup=folium.Popup(
                f"<b>{row['organization']}</b><br>"
                f"{metric_config['description']}: {value:,.0f}<br>"
                f"Адрес: {row['address']}",
                max_width=300
            ),
            color='black',
            fill_color=color,
            fill=True,
            fill_opacity=0.7,
            weight=1
        ).add_to(m)

    # Добавляем заголовок
    title_html = '''
                 <h3 align="center" style="font-size:20px"><b>Тепловая карта: {}</b></h3>
                 <p align="center">{}</p>
                 '''.format(metric_name, metric_config['description'])
    m.get_root().html.add_child(folium.Element(title_html))

    # Сохраняем карту
    m.save(output_file)
    print(f"Тепловая карта '{metric_name}' сохранена в файл: {output_file}")

    return m


def create_heatmaps(df):
    metrics_config = {
        'Фонд оплаты труда': {
            'prefix': 'Фонд оплаты труда всех сотрудников организации, тыс. руб',
            'description': 'Фонд оплаты труда (тыс. руб.)'
        },
        'Численность персонала': {
            'prefix': 'Среднесписочная численность персонала (всего по компании), чел',
            'description': 'Численность персонала (чел.)'
        },
        'Выручка': {
            'prefix': 'Выручка предприятия, тыс. руб.',
            'description': 'Выручка (тыс. руб.)'
        },
        'Налоги': {
            'prefix': 'Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб.',
            'description': 'Налоги в бюджет Москвы (тыс. руб.)'
        }
    }

    heatmap_data = prepare_heatmap_data(df, metrics_config)

    for metric_name, metric_df in heatmap_data.items():
        if not metric_df.empty:
            output_file = f'heatmap_{metric_name.replace(" ", "_").lower()}.html'
            create_metric_heatmap(
                metric_df,
                metric_name,
                metrics_config[metric_name],
                output_file
            )
