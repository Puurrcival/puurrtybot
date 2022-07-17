import random
def get_random_quantity():
    random_q = list(range(2_000_000, 2_999_999))
    return str(random.choice(random_q)/1_000_000)
