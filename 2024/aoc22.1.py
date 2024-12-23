import sys

mod = 16777216

def generate(secret, n):
    for _ in range(n):
        secret = (secret ^ (secret * 64)) % mod
        secret = (secret ^ (secret // 32)) % mod
        secret = (secret ^ (secret * 2048)) % mod
    return secret

if __name__ == '__main__':

    secrets = [int(line.strip()) for line in sys.stdin]

    total = 0
    for secret in secrets:
        total = total + generate(secret, 2000)
    print(total)