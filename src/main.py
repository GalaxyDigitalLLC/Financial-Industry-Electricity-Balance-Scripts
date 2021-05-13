from bitcoin import Bitcoin
from gold import Gold
from banking import Banking


if __name__ == "__main__":
    btc_file = './rsc/bitcoin.yaml'
    btc = Bitcoin(btc_file)
    print(btc)

    print()

    banking_file = './rsc/banking.yaml'
    banking = Banking(banking_file)
    print(banking)

    print()

    gold_file = './rsc/gold.yaml'
    gold = Gold(gold_file)
    print(gold)
