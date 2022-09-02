import datetime as dt


# Давайте оформим Docstrings для классов и функций
class Record:
    # Для значения по умолчанию date лучше использовать None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Необходимо исправить форматирование, либо перейти к блоку if/else
        self.date = (
            dt.datetime.now().date() if
            # И здесь проводить проверку if date is None
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


# Давайте оформим Docstrings для классов и функций
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    # Каждый вызов функции будет проходиться по всем записям.
    # Предлагаю сделать в классе словарь в котором будут хранится
    # суммы на указанные даты, при добавлении записи, обновлять эти значения
    def get_today_stats(self):
        today_stats = 0
        # Переменные должны именоваться с маленькой буквы.
        # Record - это название класса
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    # Аналогично - требуется проход по всем записям.
    # Если сделать словарь, достаточно будет
    # взять из него значения за 7 дней
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                # Можно записать в одну строку использя цепочки сравнения
                # A > x >= B
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


# Давайте оформим Docstrings для классов и функций
class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Необходимо придумать название переменной
        x = self.limit - self.get_today_stats()
        if x > 0:
            # f-строки лучше поместить в скобки, избавимся от "\"
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Лишний else
        else:
            # Здесь скобки не нужны
            return('Хватит есть!')


# Давайте оформим Docstrings для классов и функций
class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Лучше сделать мэпинг для валют
        # currencies = {
        #    'usd': {
        #        'rate': self.USD_RATE,
        #        'currency_type': 'USD'
        #    },
        # }
        # и считать
        # cash_remained /= self.currencies[currency]["rate"]
        # в случае добавления других валют не придётся раздувать if/else
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Ошибка. Оператор сравнения.
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # В f-строках нежелательны математические операции.
                # Округление нужно вынести
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Лишний elif
        elif cash_remained < 0:
            # Лучше использовать f-строки.
            # Контенкация будет происходить автоматически.
            # Избавимся от "\"
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Лишнее
    def get_week_stats(self):
        super().get_week_stats()
