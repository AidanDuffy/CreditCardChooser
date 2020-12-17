"""
Aidan Duffy
Class: CS 521 - Fall 2
Date: December 15, 2020
Final Project
Description: This is a user-defined class, as requested in the project
guidelines that is for the creation of wallet objects.
"""

import credit_card


class Wallet:
    __main_categories = ["dining", "grocery", "travel", "transit", "gas",
                         "online shopping", "else", "drugstores", "Amazon",
                         "PayPal"]

    def __init__(self):
        self.cards = list()
        self.best = self.construct_best_for_category()

    def construct_best_for_category(self):
        """
        This constructs a new empty best category wallet
        :return: the new best for category dictionary
        """
        best = dict()
        for category in Wallet.__main_categories:
            best[category] = None
        return best

    def add_card(self, card):
        """
        This adds a new card to the wallet
        :param card: the new card
        :return: none
        """
        self.cards.append(card)
        self.__check_if_new_best(card)

    def find_best_for_category(self, category):
        """
        Given a category, it'll return the best card
        :param category: the given category
        :return: the card that is best for that category
        """
        return self.best[category]

    def __check_if_new_best(self, card):
        """
        This takes in a new card and checks if it is now the best in any
        category
        :param card: is the new card
        :return: none
        """
        for category in self.best.keys():
            current_card = self.find_best_for_category(category)
            if current_card is None:
                self.best[category] = card
            else:
                current_card_value = current_card.check_categories(category)
                added_card_value = card.check_categories(category)
                if added_card_value > current_card_value:
                    self.best[category] = card

    def construct_template_wallet(self, database):
        """
        This takes an input file and parses through, creating a number of
        template cards
        :param database: is the opened credit card db file.
        :return: None
        """
        line = database.readline()
        line = line[:len(line) - 1]
        while line != "END":
            card_parts = list(line.split(":"))
            network = card_parts[0]
            issuer = card_parts[1]
            card_name = card_parts[2]
            cash_back_points = card_parts[3]
            if "," in cash_back_points:
                cpp = float(cash_back_points[2:])
                cash_back_points = cash_back_points[0]
            else:
                cpp = 1
            sub_info = card_parts[5]
            categories = card_parts[7]
            balance = 0
            age = 0
            card = credit_card.CreditCard("template", network, issuer,
                                          card_name,
                                          sub_info,
                                          categories, balance, age,
                                          cash_back_points, cpp)
            self.add_card(card)
            line = database.readline()
            line = line[:len(line) - 1]

    def construct_user_wallet(self, user_data):
        """
        This parses through the user's saved credit card info and populates
        their wallet
        :param user_data: is the open user cards text file
        :return:
        """
        line = user_data.readline()
        line = line[:len(line) - 1]
        while line is not "":
            card_parts = list(line.split(":"))
            holder = card_parts[0]
            network = card_parts[1]
            issuer = card_parts[2]
            card_name = card_parts[3]
            cash_back_points = card_parts[4]
            if "," in cash_back_points:
                cpp = float(cash_back_points[2:])
                cash_back_points = cash_back_points[0]
            else:
                cpp = 1.0
            sub_info = card_parts[6]
            sub_list = list(sub_info.split(","))
            if sub_list[0] == "False":
                sub_str = sub_info
            else:
                sub_str = sub_list[1] + "," + sub_list[2] + "," + sub_list[4]
            categories = card_parts[8]
            balance = card_parts[10]
            age = card_parts[9]
            card = credit_card.CreditCard(holder, network, issuer, card_name,
                                          sub_str,
                                          categories, balance, age,
                                          cash_back_points, cpp)
            if sub_list[0] == "True":
                sub = card.get_sign_up_bonus()
                sub.set_progress(int(sub_list[3]))
            self.add_card(card)
            line = user_data.readline()
            line = line[:len(line) - 1]

    def get_cards(self):
        """
        This returns all the cards in this wallet
        :return:
        """
        return self.cards

    def get_generic_category_names(self):
        """
        This allows the program to see which categories the wallet has already
        found best cards for.
        :return: the list of categories
        """
        return Wallet.__main_categories
