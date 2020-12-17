"""
Aidan Duffy
Class: CS 521 - Fall 2
Date: December 15, 2020
Final Project
Description: This is a user-defined class, as requested in the project
guidelines that is for the creation of a signup bonus (or SUB) object.
"""


class SignUpBonus:

    def __init__(self, info):
        """
        This creates a new sign-up bonus object given a string of info.
        :param info: is the SUB info provided by the database file or user.
        """
        if info == "False":
            self.active = False
            self.minimum = 0
            self.months = 0
            self.reward = 0
            self.progress = 0
            return
        sub = list(info.split(","))
        self.reward = int(sub[0])
        self.minimum = int(sub[1])
        self.months = int(sub[2])
        self.progress = 0
        """
        This is the return on spending for the "else" category, must be set
        by with CPP. It defaults to 1.0 for CPP for cash back cards, needs
        to be updated for points.
        """
        if self.get_minimum_spend() == 0:
            self.deactivate_sign_up_bonus()
        else:
            self.ROS = (self.get_reward() * 1.0) / self.get_minimum_spend()
        if self.minimum == 0:
            self.active = False
        else:
            self.active = True

    def set_return_on_spend(self, cpp):
        """
        This sets/updates the return on spend for this card's sign-up bonus.
        :param cpp: is the cents per point on this card
        :return: none
        """
        self.ROS = (self.get_reward() * .01 * cpp) / self.get_minimum_spend()

    def get_return_on_spend(self):
        """
        This gives the user the return on spend for the SUB.
        :return: the float value for the return on spend for this SUB
        """
        return self.ROS

    def set_progress(self, progress):
        """
        This sets/updates the progress of a user's ability to get a sign-up
        bonus.
        :param progress: is the additional purchases in USD.
        :return: none
        """
        self.progress += progress
        if self.progress >= self.minimum:
            self.deactivate_sign_up_bonus()

    def deactivate_sign_up_bonus(self):
        """
        This deactivates the sign-up bonus if the user hit the spend
        requirement or ran out of time.
        :return:
        """
        self.active = False

    def check_active(self):
        """
        This just checks if the sign_up_bonus is active or not.
        :return: True or False, depending on the the activity of the SUB.
        """
        return self.active

    def get_months(self):
        """
        This gives the user the number of months left on the sign_up_bonus.
        :return: the int value for the number of months left on this SUB.
        """
        return self.months

    def get_reward(self):
        """
        :return: the reward for this sign up bonus.
        """
        return self.reward

    def get_progress(self):
        """
        :return: the progress towards the minimum spend for this SUB
        """
        return self.progress

    def get_minimum_spend(self):
        """
        :return: the minimum spending requirement for this sSUB.
        """
        return self.minimum
