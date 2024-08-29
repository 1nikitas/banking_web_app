import streamlit as st
import pandas as pd


class TinkoffCSVParser:
    """
    Класс для парсинга и базовой обработки CSV файлов.
    """

    def __init__(self, file):
        self.file = file
        self.data = None
        self.filtered_data = None  # Добавим переменную для отфильтрованных данных
        self.transfers_to_self = None  # Добавим переменную для переводов "самому себе"

    def load_data(self):
        """
        Загружает данные из CSV файла.
        """
        try:
            self.data = pd.read_csv(self.file, encoding='windows-1251', delimiter=';')
            st.write("Загруженные данные (первые 5 строк):")
            st.write(self.data.head())  # Отобразить первые 5 строк данных
            return self.data
        except pd.errors.EmptyDataError:
            st.error("CSV файл пуст. Пожалуйста, загрузите файл с данными.")
            return None
        except pd.errors.ParserError:
            st.error("Ошибка парсинга CSV файла. Проверьте правильность разделителя и формат файла.")
            return None
        except UnicodeDecodeError:
            st.error("Ошибка декодирования файла. Убедитесь, что файл сохранен в правильной кодировке.")
            return None
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {e}")
            return None

    def preprocess_data(self):
        """
        Выполняет предварительную обработку данных.
        """
        if self.data is None:
            st.error("Данные не были загружены. Убедитесь, что файл загружен правильно.")
            return None

        try:
            # Преобразование колонок с датой в формат datetime
            self.data['Дата операции'] = pd.to_datetime(self.data['Дата операции'], format='%d.%m.%Y %H:%M:%S')
            self.data['Дата платежа'] = pd.to_datetime(self.data['Дата платежа'], format='%d.%m.%Y')

            # Преобразование числовых значений в правильный формат
            self.data['Сумма операции'] = self.data['Сумма операции'].str.replace(',', '.').astype(float)
            self.data['Сумма платежа'] = self.data['Сумма платежа'].str.replace(',', '.').astype(float)
            self.data['Сумма операции с округлением'] = self.data['Сумма операции с округлением'].str.replace(',', '.').astype(float)

            # Проверяем, что значения в колонке 'Кэшбэк' являются строками, и заменяем запятые на точки
            self.data['Кэшбэк'] = self.data['Кэшбэк'].astype(str).str.replace(',', '.').replace('nan', '0').astype(float)

            # Определение переводов "самому себе"
            self.transfers_to_self = self.data[(self.data['Категория'] == 'Переводы') & 
                                               (self.data['Описание'].str.contains("самому себе", case=False, na=False) | 
                                                self.data['Описание'].str.contains("между своими счетами", case=False, na=False))]

            # Исключение переводов "самому себе" из анализа
            self.filtered_data = self.data[~self.data.index.isin(self.transfers_to_self.index) & (self.data['Категория'] != 'Переводы')].copy()

            return self.filtered_data
        except KeyError as e:
            st.error(f"Ошибка обработки данных: отсутствует ожидаемая колонка {e}")
            return None
        except ValueError as e:
            st.error(f"Ошибка преобразования данных: {e}")
            return None
        except Exception as e:
            st.error(f"Неожиданная ошибка: {e}")
            return None
