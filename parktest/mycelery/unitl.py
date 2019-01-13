import random


def generate_code():
    code_list = []
    for i in range(4):
        code_list.append(str(random.randint(0, 10)))
    code_str = ''.join(code_list)
    return code_str


