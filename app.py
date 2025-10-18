import pandas as pd
import base64
import io
import dash
from dash import dcc, html, Input, Output, State

print("✅ Библиотеки импортированы успешно!")

# Создаем приложение
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Загрузчик данных для анализа промышленности Москвы", 
            style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div([
        html.P("Поддерживаемые форматы: CSV (.csv), Excel (.xlsx, .xls)"),
        html.P("Рекомендуем начинать с CSV для тестирования")
    ], style={'textAlign': 'center', 'margin': '10px'}),
    
    # Компонент для загрузки файлов
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            '📎 Перетащите файл сюда или ',
            html.A('кликните для выбора')
        ]),
        style={
            'width': '80%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '2px', 'borderStyle': 'dashed', 
            'borderRadius': '10px', 'textAlign': 'center', 
            'margin': '20px auto', 'backgroundColor': '#f0f8ff',
            'borderColor': '#4CAF50', 'cursor': 'pointer'
        },
        multiple=False
    ),
    
    # Область для сообщений
    html.Div(id='output-message', style={
        'margin': '20px', 
        'fontSize': '16px',
        'padding': '10px',
        'borderRadius': '5px'
    }),
    
    # Область для предпросмотра данных
    html.Div(id='output-data', style={'margin': '20px'})
])

def parse_file(contents, filename):
    """Улучшенная функция для чтения файлов с проверкой формата"""
    try:
        print(f"🔍 Попытка чтения файла: {filename}")
        
        # Разделяем содержимое файла
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Определяем расширение файла
        file_extension = filename.lower().split('.')[-1]
        print(f"📄 Расширение файла: {file_extension}")
        
        # Пробуем разные методы чтения в зависимости от расширения
        if file_extension == 'csv':
            try:
                # Пробуем читать как CSV
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                print(f"✅ CSV прочитан успешно: {len(df)} строк")
                return df, f"✅ CSV файл '{filename}' успешно загружен! ({len(df)} строк, {len(df.columns)} столбцов)"
            except Exception as csv_error:
                return None, f"❌ Ошибка чтения CSV: {str(csv_error)}"
                
        elif file_extension in ['xlsx', 'xlsm']:
            try:
                # Пробуем читать как современный Excel
                df = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
                print(f"✅ XLSX прочитан успешно: {len(df)} строк")
                return df, f"✅ Excel файл '{filename}' успешно загружен! ({len(df)} строк, {len(df.columns)} столбцов)"
            except Exception as xlsx_error:
                return None, f"❌ Ошибка чтения Excel (XLSX): {str(xlsx_error)}"
                
        elif file_extension == 'xls':
            try:
                # Пробуем читать как старый Excel
                df = pd.read_excel(io.BytesIO(decoded), engine='xlrd')
                print(f"✅ XLS прочитан успешно: {len(df)} строк")
                return df, f"✅ Excel файл '{filename}' успешно загружен! ({len(df)} строк, {len(df.columns)} столбцов)"
            except Exception as xls_error:
                return None, f"❌ Ошибка чтения Excel (XLS): {str(xls_error)}"
                
        else:
            return None, f"❌ Неподдерживаемый формат: .{file_extension}"
            
    except Exception as e:
        error_msg = f"❌ Общая ошибка при чтении файла: {str(e)}"
        print(error_msg)
        return None, error_msg

def create_data_preview(df, filename):
    """Создает красивый предпросмотр данных"""
    return html.Div([
        html.H4("📋 Информация о загруженных данных", 
                style={'color': '#2c3e50', 'marginBottom': '20px'}),
        
        # Карточки с общей информацией
        html.Div([
            html.Div([
                html.Div(f"📁 {filename}", 
                        style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                html.Div(f"Формат: {', '.join([str(dtype) for dtype in df.dtypes.unique()])}",
                        style={'fontSize': '14px', 'color': '#666'})
            ], style={'flex': '1', 'padding': '10px'}),
            
            html.Div([
                html.Div(f"📊 {len(df)}", 
                        style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#3498db'}),
                html.Div("строк", style={'fontSize': '14px'})
            ], style={'flex': '1', 'padding': '10px', 'textAlign': 'center'}),
            
            html.Div([
                html.Div(f"🏷️ {len(df.columns)}", 
                        style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#e74c3c'}),
                html.Div("столбцов", style={'fontSize': '14px'})
            ], style={'flex': '1', 'padding': '10px', 'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px',
                  'border': '1px solid #ddd', 'borderRadius': '5px', 'padding': '10px'}),
        
        # Список столбцов
        html.Div([
            html.H5("Столбцы данных:", style={'marginBottom': '10px'}),
            html.Ul([html.Li(f"{col} ({df[col].dtype})") for col in df.columns],
                   style={'columns': '2', 'fontSize': '14px'})
        ], style={'marginBottom': '20px'}),
        
        html.Hr(),
        
        # Предпросмотр данных
        html.H5("🔍 Предпросмотр данных (первые 5 строк):"),
        html.Table([
            # Заголовок таблицы
            html.Thead([
                html.Tr([html.Th(col, style={
                    'border': '1px solid #ddd', 
                    'padding': '8px',
                    'backgroundColor': '#34495e',
                    'color': 'white',
                    'textAlign': 'left'
                }) for col in df.columns])
            ]),
            # Данные таблицы
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][col], style={
                    'border': '1px solid #ddd', 
                    'padding': '8px',
                    'backgroundColor': '#f8f9fa' if i % 2 == 0 else 'white'
                }) for col in df.columns])
                for i in range(min(5, len(df)))
            ])
        ], style={
            'width': '100%', 
            'borderCollapse': 'collapse',
            'marginTop': '10px',
            'fontSize': '14px'
        }),
        
        html.Div(f"* Показано первых 5 строк из {len(df)}", 
                style={'fontSize': '12px', 'color': '#666', 'marginTop': '10px'})
    ])

@app.callback(
    [Output('output-message', 'children'),
     Output('output-data', 'children')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    """Обработчик загрузки файлов"""
    if contents is not None and filename is not None:
        df, message = parse_file(contents, filename)
        
        if df is not None:
            # Успешная загрузка
            preview = create_data_preview(df, filename)
            return html.Div(message, style={'color': 'green', 'fontWeight': 'bold'}), preview
        else:
            # Ошибка загрузки
            return html.Div(message, style={'color': 'red', 'fontWeight': 'bold'}), ""
    
    return html.Div("📁 Ожидание загрузки файла...", style={'color': '#666'}), ""

if __name__ == '__main__':
    print("🚀 Запуск приложения...")
    print("📖 Откройте браузер и перейдите по адресу: http://127.0.0.1:8050/")
    app.run(debug=True)