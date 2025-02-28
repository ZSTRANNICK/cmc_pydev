def ask(prompt: str, valid: list[str] = None) -> str:
    print(prompt)
    while True:
        res = input()
        if not valid or res in valid:
            return res
        

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    pass
