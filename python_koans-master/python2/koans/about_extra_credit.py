#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from runner.koan import *
import random

import random

DEFAULT_DICE_NUMBER = 5

def roll(n):
    return [random.randint(1, 6) for _ in range(n)]

def score(dice):
    result = 0
    if len(dice) <= 5:
        dice_dict = dict((i, dice.count(i)) for i in dice)
        if dice_dict.get(1) >= 3:
            result += 1000
            dice_dict[1] -= 3
        for number in dice_dict:
            if dice_dict.get(number) >= 3:
                result += number * 100
                dice_dict[number] -= 3
        if 1 in dice_dict:
            result += dice_dict[1] * 100
            dice_dict[1] = 0
        if 5 in dice_dict:
            result += dice_dict[5] * 50
            dice_dict[5] = 0

    remaining_dice = len([die for die in dice_dict.keys() if dice_dict[die] != 0])
    remaining_dice = remaining_dice if remaining_dice else DEFAULT_DICE_NUMBER
    return result, remaining_dice


def print_turn(player, score):
    print "\n------------------------------------------\nStarting turn of {0} [Score: {1}]\n".format(player, score)


def ask_yes_no_question(prompt):
    user_input = raw_input(prompt)
    return user_input.upper() in ["Y", "YES"]

def ask_roll_again(player):
    return ask_yes_no_question("\n{0}, will you roll again? (y/n): ".format(player))


class Player(object):
    def __init__(self, name=""):
        self.name = name

    def __str__(self):
        if self.name:
            return "'{0}'".format(self.name)
        else:
            return "'Anonymous player'"

    def __repr__(self):
        return self.__str__()


class Game(object):
    def __init__(self, players, goal = 3000):
        if len(players) < 2:
            raise "This game is for 2 or more players."
        self.players_scores = dict((player, 0) for player in players)
        self.number_of_players = len(self.players_scores)
        self.players = [player for player in self.players_scores.keys()]
        self.goal = goal

    def play(self):
        first_player_to_reach_final_round = None
        turn = random.randint(0, len(self.players)-1)

        while turn != first_player_to_reach_final_round:
            player = self.players[turn]
            score = self.players_scores[player]
            print_turn(player, score)
            won_score = self._turn_score(player)
            self.players_scores[player] += won_score
            print "{0} has won {1} points (total {2}).".format(player, won_score, self.players_scores[player])
            if self.players_scores[player] >= self.goal:
                if first_player_to_reach_final_round is None:
                    first_player_to_reach_final_round = turn
                print "{0} has reached over {1} points. Next round will be the last round.".format(player, self.goal)
                print "\n\nLAST ROUND!!! Let's see who wins!"
            turn = (turn + 1) % self.number_of_players

        winner = self._winner()
        print "\n\nCongratulations, {0}! You have won the Greed Game!".format(winner)

    def _turn_score(self, player):
        total_score = 0
        keep_rolling = False

        dice = roll(DEFAULT_DICE_NUMBER)
        print "\n{0} rolls the dice and gets {1}.".format(player, dice)
        rolling_score, nb_dice = score(dice)

        if rolling_score > 0:
            # If dice is empty it means there were no non-scoring dice after the roll, so the player gets the choice to roll all 5 dice again
            numbers = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five" }
            print "That's a score of {0} points and {1} non-scoring {2} can be rolled again.".format(rolling_score, nb_dice, "die" if nb_dice == 1 else "dice")

            total_score += rolling_score

            keep_rolling = ask_roll_again(player) 

            while keep_rolling:
                dice = roll(nb_dice)
                print "\n{0} rolls the dice and gets {1}.".format(player, dice)
                rolling_score, nb_dice = score(dice)

                if rolling_score > 0:
                    numbers = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five" }
                    print "That's a score of {0} points and {1} non-scoring {2} can be rolled again.".format(rolling_score, nb_dice, "die" if nb_dice == 1 else "dice")

                    if total_score + rolling_score >= 300:
                        total_score += rolling_score
                        print "Since you reached more than 300 points this turn, your turn score is now {0}".format(total_score)
                    else:
                        total_score = rolling_score
                        print "Your turn score is less than 300 points, so now it's just the rolling score, {0} points.".format(total_score)

                    keep_rolling = ask_roll_again(player)
                else:
                    print "That's a zero-point roll, you lost your turn and all your won points in this turn."
                    keep_rolling = False
                    total_score = 0
        else:
            print "That's a zero-point roll, you cannot roll again in this turn."

        return total_score

    def _winner(self):
        return max(self.players_scores, key = self.players_scores.get)

    def _print_scores(self):
        print "\n------------------------------------------\nScores table\n"
        for player, score in self.players_scores:
            print "{0}: {1} points".format(player, score)

class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py
    def test_extra_credit_task(self):
		player1 = Player("Player 1")
		player2 = Player("Player 2")
		players = [ player1, player2 ]
		game = Game(players, 1500)
		game.play()

