import requests


# import json


class BankRate:

    def __init__(self, balance=5000, term=12, rate=1.50, compounded=12):
        self.term = term
        self.rate = rate
        self.monthly_rate = None
        self.balance = balance
        self.compounded = compounded
        self.month_return = (self.balance * ((self.rate / 100) / 12))
        # dec = self.rate / 100
        # month_rate = dec / 12
        # self.monthly_rate = month_rate
        # self.month_return = self.monthly_rate * self.balance

    def __str__(self):
        return F"With a starting balance of ${self.balance:.2f}\tand an APY of {self.rate:.2f}% \n" \
               F"you will end the month with a gain of ${self.month_return:.2f}."


class Treasury:
    """amount ia a multiple of 100 for if you have 10 of 100 you have 1000 (the min on td-ameritrade)"""

    def __init__(self, data_json, amount=10):
        self.term = data_json['term']
        self.term_day = data_json['securityTermDayMonth']
        self.amount = amount
        self.total = 0
        self.price_per100 = float(data_json['highPrice'])
        self.returnamount = (100 * amount) - (self.price_per100 * amount)
        self.line_one = "term -> " + self.term
        self.line_two = F"Annualized return -> {self.total:.2f}%"
        self.line_three = F"return amount -> ${self.returnamount:.2f}"

    def totals(self):
        yieldper = ((100 - self.price_per100) / self.price_per100) * 100
        term = int(self.term_day.split("-")[0])
        anreturn = yieldper * (365 / term)
        self.total = anreturn

    def __str__(self):
        return "\tterm -> " + self.term + f"\nAnnualized return -> {self.total:.2f}%\n return amount -> ${self.returnamount:.2f}"


def t_bill(amount: int):
    listof = []
    # base = "http://www.treasurydirect.gov/TA_WS"
    # formats = "format=json"
    # page = "pagesize=15"
    days = "5"
    # types = "types=Bill"
    #
    # # data = requests.get("{}+/securities/auctioned?{}&{}".format(base, formats, page))
    # # data.json()
    data = requests.get(F"http://www.treasurydirect.gov/TA_WS/securities/auctioned?format=json&type=Bill&days={days}")
    # print(data.json())
    file = open("data.json", "w")
    file.write(str(data.json()))
    data = data.json()

    for i in range(len(data)):
        cusip = data[i]['cusip']
        # if data[i]['securityTerm'] == "4-Week":
        data2 = requests.get(
            "http://www.treasurydirect.gov/TA_WS/securities/search?cusip=" + cusip + "&format=json")
        data2 = data2.json()

        for indx in range(len(data2)):
            # data2[i]['securityTerm'] = data2[i]['lowDiscountRate']
            # a = t_rate(data2[i], data2[i]['securityTerm'], data2[i]['lowDiscountRate'])
            listof.append(Treasury(data2[indx], amount=amount))
            for inx in listof:
                inx.totals()
    return listof


def t_bill_print(list_of_data, printlist_one="|", print_l_2="|", p_l_3="|"):
    if len(list_of_data) == 0:
        return "####there may be en error in the Treasury Direct API used to acquire this data####"
    p1 = printlist_one
    p2 = print_l_2
    p3 = p_l_3
    for i in range(len(list_of_data)):
        if list_of_data[i].term != "":
            p1 += F"{list_of_data[i].line_one:^25}\t|\t"
            p2 += F"{list_of_data[i].line_two:^25}\t|\t"
            p3 += F"{list_of_data[i].line_three:^25}\t|\t"
    p1 += F"\n{p2}\n{p3}"
    return p1


#
# def recommend(bank_obj:object, t_bill_obj_list:list):
#     dictionary = {}
#     for each in range(len(t_bill_obj_list)):
#         dictionary[F'{t_bill_obj_list[each].term}'] = F'{t_bill_obj_list[each].returnamount}'
#
#
#
#     new_val = dictionary.values()
#     maximum_val = max(new_val)
#     print("Maximum value from dict:",maximum_val)


def disclaimer():
    """Disclaimer was taken from https://www.stockopedia.com/learn/account-billing/disclaimer-463143/"""
    return """\t\tDisclaimer
This script is meant only for informational purposes 
Before using this please make sure that you note the following important information:\n\t\tDo Your Own Research
Our content is intended to be used and must be used for information and education purposes only. It is very important
to do your own analysis before making any investment based on your own personal circumstances. You should take
independent financial advice from a professional in connection with, or independently research and verify, 
any information that you find on and wish to rely upon, whether for the purpose of making an investment decision or otherwise."""


def main():
    print(disclaimer())
    amount_int = 0
    amount_valid = True
    while amount_valid:
        amount = input("\nHow much money are you looking to invest? (Must be a multiple of 1000)\t>>\t")
        amount_int = int(amount)
        if amount_int % 1000 == 0:
            amount_valid = False
    apy = float(input("What is the APY for your bank account, CD or similar account?\t>>\t"))

    t_bill_data = t_bill(amount=amount_int / 100)
    print(F"\nBased on Historical Data from the past 5 days Treasury auctions.")
    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-" * len(t_bill_data))
    print(t_bill_print(t_bill_data))
    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-" * len(t_bill_data))
    bank = BankRate(amount_int, rate=apy)

    print(F"{bank}")


main()
