import sys

mod = 16777216

def generate(secret, n):
    prices = [secret % 10]
    price_changes = []
    for _ in range(n):
        secret = (secret ^ (secret * 64)) % mod
        secret = (secret ^ (secret // 32)) % mod
        secret = (secret ^ (secret * 2048)) % mod
        prices.append(secret % 10)
        price_changes.append(prices[-1] - prices[-2])
    return prices, price_changes

if __name__ == '__main__':

    secrets = [int(line.strip()) for line in sys.stdin]

    sequence_dict = dict()
    for si in range(len(secrets)):
        secret = secrets[si]
        prices, price_changes = generate(secret, 2000)
        # print(f'{secret}:')
        # print(prices)
        # print(price_changes)

        for i in range(len(price_changes) - 4):
            sequence = tuple(price_changes[i:i+4])
            if sequence not in sequence_dict:
                sequence_dict[sequence] = dict()
            if si not in sequence_dict[sequence]:
                sequence_dict[sequence][si] = prices[i+4]
    
    sequence_dict_prices = {sequence: sum([price for si, price in sequence_prices.items()]) for sequence, sequence_prices in sequence_dict.items()}
    max_sequence, max_price = list(sorted(sequence_dict_prices.items(), key=lambda x: x[1]))[-1]
    print(max_sequence, max_price)