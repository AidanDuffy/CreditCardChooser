"""
Aidan Duffy
Class: CS 521 - Fall 2
Date: December 15, 2020
Final Project
Description: This is a test file that is meant to check functions are working
properly
"""

import credit_card

from main import decider


def test_setup_and_changes():
    holder = "template"
    network = "Mastercard"
    issuer = "Citi"
    name = "Double Cash"
    sub_info = "0,0,0"
    categories = "else-2"
    balance = 0
    age = 0
    points_cash_back = "C"
    card = credit_card.CreditCard(holder, network, issuer, name, sub_info,
                                  categories, balance, age, points_cash_back)
    card.purchase(1000)
    card.pay_off_card(700)
    assert (card.check_balance() == 300)
    assert (card.get_cents_per_point() == 1)
    assert (card.check_points_or_cash() == "C")
    test = "template:Mastercard:Citi:Double Cash:C:SUB:False:Categories:" \
           "else-2:0:300"
    repstr = card.__repr__()
    assert (test == repstr)
    return True


def test_sign_up_bonus():
    holder = "template"
    network = "AMEX"
    issuer = "AMEX"
    name = "Gold"
    sub_info = "60000,4000,6"
    categories = "dining-4,grocery-4,flight(AMEX)-3,else-1"
    balance = 0
    age = 0
    points_cash_back = "P"
    cpp = 2
    card = credit_card.CreditCard(holder, network, issuer, name, sub_info,
                                  categories, balance, age, points_cash_back,
                                  cpp)
    sub = card.get_sign_up_bonus()
    assert (sub.check_active())
    assert (sub.get_progress() == 0)
    card.purchase(3000)
    assert (sub.get_progress() == 3000)
    card.purchase(1000)
    assert (sub.check_active() is False)
    card.purchase(5000)
    assert (sub.get_progress() == 4000)
    return True


def test_select_category():
    holder = "template"
    network = "Mastercard"
    issuer = "Citi"
    name = "Double Cash"
    sub_info = "0,0,0"
    categories = "else-2"
    balance = 0
    age = 0
    points_cash_back = "C"
    card1 = credit_card.CreditCard(holder, network, issuer, name, sub_info,
                                   categories, balance, age, points_cash_back)
    holder = "template"
    network = "AMEX"
    issuer = "AMEX"
    name = "Gold"
    sub_info = "60000,4000,6"
    categories = "dining-4,grocery-4,flight(AMEX)-3,else-1"
    balance = 0
    age = 0
    points_cash_back = "P"
    cpp = 2
    card2 = credit_card.CreditCard(holder, network, issuer, name, sub_info,
                                   categories, balance, age, points_cash_back,
                                   cpp)
    assert (card1.check_categories("dining") == 2)
    assert (card2.check_categories("dining") == 8)
    assert (card2.check_categories("gas") == 2)
    return True


def test_decider():
    holder = "template"
    network = "AMEX"
    issuer = "AMEX"
    name = "Gold"
    sub_info = "60000,4000,6"
    categories = "dining-4,grocery-4,flight(AMEX)-3,else-1"
    balance = 6000
    age = 10
    points_cash_back = "P"
    cpp = 2
    card = credit_card.CreditCard(holder, network, issuer, name, sub_info,
                                  categories, balance, age, points_cash_back,
                                  cpp)
    holder = "template"
    network = "Mastercard"
    issuer = "Citi"
    name = "Double Cash"
    sub_info = "0,0,0"
    categories = "else-2"
    balance = 0
    age = 0
    points_cash_back = "C"
    card1 = credit_card.CreditCard(holder, network, issuer, name, sub_info,
                                   categories, balance, age, points_cash_back)
    assert (card.get_sign_up_bonus().check_active() is False)
    wallet = list()
    wallet.append(card)
    wallet.append(card1)
    print("Type 1, then 1 or 2, then N for the first test.")
    result = decider(wallet)
    if result[0] != "tie":
        assert result[0] == "AMEX"
    print("Type 4, then N for the second test.")
    result = decider(wallet)
    assert (result[0] == "tie")
    holder = "template"
    network = "Mastercard"
    issuer = "Chase"
    name = "Freedom Flex"
    sub_info = "500,200,3"
    categories = "quarterly-5,travel(Chase)-5,dining-3,drugstores-3,else-1"
    balance = 0
    age = 0
    points_cash_back = "P"
    card2 = credit_card.CreditCard(holder, network, issuer, name, sub_info,
                                   categories, balance, age, points_cash_back,
                                   2)
    assert card2.get_sign_up_bonus().check_active()
    wallet.append(card2)
    print("Won't type anything, will always return card2 as it has the SUB")
    result = decider(wallet)
    assert result[2] == 0
    assert result[1] == "Freedom Flex"
    return True


def main():
    check = test_setup_and_changes()
    if check:
        print("Initial setup and basic change test passed!")
    else:
        print("Initial setup and basic change test failed...")
    check = test_sign_up_bonus()
    if check:
        print("Sign-up bonus test passed!")
    else:
        print("Sign-up bonus test failed...")
    check = test_select_category()
    if check:
        print("Category Selection test passed!")
    else:
        print("Category Selection test failed...")
    check = test_decider()
    if check:
        print("Decider test passed!")
    else:
        print("Decider test failed...")


if __name__ == "__main__":
    main()
