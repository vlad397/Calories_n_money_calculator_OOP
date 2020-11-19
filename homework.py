import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    TODAY = dt.date.today()

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        return sum(records.amount for records in self.records
                   if records.date == self.TODAY)

    def get_week_stats(self):
        week = 0
        week_back = self.TODAY - dt.timedelta(7)
        for record in self.records:
            if self.TODAY >= record.date > week_back:
                week += record.amount
        return week

    def __str__(self):
        return '\n'.join(self.records)

    def get_today_remained(self):
        today_remained = self.limit - self.get_today_stats()
        return today_remained


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    currencies = {
        "usd": ["USD", USD_RATE],
        "eur": ["Euro", EURO_RATE],
        "rub": ["руб", 1]
    }

    def get_today_cash_remained(self, currency):
        if self.get_today_remained() == 0:
            return "Денег нет, держись"
        if currency not in self.currencies:
            return "Валюта не поддерживается"
        currency_name, currency_rate = self.currencies[currency]
        remained = (self.get_today_remained() / currency_rate)
        cash_remained = round(remained, 2)
        cash_remained_abs = abs(cash_remained)
        if cash_remained > 0:
            return f"На сегодня осталось {cash_remained} {currency_name}"
        return (f"Денег нет, держись: твой долг - "
                f"{cash_remained_abs} {currency_name}")


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_today_remained() > 0:
            return (f"Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {self.get_today_remained()} кКал")
        return "Хватит есть!"
