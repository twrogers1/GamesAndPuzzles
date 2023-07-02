# prove the minimum number of coins needed to make any change between .01 and .99

from collections import OrderedDict
from textwrap import dedent


def tend_coins(amount: int) -> OrderedDict[int, int]:
    """
    From the given `amount` (in cents), determine the least amount of coins required to make change.
    For example, if `amount` is 25, return 1 quarter, rather of 2 dimes and 1 nickel.

    Possible coin values are 25, 10, 5, and 1 -- 50-cent pieces are not included as they are not common enough tender.
    
    Args:
        amount: the amount of change to make, given as an integer (e.g. $.25 = 25)

    Returns:
        An OrderedDict with K = coin, V = quantity
        (e.g. 32 = {25: 1, 5: 1, 1: 2})
    """
    if amount < 1 or amount > 99:
        raise ValueError("amount should be given as an int of cents between 1-99")
    
    quarters, amount = divmod(amount, 25)
    dimes, amount = divmod(amount, 10)
    nickels, pennies = divmod(amount, 5)
    
    # only include a coin value if at least 1 will be given back
    coins = OrderedDict()
    if quarters > 0: coins[25] = quarters
    if dimes > 0: coins[10] = dimes
    if nickels > 0: coins[5] = nickels
    if pennies > 0: coins[1] = pennies
    return coins


if __name__ == "__main__":
    quarters = 0
    dimes = 0
    nickels = 0
    pennies = 0
    for x in range(1, 100):
        # iterate from $.01 - $.99 and note the max number of each coin used
        coins = tend_coins(x)
        quarters = max(quarters, coins.get(25, 0))
        dimes = max(dimes, coins.get(10, 0))
        nickels = max(nickels, coins.get(5, 0))
        pennies = max(pennies, coins.get(1, 0))

    print(dedent(f"""
    💲 Minimum required coins:
    {quarters} Quarters
    {dimes} Dimes
    {nickels} Nickel
    {pennies} Pennies
    --------------------------
    {quarters + dimes + nickels + pennies} total coins
    """))
