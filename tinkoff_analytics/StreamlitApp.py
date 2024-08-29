import streamlit as st
import pandas as pd

from SpendingAnalyzer import SpendingAnalyzer
from TinkoffCSVParser import TinkoffCSVParser

import plotly.express as px

class StreamlitApp:
    """
    Класс для управления интерфейсом Streamlit.
    """

    def __init__(self):
        self.parser = None
        self.analyzer = None

    def run(self):
        """
        Запускает приложение Streamlit.
        """
        st.set_page_config(layout="wide")
        st.title('Анализ расходов из Тинькофф')

        uploaded_file = st.file_uploader("Загрузите CSV файл", type="csv")

        if uploaded_file is not None:
            st.write("Файл загружен, начинаю обработку...")
            self.parser = TinkoffCSVParser(uploaded_file)
            data = self.parser.load_data()

            if data is not None:
                processed_data = self.parser.preprocess_data()

                if processed_data is not None:
                    self.analyzer = SpendingAnalyzer(processed_data)
                    spending_by_category, filtered_data = self.analyzer.analyze_spending()
                    frequent_purchases = self.analyzer.analyze_frequent_purchases()
                    daily_cost, weekly_cost, monthly_cost = self.analyzer.calculate_basket_cost()
                    transfers_to_self = self.analyzer.transfers_to_self
                    transfers_to_others = self.analyzer.transfers_to_others

                    self.display_results(spending_by_category, filtered_data, frequent_purchases, daily_cost, weekly_cost, monthly_cost, transfers_to_self, transfers_to_others)
                else:
                    st.error("Не удалось обработать данные. Проверьте формат файла.")
            else:
                st.error("Не удалось загрузить данные. Проверьте файл.")

    def display_results(self, spending_by_category, filtered_data, frequent_purchases, daily_cost, weekly_cost, monthly_cost, transfers_to_self, transfers_to_others):
        """
        Отображает результаты анализа в Streamlit.
        """
        col1, col2 = st.columns(2)

        with col1:
            st.header("Реальные траты по категориям (исключая переводы)")
            df_display = spending_by_category.reset_index()
            df_display.columns = ['Категория', 'Сумма операции']
            df_display['Сумма операции'] = pd.to_numeric(df_display['Сумма операции'], errors='coerce')
            st.dataframe(df_display.sort_values(by='Сумма операции', ascending=False))

            # Pie chart for spending by category
            fig = px.pie(df_display, values='Сумма операции', names='Категория', title='Процент расходов по категориям')
            st.plotly_chart(fig)

            st.header("Наиболее частые покупки")
            st.write(frequent_purchases)

            # Bar chart for frequent purchases
            frequent_purchases_df = frequent_purchases.reset_index()
            frequent_purchases_df.columns = ['Категория', 'Количество']
            fig = px.bar(frequent_purchases_df, x='Категория', y='Количество', title='Наиболее частые покупки по категориям')
            st.plotly_chart(fig)

            st.header("Примерная стоимость потребительской корзины")
            st.write(f"Ежедневная: {daily_cost:.2f} RUB")
            st.write(f"Еженедельная: {weekly_cost:.2f} RUB")
            st.write(f"Ежемесячная: {monthly_cost:.2f} RUB")

        with col2:
            st.header("Переводы 'самому себе'")
            st.dataframe(transfers_to_self)

            st.header("Переводы другим людям")
            st.dataframe(transfers_to_others)

            # Line chart for daily spending over time
            if 'Дата операции' in filtered_data.columns and 'Сумма операции' in filtered_data.columns:
                daily_spending = filtered_data.groupby(filtered_data['Дата операции'].dt.date)['Сумма операции'].sum().reset_index()
                daily_spending.columns = ['Дата', 'Сумма операции']
                fig = px.line(daily_spending, x='Дата', y='Сумма операции', title='Ежедневные расходы с течением времени')
                st.plotly_chart(fig)

            # Histogram for spending distribution
            fig = px.histogram(filtered_data, x='Сумма операции', nbins=50, title='Распределение суммы операций')
            st.plotly_chart(fig)


           
