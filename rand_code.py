from random import randrange

def create_verify_code():
    code = randrange(10000)
    return f"{code:04d}"

strein = "aldfkger"
strein2 = ""
if __name__ == "__main__":

    print(len(strein2))