"""
class DiceSet(object):
    def __init__(self):
        self._values = None

    @property
    def values(self):
        return self._values

    def roll(self, n):
        self._values = []
        for i in range(0, n):
            val = random.randint(1, 6)
            self._values.append(val)
        return self._values

class Player(object):
	def __init__(self, name=""):
		self.name = name

	def __str__(self):
		if self.name:
			return "'{0}'".format(self.name)
		else:
			return "'Anonymous player'"

	def __repr__(self):
		return self.__str__()


class Game(object):
	def __init__(self, players, dice, goal = 3000):
		if len(players) < 2:
			raise "This game is for 2 or more players."
		self.dice = dice
		self.players_scores = dict((player, 0) for player in players)
		self.number_of_players = len(self.players_scores)
		self.players = [player for player in self.players_scores.keys()]
		self.turn = random.randint(0, len(self.players)-1)
		self.goal = goal

	def play(self):
		final_round = False
		first_player_to_reach_firnal_round = None

		while not final_round:
			self._print_turn()
			won_score = self._turn_score()
			self.players_scores[self.players[self.turn]] += won_score
			print "{0} has won {1} points (total {2}).".format(self.players[self.turn], won_score, self.players_scores[self.players[self.turn]])
			if self.players_scores[self.players[self.turn]] >= self.goal:
				final_round = True
				first_player_to_reach_firnal_round = self.turn
				print "{0} has reached over {1} points. Next round will be the last round.".format(self.players[self.turn], self.goal)
			self.turn = (self.turn + 1) % self.number_of_players

		# Last round. The player that reached the goal number of points doesn't play this round.
		print "\n\nLAST ROUND!!! Let's see who wins!"
		while self.turn != first_player_to_reach_firnal_round:
			self._print_turn()
			won_score = self._turn_score()
			self.players_scores[self.players[self.turn]] += won_score
			print "{0} has won {1} points (total {2}).".format(self.players[self.turn], won_score, self.players_scores[self.players[self.turn]])
			self.turn = (self.turn + 1) % self.number_of_players

		winner = self._winner()
		print "\n\nCongratulations, {0}! You have won the Greed Game!".format(winner)

	def score(self, dice):
	    result = 0
	    if len(dice) <= 5:
	        dice_dict = dict((i, dice.count(i)) for i in dice)
	        if dice_dict.get(1) >= 3:
	            result += 1000
	            dice_dict[1] -= 3
	        for number in dice_dict:
	            if dice_dict.get(number) >= 3:
	                result += number * 100
	                dice_dict[number] -= 3
	        if 1 in dice_dict:
	            result += dice_dict[1] * 100
	            dice_dict[1] = 0
	        if 5 in dice_dict:
	            result += dice_dict[5] * 50
	            dice_dict[5] = 0

	    non_scoring_dice = [die for die in dice_dict.keys() if dice_dict[die] != 0]
	    return result, non_scoring_dice

	def _turn_score(self):
		total_score = 0
		keep_rolling = False

		dice = self.dice.roll(5)
		print "\n{0} rolls the dice and gets {1}.".format(self.players[self.turn], dice)
		rolling_score, dice = self.score(dice)

		if rolling_score > 0:
			# If dice is empty it means there were no non-scoring dice after the roll, so the player gets the choice to roll all 5 dice again
			number_of_rollable_dice = 5 if not dice else len(dice)
			numbers = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five" }
			print "That's a score of {0} points and {1} non-scoring {2} can be rolled again.".format(rolling_score, number_of_rollable_dice, "die" if number_of_rollable_dice == 1 else "dice")

			total_score += rolling_score

			player_choice = raw_input("\n{0}, will you roll again? (y/n): ".format(self.players[self.turn]))
			if player_choice.upper() in ["Y", "YES"]:
				keep_rolling = True
		
			while keep_rolling:
				dice = self.dice.roll(number_of_rollable_dice)
				print "\n{0} rolls the dice and gets {1}.".format(self.players[self.turn], dice)
				rolling_score, dice = self.score(dice)

				if rolling_score > 0:
					number_of_rollable_dice = 5 if not dice else len(dice)
					numbers = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five" }
					print "That's a score of {0} points and {1} non-scoring {2} can be rolled again.".format(rolling_score, number_of_rollable_dice, "die" if number_of_rollable_dice == 1 else "dice")
					
					if total_score + rolling_score >= 300:
						total_score += rolling_score
						print "Since you reached more than 300 points this turn, your turn score is now {0}".format(total_score)
					else:
						total_score = rolling_score
						print "Your turn score is less than 300 points, so now it's just the rolling score, {0} points.".format(total_score)

					player_choice = raw_input("\n{0}, will you roll again? (y/n): ".format(self.players[self.turn]))
					if player_choice.upper() in ["Y", "YES"]:
						keep_rolling = True
					else:
						keep_rolling = False
				else:
					print "That's a zero-point roll, you lost your turn and all your won points in this turn."
					keep_rolling = False
					total_score = 0
		else:
			print "That's a zero-point roll, you cannot roll again in this turn."

		return total_score

	def _winner(self):
		return max(self.players_scores, key = self.players_scores.get)

	def _print_turn(self):
		print "\n------------------------------------------\nStarting turn of {0} [Score: {1}]\n".format(self.players[self.turn], self.players_scores[self.players[self.turn]])

	def _print_scores(self):
		print "\n------------------------------------------\nScores table\n"
		for player, score in self.players_scores:
			print "{0}: {1} points".format(player, score)


class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py
    def test_extra_credit_task(self):
		player1 = Player("Player 1")
		player2 = Player("Player 2")
		players = [ player1, player2 ]
		dice = DiceSet()
		game = Game(players, dice, 1500)
		game.play()
"""