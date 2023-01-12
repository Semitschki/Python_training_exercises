"""Algorithm that calculates the change like a cash register."""

MONEY_TYPES = (
500.0, 200.0, 100.0, 50.0, 20.0, 10.0, 5.0,
2.0, 1.0, 0.5, 0.20, 0.10, 0.05, 0.02, 0.01
)


def main(pay, cost):
    """This function calculates the back money."""
    back_money = {}
    if cost <= pay:
        difference = pay - cost
        for number in MONEY_TYPES:
            (count, difference) = divmod(difference, number)

            if count:
                back_money[number] = int(count)

                if difference == 0:
                    break
    return back_money
