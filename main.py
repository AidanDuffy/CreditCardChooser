"""
Aidan Duffy
Class: CS 521 - Fall 2
Date: December 15, 2020
Final Project
Description: This is the main project file for the credit card choosing program
Future Goals: 1. Add a Wallet Class for additional accessor/mutator methods.
2. Add a function that prints out all a user's cards
3. Incorporate naming schemes to separate user info.
4. Implement an actual user interface for easier usage
5. Implement a way to scrape blogs to find the most up to date CPP data.
6. Implement a way to pull SUB data as well as quarterly category data for the
affected cards.
"""

import credit_card
from wallet import Wallet


def save_user_cards(wallet, user_data):
    """
    This saves all of the user card information in a text file for next time.
    :param wallet: is the list of this user's cards
    :param user_data: is the file which all this data will be saved to.
    :return: none
    """
    for card in wallet.get_cards():
        user_data.write(card.__repr__() + "\n")


# noinspection PyBroadException
def add_card(wallet, template_wallet):
    """
    This is adds a new card to the user wallet from the template_wallet, but
    it is populated with any user provided information, such as age of account
    and account balance.
    :param wallet: is the list of credit cards for this given user
    :param template_wallet: is list of all credit cards this program can handle
    :return: True or False depending on the success of the function.
    """
    name = input("What is the name on the card? ")
    issuer = input("Which bank is the issuer? ")
    selected = False
    new_card = None
    yes_no = ""
    for card in template_wallet.get_cards():
        if card.get_issuer() != issuer:
            continue
        while yes_no != "Y" or yes_no != "N":
            yes_no = input("Is it the " + card.get_card_name()
                           + "(Input Y or N)? ")
            if yes_no == "Y":
                selected = True
                new_card = card
                break
            elif yes_no == "N":
                break
            else:
                print("Error! Please enter in Y or N!")
        if selected:
            break
    if selected is False:
        return
    result = None
    while yes_no != "Y" or yes_no != "N":
        yes_no = input("Is the card new (Input Y or N)? ")
        sub = new_card.get_sign_up_bonus()
        network = new_card.get_network()
        issuer = new_card.get_issuer()
        card_name = new_card.get_card_name()
        cats = new_card.print_categories()
        p_or_c = new_card.check_points_or_cash()
        cpp = new_card.get_cents_per_point()
        sub_info = str(sub.get_reward()) + "," + str(sub.get_minimum_spend()) \
            + "," + str(sub.get_months())
        if yes_no == "Y":
            balance = 0
            age = 0
            result = credit_card.CreditCard(name, network, issuer, card_name,
                                            sub_info, cats, balance, age,
                                            p_or_c, cpp)
            break
        elif yes_no == "N":
            while True:
                try:
                    balance = float(input("Please enter the balance in USD: "))
                    age = int(input("Please enter the age in months of the "
                                    "card: "))
                    break
                except ValueError:
                    print("Please enter valid numbers!")

            result = credit_card.CreditCard(name, network, issuer, card_name,
                                            sub_info, cats, balance, age,
                                            p_or_c, cpp)
            break
        else:
            print("Error! Please enter in Y or N!")

    if selected:
        wallet.add_card(result)
    return selected


