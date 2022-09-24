import random

BET_COEF = [(1, 1.0625), (2, 1.125), (4, 1.25), (8, 1.5), (16, 2.0), (128, 3.0)]
ESTIMATE_COEF = [(1, 3.0), (2, 2.0), (4, 1.0), (8, -0.0), (16, -0.5), (32, -1.0), (64, -2.0), (128, -3.0)]


def coefficient(diff, coef):
    for max_diff, c in coef:
        if max_diff >= diff:
            return c
    return 0


def eval_bet(real_times, estimates, team, bet, bet_type):
    diff = real_times[team] - estimates[team][1]
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
    return "be better" if bet_type == 1 else "be worse"


def print_result(res):
    return [(f"team {i + 1}", v) for i, v in enumerate(res)]


def main():
    init_shitcoins = 10000
    teams_cnt = 7
    first_place_reward = 20000
    next_place = -1 * first_place_reward / 10
    guess_reward = 10000
    initial_bet_multiplier = 1.0

    real_times = [
        151,
        118,
        160,
        136,
        128,
        142,
        130,
    ]

    estimates = [
        (0, 60),
        (5, 69),
        (2, 87),
        (4, 90),
        (1, 100),
        (6, 100),
        (3, 102),
    ]

    estimates.sort()

    print(f"estimates: {print_result([i[1] for i in estimates])}")

    print(f"times: {print_result(real_times)}")

    teams_money = [init_shitcoins for _ in range(teams_cnt)]

    for i, v in enumerate(sorted(enumerate(real_times), key=lambda x: x[1])):
        team, _ = v
        reward = first_place_reward + (i * next_place)
        print(f"team {team + 1} position award {team}: {reward}")
        teams_money[team] += reward

    print(f"money with rewards: {print_result(teams_money)}")

    for i in range(teams_cnt):
        diff = abs(real_times[i] - estimates[i][1])
        c = coefficient(diff, ESTIMATE_COEF)
        reward = guess_reward * initial_bet_multiplier * c
        print(f"team {i + 1} diff {diff} coef {c} reward {reward}")
        teams_money[i] += reward

    print(f"money with estimate bonus: {print_result(teams_money)}")

    bets = [
        (0, 5 - 1, 5000, -1),
        (0, 4 - 1, 5000, 1),
        (0, 6 - 1, 5000, -1),

        (1, 1 - 1, 2000, -1),
        (1, 6 - 1, 2000, -1),
        (1, 4 - 1, 2000, 1),
        (1, 7 - 1, 2000, 1),

        (2, 1 - 1, -1, 1666.666667),
        (2, 2 - 1, -1, 1666.666667),
        (2, 4 - 1, -1, 1666.666667),
        (2, 5 - 1, -1, 1666.666667),
        (2, 6 - 1, -1, 1666.666667),
        (2, 7 - 1, -1, 1666.666667),
        (2, 7 - 1, 1, 10000),
    ]

    for i in range(10000):
        bets.append((3, 0, 1000, -1))

    bets += [
        (4, 1 - 1, 500, - 1),
        (4, 2 - 1, 200, 1),
        (4, 3 - 1, 200, 1),
        (4, 4 - 1, 200, 1),
        (4, 6 - 1, 1000, - 1),
        (4, 7 - 1, 200, 1),

        (5, 1 - 1, 2000, - 1),
        (5, 2 - 1, 2000, 1),
        (5, 4 - 1, 2000, 1),
        (5, 7 - 1, 2000, 1),

        (6, 6 - 1, 3000, -1),
        (6, 1 - 1, 3000, -1),
        (6, 2 - 1, 3000, 1),
    ]

    # eval bets
    for b in bets:
        team, team_bet, bet, bet_type = b
        if team == team_bet:
            print("it is illegal to bet on yourself")
            continue
        if teams_money[team] < bet:
            print(
                f"team {team + 1} does not have enough money to bet {bet} that {team_bet + 1} will {bet_type_to_str(bet_type)}")
            continue
        teams_money[team] -= bet
        won = eval_bet(real_times, estimates, team_bet, bet, bet_type)
        print(f"team {team + 1} bet {bet} that {team_bet + 1} will {bet_type_to_str(bet_type)} and won {won}")
        teams_money[team] += won

    print(f"final money: {print_result(teams_money)}")


if __name__ == '__main__':
    main()
