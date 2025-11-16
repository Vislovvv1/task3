from finance_classes import Transaction, Category, FinanceManager, TransactionType


def demonstrate_classes():
    """Демонстрация работы трех основных классов"""
    print("=== ДЕМОНСТРАЦИЯ ТРЕХ ОСНОВНЫХ КЛАССОВ ===\n")

    # 1. Демонстрация класса Category
    print("1. КЛАСС CATEGORY:")
    salary_category = Category("Зарплата", TransactionType.INCOME)
    food_category = Category("Продукты", TransactionType.EXPENSE)

    print(f"   Категория дохода: {salary_category}")
    print(f"   Категория расхода: {food_category}")
    print(f"   Тип категории 'Зарплата': {salary_category.type}")
    print(f"   Тип категории 'Продукты': {food_category.type}")

    # 2. Демонстрация класса Transaction
    print("\n2. КЛАСС TRANSACTION:")
    transaction1 = Transaction(50000, salary_category, "2024-01-15", "Зарплата за январь")
    transaction2 = Transaction(1500, food_category, "2024-01-16", "Покупка продуктов")

    print(f"   Транзакция 1: {transaction1}")
    print(f"   Транзакция 2: {transaction2}")
    print(f"   Сумма транзакции: {transaction1.amount} руб.")
    print(f"   Категория транзакции: {transaction1.category.name}")

    # 3. Демонстрация класса FinanceManager
    print("\n3. КЛАСС FINANCEMANAGER:")
    manager = FinanceManager("demo_transactions.csv")

    # Добавляем демо-транзакции
    manager.add_transaction(transaction1)
    manager.add_transaction(transaction2)

    print(f"   Общее количество транзакций: {len(manager.transactions)}")
    print(f"   Текущий баланс: {manager.get_balance():.2f} руб.")
    print(f"   Общий доход: {manager.get_income_total():.2f} руб.")
    print(f"   Общий расход: {manager.get_expenses_total():.2f} руб.")

    # Аналитика по категориям
    print("\n   Аналитика по категориям:")
    summary = manager.get_category_summary()
    for category, amount in summary.items():
        print(f"     {category}: {amount:+.2f} руб.")

    print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")


if __name__ == "__main__":
    demonstrate_classes()