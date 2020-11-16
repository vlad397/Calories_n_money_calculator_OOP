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
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        todays_spend = 0
        for records in self.records:
            if records.date == dt.date.today():
                todays_spend += records.amount
        return todays_spend

    def get_week_stats(self):
        week = 0
        week_back = dt.date.today() - dt.timedelta(7)
        for record in self.records:
            if dt.date.today() >= record.date > week_back:
                week += record.amount
        return week

    def __str__(self):
        return('\n'.join(self.records))


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    currencies = {
        "usd": ["USD", USD_RATE],
        "eur": ["Euro", EURO_RATE],
        "rub": ["руб", 1]
    }

    def get_today_cash_remained(self, currency):
        currency_title = self.currencies[currency][0]
        remained = ((self.limit - self.get_today_stats()) /
                    self.currencies[currency][1])
        cash_remained = round(remained, 2)
        if cash_remained == 0:
            return "Денег нет, держись"
        elif cash_remained > 0:
            return f"На сегодня осталось {cash_remained} {currency_title}"
        else:
            return f"Денег нет, держись: твой долг - "\
                    f"{abs(cash_remained)} {currency_title}"


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но "\
                    f"с общей калорийностью не более {calories_remained} кКал"
        else:
            return f"Хватит есть!"