def decider(wallet):
    """
    This checks the best card to use for a given purchase.
    :param wallet: is the list of credit cards for this given user
    :return: True or False depending on the success of the function.
             if True, it will return a list:the card issuer, name,
             the spending category and the value of the rewards.
    Future Goals: 1. Update to include a map to consolidate the menu function,
    ex: {"Food":"dining,groceries"}?
    2. find out how to not have to hardcode quarterly categories for card like
     the Chase Freedom Flex/Discover It.
    3. Add larger functionality generally for deciding on subcategories.
    4. Add Wallet object, which will have flags for the best travel card or
    dining card.
    """
    found = False
    if len(wallet.get_cards()) == 0:
        return found
    elif len(wallet.get_cards()) == 1:
        card = wallet.get_cards()[0]
        found = list()
        found.append(card.get_issuer())
        found.append(card.get_card_name())
        found.append(-1)
        return found
    """
    First, we need to check for any valid SUB. If so, if there's one,
    then that will be selected, otherwise, narrow the options to just 
    those with active sign_up_bonus and do the usual process.
    """
    sub_cards = list()
    subs = False
    for card in wallet.get_cards():
        sub = card.get_sign_up_bonus()
        if sub.check_active():
            sub_cards.append(card)
            subs = True
    if len(sub_cards) == 1:
        found = list()
        card = sub_cards[0]
        found.append(card.get_issuer())
        found.append(card.get_card_name())
        found.append(0)
        return found
    elif len(sub_cards) > 1:
        subs = True
    category = decider_menu()
    # PayPal is currently a quarterly category on several cards
    paypal = ""
    while paypal != "N" and paypal != "Y":
        paypal = input(
            "Will you be purchasing through PayPal? (Y/N):  ")
        if paypal == "Y":
            category = category + "(PayPal)"
            break
        elif paypal == "N":
            break
        else:
            print("Invalid input")
    main_categories = wallet.get_generic_category_names()
    if category in main_categories:
        best_card = wallet.find_best_for_category(category)
        found = list()
        found.append(best_card.get_issuer())
        found.append(best_card.get_card_name())
        found.append(category)
        found.append(best_card.check_categories(category))
        return found
    best = list()
    best.append(0)
    best.append(0)
    tie = list()
    """
    Here, depending on whether of not there are active sign-up bonuses, the
    function will go through each card in the wallet to find the best value.
    A future goal is implementing the Wallet class, in which I will have a 
    dictionary attribute which will contain the best card mapped to its
    category i.e. {"dining":AMEX Gold}, and whenever new cards are added, it
    will check then so as to prevent algorithmic backups which occur now.
    """
    for card in sub_cards:
        sub = card.get_sign_up_bonus()
        value = card.check_categories(category)
        if "(" in category:
            if "PayPal" in category:
                category = category[:len(category) - 8]
                if (card.check_categories("quarterly") !=
                        card.check_categories("else")):
                    value = card.check_categories("quarterly")
                    value += card.check_categories(category)
            if "IHG" in category:
                if value != 25 * .6:
                    value = card.check_categories("travel")
            if "Whole Foods" in category:
                if value == card.check_categories("else"):
                    value = card.check_categories("grocery")
            if "Amazon" in category:
                if value == card.check_categories("else"):
                    value = card.check_categories("online shopping")
        if subs:
            value += sub.get_return_on_spend() * 100
        if value > best[0]:
            best[0] = value
            best[1] = card
            tie = list()
        elif value == best[0]:
            tie.append(card)
            tie.append(best[1])
    if subs:
        print("Note: This recommendation is made because"
              " of a sign-up bonus, not only multipliers!")
    found = list()
    if len(tie) == 0:
        card = best[1]
        found.append(card.get_issuer())
        found.append(card.get_card_name())
        found.append(category)
        found.append(best[0])
    else:
        found.append("tie")
        found.append(tie)
        found.append(category)
        found.append(best[0])
    return found


def decider_menu():
    """
    Here, we will continue to run through this menu of categories and sub-
    categories until a user has selected a valid one, providing the function
    with all the necessary information.
    :return: the category string
    """
    menu_value = -1
    while menu_value < 0 or menu_value > 6:
        print("Spending Categories:\n\t1. Food\n\t2. Travel\n\t3. Transit"
              "\n\t4. Gas\n\t5. Online Shopping\n\t6. Other\n")
        menu_value = input("Please enter one of the above values or 0 "
                           "to cancel: ")
        try:
            menu_value = int(menu_value)
        except ValueError:
            print("Error: Not an integer! Please enter a valid input!")
            continue
        if menu_value == 0:
            break
        elif menu_value < 0 or menu_value > 6:
            print("Error: Not a valid integer! Please enter a valid number!")
            continue
        elif menu_value == 1:
            print("You have selected Food! Please select a subcategory:\n\t"
                  "1. Dining\n\t2. Groceries")
            subcategory = input("Please enter an above values, anything else "
                                "to leave this category: ")
            try:
                subcategory = int(subcategory)
                if subcategory == 1:
                    return "dining"
                elif subcategory == 2:
                    amazon = ""
                    while amazon != "N" and amazon != "Y":
                        amazon = input(
                            "Are you shopping at Whole Foods? (Y/N):  ")
                        if amazon == "N":
                            return "grocery"
                        elif amazon == "Y":
                            return "grocery(Whole Foods)"
                        else:
                            print("Invalid input")
                else:
                    print("Exiting the food category...")
                    continue
            except ValueError:
                print("Exiting the food category...")
                continue
        elif menu_value == 2:
            print("You have selected Travel! Please select a subcategory:\n"
                  "\t1. Flights\n\t2. Hotels\n\t3. Chase\n\t4. AMEX")
            subcategory = input("Please enter an above value, anything else "
                                "to leave this category: ")
            try:
                subcategory = int(subcategory)
                if subcategory == 1:
                    return "travel"
                elif subcategory == 2:
                    print("You have selected Hotel! Are you booking:\n\t1."
                          "With an IHG partner\n\t2. Elsewhere")
                    subcategory = int(input("Option: "))
                    if subcategory == 1:
                        return "hotel(IHG)"
                    else:
                        return "travel"
                elif subcategory == 3:
                    return "travel(Chase)"
                elif subcategory == 4:
                    return "travel(AMEX)"
                else:
                    print("Exiting the Travel category...")
                    continue
            except ValueError:
                print("Error! Exiting the Travel category...")
                continue
        elif menu_value == 3:
            return "transit"
        elif menu_value == 4:
            return "gas"
        elif menu_value == 5:
            print("You have selected Online Shopping! Please select a "
                  "subcategory:\n\t1. Amazon\n\t2. Walmart\n\t3. Elsewhere")
            subcategory = input(
                "Please enter an above value, anything else to "
                "leave this category: ")
            try:
                subcategory = int(subcategory)
                if subcategory == 1:
                    return "online shopping(Amazon)"
                elif subcategory == 2:
                    return "online shopping(Walmart)"
                elif subcategory == 3:
                    return "online shopping"
                else:
                    print("Exiting the Online Shopping category...")
                    continue
            except ValueError:
                print("Error! Exiting the Online Shopping category...")
                continue
        elif menu_value == 6:
            print("You have selected Other! Please select a subcategory:\n\t1."
                  " Streaming\n\t2. Utilities\n\t3. Drugstores\n\t4. Other")
            subcategory = input("Please enter an above value, anything else to"
                                " leave this category: ")
            try:
                subcategory = int(subcategory)
                if subcategory == 1:
                    return "streaming"
                elif subcategory == 2:
                    return "utilities"
                elif subcategory == 3:
                    return "drugstores"
                elif subcategory == 4:
                    return "else"
                else:
                    print("Exiting the Other category...")
                    continue
            except ValueError:
                print("Error! Exiting the Other category...")
                continue


