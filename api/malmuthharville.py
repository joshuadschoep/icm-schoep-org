from itertools import permutations

# This fn has the goal of generating all subset of permutations P
# of set S by filtering out the limiting element, x, and then inserting it after
#
# It helps efficiency of malmuth harville's equation because we only need to generate
# payouts where x is in space i, so we only need to generate P(S{naught x}) permutations
# and insert x in those locations. 
# 
# Technically still n! time complexity but when you're dealing with that, O((n-1)!+i!) is
# still a huge improvement
# def limited_permutations():

def get_probability_of_iteration(ordered_proportional_stacks):
    rolling_probability = 0
    rolling_stacks_already_counted = 0
    for index, stack in enumerate(ordered_proportional_stacks):
        if index == 0:
            rolling_probability = stack
            rolling_stacks_already_counted = stack
        else:
            rolling_probability *= stack / (1 - rolling_stacks_already_counted)
            rolling_stacks_already_counted += stack
    return rolling_probability

def get_payouts_from_probability_table(payouts, probability_table):
    for player in probability_table:
        rolling_payout = 0
        for position, payout in enumerate(payouts):
            rolling_payout += player[position] * payout
        yield rolling_payout

def calculate(payouts, players):
    total_stacks = sum(players)
    players_with_stack_proportions = [{ 'index': i, 'stack': (s / total_stacks) } for i, s in enumerate(players)]
    final_odds = [[0 for _ in players] for _ in players]
    for iteration in permutations(players_with_stack_proportions):
        prob = get_probability_of_iteration((player['stack'] for player in iteration))
        for position, player in enumerate(iteration):
            final_odds[player['index']][position] += prob
    return get_payouts_from_probability_table(sorted(payouts, reverse=True), final_odds)

