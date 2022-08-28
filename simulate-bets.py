import random

import matplotlib.pyplot as plt
import pandas

BET_COEF = [(1, 1.0625), (2, 1.125), (4, 1.25), (8, 1.5), (16, 2.0), (32, 3.0)]
ESTIMATE_COEF = [(1, 3.0), (2, 2.0), (4, 1.0), (8, -0.0), (16, -0.5), (32, -1.0)]


def coefficient(diff, coef):
    for max_diff, c in coef:
        if max_diff >= diff:
            return c
    return 0


def eval_bet(real_times, estimates, team, bet, bet_type):
    diff = real_times[team] - estimates[team]
    if bet_type == -1 and diff < 0:
        return 0
    if bet_type == 1 and diff > 0:
        return 0
    diff = abs(diff)
    # worse
    if bet_type == -1:
        return bet * (coefficient(diff, BET_COEF))
    # better
    if bet_type == 1:
        return bet * (coefficient(diff, BET_COEF))
    print("invalid bet")
    return 0


def bet_type_to_str(bet_type):
    return "be better" if bet_type == -1 else "be worse"


def random_bet(current_team, teams_cnt, average_bet, bet_sigma):
    team = random.randint(0, teams_cnt - 1)
    if team == current_team:
        return
    bet = round(random.gauss(average_bet, bet_sigma))
    if bet <= 0:
        return
    bet_type = random.choice([-1, 1])
    return team, bet, bet_type


def believer_bet(current_team, teams_cnt, average_bet, bet_sigma, estimates, average_time):
    # teams who estimate worse than average are bet to be better
    team = random.randint(0, teams_cnt - 1)
    if team == current_team:
        return
    bet = round(random.gauss(average_bet, bet_sigma))
    if estimates[team] < average_time:
        return
    if bet <= 0:
        return
    return team, bet, 1


def nonbeliever_bet(current_team, teams_cnt, average_bet, bet_sigma, estimates, average_time):
    # teams who estimate better than average are bet to be worse
    team = random.randint(0, teams_cnt - 1)
    if team == current_team:
        return
    bet = round(random.gauss(average_bet, bet_sigma))
    if estimates[team] > average_time:
        return
    if bet <= 0:
        return
    return team, bet, -1


def informed_bet(current_team, teams_cnt, average_bet, bet_sigma, real_times, estimates):
    team = random.randint(0, teams_cnt - 1)
    if team == current_team:
        return
    bet = round(random.gauss(average_bet, bet_sigma))
    if bet <= 0:
        return
    if real_times[team] < estimates[team]:
        return team, bet, 1
    if real_times[team] > estimates[team]:
        return team, bet, -1
    return


def main():
    init_shitcoins = 10000
    teams_cnt = 8
    min_time = 50
    max_time = 80
    time_variance = 12
    average_time = (min_time + max_time) / 2
    error = 16
    first_place_reward = 20000
    next_place = -1 * first_place_reward / 10
    guess_reward = 10000
    initial_bet_multiplier = 1.0
    min_cnt_bets = 2
    max_cnt_bets = 20
    average_cnt_bets = 8
    bets_cnt_sigma = 3
    average_bet = 2000
    bet_sigma = 1000
    simulations = 420

    time_step = (max_time - min_time) / teams_cnt
    # equidistant distribution
    # real_times = list(range(min_time, max_time, round(time_step)))
    # normal distribution
    real_times = sorted((round(random.gauss(average_time, time_variance)) for _ in range(teams_cnt)))

    print(f"times: {real_times}")

    results = []
    wins = []

    for _ in range(simulations):
        teams_money = [init_shitcoins for _ in range(teams_cnt)]

        for i in range(teams_cnt):
            teams_money[i] += first_place_reward + (i * next_place)

        # random estimates
        # estimates = [random.randint(min_time - error, max_time + error) for _ in range(teams_cnt)]

        # educated guess estimates
        estimates = [random.randint(real_times[i] - error, real_times[i] + error) for i in range(teams_cnt)]

        print(f"estimates: {estimates}")

        print(f"money: {teams_money}")
        for i in range(teams_cnt):
            diff = abs(real_times[i] - estimates[i])
            c = coefficient(diff, ESTIMATE_COEF)
            reward = guess_reward * initial_bet_multiplier * c
            print(f"team {i} diff {diff} coef {c} reward {reward}")
            teams_money[i] += reward

        bets = []
        # generate bets
        for i in range(teams_cnt):
            for _ in range(min_cnt_bets + round(random.gauss(average_cnt_bets, bets_cnt_sigma))):
                # if i == 3:
                #     # b = informed_bet(i, teams_cnt, average_bet, bet_sigma, real_times, estimates)
                #     # b = believer_bet(i, teams_cnt, average_bet, bet_sigma, estimates, average_time)
                #     # b = nonbeliever_bet(i, teams_cnt, average_bet, bet_sigma, estimates, average_time)
                #     # b = None  # play it safe
                #     b = random_bet(i, teams_cnt, average_bet * 2, bet_sigma)  # big better
                # else:
                #     b = random_bet(i, teams_cnt, average_bet, bet_sigma)
                b = random_bet(i, teams_cnt, average_bet, bet_sigma)
                if b:
                    team, bet, bet_type = b
                    bets.append((i, team, bet, bet_type))

        # eval bets
        for b in bets:
            team, team_bet, bet, bet_type = b
            if team == team_bet:
                print("it is illegal to bet on yourself")
                continue
            if teams_money[team] < bet:
                print(
                    f"team {team} does not have enough money to bet {bet} that {team_bet} will {bet_type_to_str(bet_type)}")
                continue
            teams_money[team] -= bet
            won = eval_bet(real_times, estimates, team_bet, bet, bet_type)
            print(f"team {team} bet {bet} that {team_bet} will {bet_type_to_str(bet_type)} and won {won}")
            teams_money[team] += won

        wins.append(teams_money.index(max(teams_money)))
        results.append(teams_money)
        print(f"money: {teams_money}")
        print()

    df = pandas.DataFrame(results)
    print(df)
    df.plot.hist(bins=50)
    plt.show()
    df.boxplot()
    plt.show()
    pandas.Series(wins).plot.hist(bins=teams_cnt)
    plt.show()


if __name__ == '__main__':
    main()
