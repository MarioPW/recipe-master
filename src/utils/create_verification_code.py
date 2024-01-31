from random import randint

def create_verification_code() -> int: 
    code_list = [randint(0, 9) for _ in range(4)]
    if code_list[0] == 0: # If the number begins with 0, the 'int' type will be incorrect; 
       code_list[0] = 7   # so in that case, I changed it to a seven just because :)
    code_str = ''.join(map(str, code_list))
    code_int = int(code_str)
    return code_int