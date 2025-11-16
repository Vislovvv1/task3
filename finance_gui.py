import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from finance_classes import Transaction, Category, FinanceManager, TransactionType


class FinanceApp:
    def __init__(self, root):
        # Используем три основных класса
        self.manager = FinanceManager()  # FinanceManager управляет операциями
        self.root = root
        self.root.title("Учет личных финансов - Three Classes Demo")
        self.root.geometry("900x700")
        self.setup_ui()

    def setup_ui(self):
        # Заголовок с описанием архитектуры
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(title_frame, text="Приложение демонстрирует три основных класса:",
                  font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        ttk.Label(title_frame, text="Transaction (операции), Category (категории), FinanceManager (управление)",
                  font=('Arial', 9)).pack(anchor=tk.W)

        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавить операцию (класс Transaction)", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Поля ввода
        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Категория (класс Category):").grid(row=1, column=0, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var)
        categories = [cat.name for cat in self.manager.categories]  # Используем категории из FinanceManager
        self.category_combo['values'] = categories
        self.category_combo.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky=tk.W)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Описание:").grid(row=3, column=0, sticky=tk.W)
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопки
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Создать Transaction",
                   command=self.add_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить Transaction",
                   command=self.delete_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Аналитика FinanceManager",
                   command=self.show_analytics).pack(side=tk.LEFT, padx=5)

        # Информация о балансе
        info_frame = ttk.LabelFrame(self.root, text="Финансовая информация (FinanceManager методы)", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Создаем фрейм для отображения нескольких показателей
        metrics_frame = ttk.Frame(info_frame)
        metrics_frame.pack(fill=tk.X)

        self.balance_label = ttk.Label(metrics_frame, text="", font=('Arial', 12, 'bold'))
        self.balance_label.pack(side=tk.LEFT, padx=20)

        self.income_label = ttk.Label(metrics_frame, text="", font=('Arial', 10), foreground='green')
        self.income_label.pack(side=tk.LEFT, padx=20)

        self.expense_label = ttk.Label(metrics_frame, text="", font=('Arial', 10), foreground='red')
        self.expense_label.pack(side=tk.LEFT, padx=20)

        self.update_balance()

        # Таблица операций
        table_frame = ttk.LabelFrame(self.root, text="История операций (список Transaction объектов)", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ('#1', '#2', '#3', '#4', '#5')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        self.tree.heading('#1', text='Дата')
        self.tree.heading('#2', text='Категория')
        self.tree.heading('#3', text='Тип')
        self.tree.heading('#4', text='Сумма')
        self.tree.heading('#5', text='Описание')

        self.tree.column('#1', width=100)
        self.tree.column('#2', width=120)
        self.tree.column('#3', width=80)
        self.tree.column('#4', width=100)
        self.tree.column('#5', width=300)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.update_table()

    def add_transaction(self):
        """Создает новый объект Transaction и добавляет его через FinanceManager"""
        try:
            amount = float(self.amount_entry.get())
            category_name = self.category_var.get()
            date = self.date_entry.get()
            description = self.desc_entry.get()

            if not all([amount, category_name, date]):
                messagebox.showwarning("Ошибка", "Заполните обязательные поля!")
                return

            # Проверка формата даты
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
                return

            # Находим объект Category по имени
            category = next((cat for cat in self.manager.categories
                             if cat.name == category_name), None)
            if not category:
                messagebox.showwarning("Ошибка", "Выберите корректную категорию!")
                return

            # СОЗДАЕМ ОБЪЕКТ TRANSACTION
            transaction = Transaction(amount, category, date, description)

            # ДОБАВЛЯЕМ ЧЕРЕЗ FINANCEMANAGER
            self.manager.add_transaction(transaction)

            self.update_table()
            self.update_balance()
            self.clear_inputs()

            messagebox.showinfo("Успех", f"Создана новая транзакция:\n{transaction}")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму!")

    def delete_transaction(self):
        """Удаляет Transaction через FinanceManager"""
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            success = self.manager.delete_transaction(index)
            if success:
                self.update_table()
                self.update_balance()
                messagebox.showinfo("Успех", "Транзакция удалена")
        else:
            messagebox.showwarning("Ошибка", "Выберите операцию для удаления!")

    def show_analytics(self):
        """Показывает аналитику через методы FinanceManager"""
        summary = self.manager.get_category_summary()
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("Аналитика по категориям (FinanceManager)")
        analytics_window.geometry("400x500")

        if not summary:
            ttk.Label(analytics_window, text="Нет данных для анализа").pack(padx=10, pady=10)
            return

        # Заголовок
        ttk.Label(analytics_window, text="Сводка по категориям:",
                  font=('Arial', 11, 'bold')).pack(pady=10)

        for category, amount in summary.items():
            color = "green" if amount >= 0 else "red"
            ttk.Label(analytics_window,
                      text=f"{category}: {amount:+.2f} руб.",
                      foreground=color,
                      font=('Arial', 10)).pack(padx=20, pady=2, anchor=tk.W)

    def update_table(self):
        """Обновляет таблицу с Transaction объектами"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for transaction in self.manager.transactions:
            amount_color = "green" if transaction.category.type == TransactionType.INCOME else "red"
            self.tree.insert('', tk.END, values=(
                transaction.date,
                transaction.category.name,
                transaction.category.type.value,
                f"{transaction.amount:.2f}",
                transaction.description
            ))

    def update_balance(self):
        """Обновляет финансовые показатели через FinanceManager"""
        balance = self.manager.get_balance()
        income = self.manager.get_income_total()
        expenses = self.manager.get_expenses_total()

        balance_color = "green" if balance >= 0 else "red"
        self.balance_label.config(
            text=f"Баланс: {balance:.2f} руб.",
            foreground=balance_color
        )
        self.income_label.config(text=f"Доходы: {income:.2f} руб.")
        self.expense_label.config(text=f"Расходы: {expenses:.2f} руб.")

    def clear_inputs(self):
        """Очищает поля ввода"""
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()