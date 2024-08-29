class SpendingAnalyzer:
    """
    Класс для анализа данных о расходах.
    """

    def __init__(self, data):
        self.data = data
        self.spending_by_category = None
        self.filtered_data = None
        self.frequent_purchases = None
        self.transfers_to_self = None
        self.transfers_to_others = None

    def analyze_spending(self):
        """
        Analyzes spending by category, excluding "self-transfers".
        """
        # Exclude self-transfers and intra-account transfers from analysis
        self.filtered_data = self.data[self.data['Категория'] != 'Переводы'].copy()

        # Recalculate data by category, excluding transfers
        self.spending_by_category = self.filtered_data[self.filtered_data['Сумма операции'] < 0].groupby('Категория')['Сумма операции'].sum().sort_values(ascending=False)
        
        # Filter for transfers to self
        self.transfers_to_self = self.data.loc[(self.data['Категория'] == 'Переводы') & 
                                            (self.data['Описание'].str.contains("самому себе", case=False, na=False) | 
                                                self.data['Описание'].str.contains("между своими счетами", case=False, na=False))]

        # Debugging: Print the number of matching rows
        print(f"Number of 'transfers to self' rows: {self.transfers_to_self.shape[0]}")

        # Filter for transfers to others
        self.transfers_to_others = self.data.loc[(self.data['Категория'] == 'Переводы') & 
                                                ~self.data.index.isin(self.transfers_to_self.index)]

        # Debugging: Print the number of matching rows
        print(f"Number of 'transfers to others' rows: {self.transfers_to_others.shape[0]}")

        return self.spending_by_category.abs(), self.filtered_data

    def analyze_frequent_purchases(self):
        """
        Анализирует наиболее частые покупки.
        """
        self.frequent_purchases = self.filtered_data['Категория'].value_counts().head(5)
        return self.frequent_purchases

    def calculate_basket_cost(self):
        """
        Рассчитывает примерную стоимость дневной, недельной и месячной корзины потребителя.
        """
        daily_cost = self.filtered_data.groupby('Категория')['Сумма операции'].mean().sum()
        weekly_cost = daily_cost * 7
        monthly_cost = daily_cost * 30
        
        return daily_cost, weekly_cost, monthly_cost