def check_balance(wallet):
    """
    This checks the balance on a given user card.
    :param wallet: is the list of credit cards for this given user
    :return: True or False depending on the success of the function.
             if True, it will return a list:the card issuer, name, and balance.
    """
    which_card = input("Which card are you checking the balance for? (Enter "
                       "in Issuer,Card Name) ")
    card_parts = list(which_card.split(","))
    found = False
    if len(card_parts) == 2:
        for card in wallet:
            if card.get_issuer() == card_parts[0]:
                if card.get_card_name() == card_parts[1]:
                    found = card_parts
                    found.append(card.check_balance())
                    break
    return found


def make_payment(wallet):
    """
    This makes a payment to a given user card.
    :param wallet: is the list of credit cards for this given user
    :return: True or False depending on the success of the function.
             if True, it will return a list:the card issuer and name.
    """
    which_card = input("Which card are you making a payment for? (Enter "
                       "in Issuer,Card Name) ")
    amount = input("How much are you paying off? (Use integers): ")
    found = False
    try:
        amount = int(amount)
    except ValueError:
        return found
    card_parts = list(which_card.split(","))
    if len(card_parts) == 2:
        for card in wallet:
            if card.get_issuer() == card_parts[0]:
                if card.get_card_name() == card_parts[1]:
                    card.pay_off_card(amount)
                    found = card_parts
                    found.append(str(amount))
                    break
    return found


def check_sign_up_bonus(wallet):
    """
    This checks the sign up bonus information of a given user card.
    :param wallet: is the list of credit cards for this given user
    :return: True or False depending on the success of the function.
             if True, it will return a list: sign-up bonus object and
             the card issuer and name.
    """
    which_card = input("Which card are you checking the SUB for? "
                       "(Enter in Issuer,Card Name) ")
    card_parts = list(which_card.split(","))
    found = False
    if len(card_parts) == 2:
        for card in wallet:
            if card.get_issuer() == card_parts[0]:
                if card.get_card_name() == card_parts[1]:
                    found = list()
                    found.append(card.get_sign_up_bonus())
                    found.append(card.get_issuer())
                    found.append(card.get_card_name())
                    break
    return found


def check_cents_per_point(wallet):
    """
    This checks the cents per point value of a given user card.
    :param wallet: is the list of credit cards for this given user
    :return: True or False depending on the success of the function.
             if True, it will return a list: the issuer, name, and CPP
    """
    which_card = input("Which card are you checking the CPP for? (Enter "
                       "in Issuer,Card Name) ")
    card_parts = list(which_card.split(","))
    found = False
    if len(card_parts) == 2:
        for card in wallet:
            if card.get_issuer() == card_parts[0]:
                if card.get_card_name() == card_parts[1]:
                    found = card_parts
                    found.append(card.get_cents_per_point())
                    break
    return found


