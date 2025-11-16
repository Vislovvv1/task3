import csv
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    INCOME = "Доход"
    EXPENSE = "Расход"


class Category:
    """
    Класс описывает категорию доходов/расходов
    """

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.name} ({self.type.value})"

    def __repr__(self):
        return f"Category(name='{self.name}', type={self.type})"


class Transaction:
    """
    Класс описывает финансовую операцию
    """

    def __init__(self, amount, category, date, description=""):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def __str__(self):
        return f"Transaction: {self.amount} руб. ({self.category.name}) - {self.date}"

    def __repr__(self):
        return f"Transaction(amount={self.amount}, category='{self.category.name}', date='{self.date}')"


class FinanceManager:
    """
    Класс управляет операциями и файловыми операциями
    """

    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self.transactions = []
        self.categories = [
            Category("Зарплата", TransactionType.INCOME),
            Category("Инвестиции", TransactionType.INCOME),
            Category("Продукты", TransactionType.EXPENSE),
            Category("Транспорт", TransactionType.EXPENSE),
            Category("Развлечения", TransactionType.EXPENSE),
            Category("Жилье", TransactionType.EXPENSE),
            Category("Здоровье", TransactionType.EXPENSE),
            Category("Образование", TransactionType.EXPENSE)
        ]
        self.load_from_file()

    def add_transaction(self, transaction):
        """Добавляет новую транзакцию"""
        self.transactions.append(transaction)
        self.save_to_file()

    def delete_transaction(self, index):
        """Удаляет транзакцию по индексу"""
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
            self.save_to_file()
            return True
        return False

    def get_balance(self):
        """Рассчитывает текущий баланс"""
        income = sum(t.amount for t in self.transactions
                     if t.category.type == TransactionType.INCOME)
        expenses = sum(t.amount for t in self.transactions
                       if t.category.type == TransactionType.EXPENSE)
        return income - expenses

    def get_income_total(self):
        """Возвращает общую сумму доходов"""
        return sum(t.amount for t in self.transactions
                   if t.category.type == TransactionType.INCOME)

    def get_expenses_total(self):
        """Возвращает общую сумму расходов"""
        return sum(t.amount for t in self.transactions
                   if t.category.type == TransactionType.EXPENSE)

    def get_category_summary(self):
        """Возвращает аналитику по категориям"""
        summary = {}
        for transaction in self.transactions:
            cat_name = transaction.category.name
            if cat_name not in summary:
                summary[cat_name] = 0
            if transaction.category.type == TransactionType.INCOME:
                summary[cat_name] += transaction.amount
            else:
                summary[cat_name] -= transaction.amount
        return summary

    def get_transactions_by_category(self, category_name):
        """Возвращает все транзакции по указанной категории"""
        return [t for t in self.transactions if t.category.name == category_name]

    def save_to_file(self):
        """Сохраняет все транзакции в CSV файл"""
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Amount', 'Category', 'Type', 'Date', 'Description'])
                for transaction in self.transactions:
                    writer.writerow([
                        transaction.amount,
                        transaction.category.name,
                        transaction.category.type.value,
                        transaction.date,
                        transaction.description
                    ])
            print(f"Данные сохранены в файл: {self.filename}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def load_from_file(self):
        """Загружает транзакции из CSV файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.transactions = []  # Очищаем текущие транзакции

                for row in reader:
                    category = next((cat for cat in self.categories
                                     if cat.name == row['Category']), None)
                    if category:
                        transaction = Transaction(
                            amount=float(row['Amount']),
                            category=category,
                            date=row['Date'],
                            description=row['Description']
                        )
                        self.transactions.append(transaction)

                print(f"Загружено {len(self.transactions)} транзакций из файла: {self.filename}")

        except FileNotFoundError:
            print(f"Файл {self.filename} не найден. Будет создан новый при сохранении.")
            self.transactions = []
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            self.transactions = []

    def add_category(self, name, type):
        """Добавляет новую категорию"""
        new_category = Category(name, type)
        self.categories.append(new_category)
        return new_category

    def get_categories_by_type(self, type):
        """Возвращает категории по типу (доход/расход)"""
        return [cat for cat in self.categories if cat.type == type]