def main_menu(template_wallet, wallet):
    """
    This is the main menus of the program.
    :param template_wallet: is the default wallet
    :param wallet: is the user's wallet
    :return: none
    """
    menu_value = -1
    while menu_value != 0:
        print(
            "Main Menu:\n\t0. Exit\n\t1. Add New Card\n\t2. Which Card Should"
            " I Use for this Purchase?\n\t3. Check Balance"
            "\n\t4. Make a Payment\n\t5. Check Sign-Up Bonus Information"
            "\n\t6. Check the Cents Per Point\n")
        menu_value = (input("Please enter one of the above values: "))
        try:
            menu_value = int(menu_value)
        except ValueError:
            print("Error: Not an integer! Please enter a valid input!")
            continue
        print("\n\n")
        if menu_value == 0:
            break
        elif menu_value == 1:
            function_success = add_card(wallet, template_wallet)
            if function_success:
                print("Successfully added your card to your digital wallet!")
            else:
                print("It appears we do not currently support the card or "
                      "issuer you are looking for! Check back again later!")
            continue
        elif len(wallet.get_cards()) == 0:
            print("Try adding a card first!\n")
            continue
        elif menu_value == 2:
            function_success = decider(wallet)
            if function_success:
                category = function_success[2]
                card_name = function_success[1]
                card_issuer = function_success[0]
                if category == -1:
                    print("Success! You only have one card: the", card_issuer,
                          card_name, "is what you use for all purchases!")
                elif category == 0:
                    print("Success! You have one card with an active SUB: use",
                          "the", card_issuer, card_name, "for all purchases!")
                else:
                    reward = function_success[3]
                    if function_success[0] == "tie":
                        print("It's a tie for purchases in the", category,
                              "category. You should see a", reward, "percent",
                              "return with the following cards:")
                        for card in function_success[1]:
                            print("\t", card.get_issuer(),
                                  card.get_card_name())
                        continue
                    print("Success! Use the", card_issuer, card_name, "for",
                          "purchases in the", category, "category. You "
                                                        "should see a", reward,
                          "percent return!")
        elif menu_value == 3:
            function_success = check_balance(wallet)
            if function_success:
                balance = function_success[2]
                card_name = function_success[1]
                card_issuer = function_success[0]
                print("Success! The balance on your", card_issuer,
                      card_name, "is", balance, ".")
        elif menu_value == 4:
            function_success = make_payment(wallet)
            if function_success:
                card_name = function_success[1]
                card_issuer = function_success[0]
                payment = function_success[2]
                print("Success! You have made a payment on your",
                      card_issuer, card_name, "of", payment, "!")
        elif menu_value == 5:
            function_success = check_sign_up_bonus(wallet)
            if function_success:
                sub = function_success[0]
                card_name = function_success[2]
                card_issuer = function_success[1]
                if sub.check_active() is False:
                    print("Success! Unfortunately, your ", card_issuer, " ",
                          card_name, "'s sign-up bonus is no longer active",
                          sep="")
                    continue
                print("Success! Here is the sign-up bonus information for"
                      " your", card_issuer, card_name, ":\n\tSUB",
                      "Reward:", str(sub.get_reward()),
                      "\n\tMinimum Spend:",
                      str(sub.get_minimum_spend()), "\n\tProgress: ",
                      str(sub.get_progress()), "\n\tMonths: ",
                      str(sub.get_months()), "\n\n")
        elif menu_value == 6:
            function_success = check_cents_per_point(wallet)
            if function_success:
                print("Success! The", function_success[0], function_success[1],
                      "point value in cents per point (CPP) is",
                      function_success[2])
            if function_success is False:
                print(
                    "Failure... You either do not have this card or gave a bad"
                    "input! Try again!")
        else:
            print("Error: Not a valid integer! Please enter a valid number!")
            continue
    print("Exiting...")


def main(ccdb, user_data):
    """
    This is the main method of the program
    :param ccdb: is the name of the card database text file
    :param user_data: is the name of the user card text file
    :return:
    Future Goals: Have the menu run through a separate function in order to
    consolidate/modularize.
    """
    database = open(ccdb, "r+")
    user = open(user_data, "r+")

    template_wallet = Wallet()
    template_wallet.construct_template_wallet(database)
    wallet = Wallet()
    if len(user.read()) > 0:
        user = open(user_data, "r+")
        wallet.construct_user_wallet(user)
    main_menu(template_wallet, wallet)
    user = open(user_data, "r+")
    save_user_cards(wallet, user)
    user.close()
    database.close()


if __name__ == "__main__":
    main("Credit Card Database.txt", "user cards.txt")
