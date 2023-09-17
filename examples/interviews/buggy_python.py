class Token:
    def __init__(self, token, token_type):
        self.chars = dict.fromkeys(token)
        self.type = token_type
        self.dot = "." in self.chars

    def display(self):
        print(self.chars, self.type)

    def match(self, text):
        if self.type == "*":
            offsets = [0]
            index = 0
            while index < len(text) and self.matchBase(text[index]):
                index = index + 1
                offsets.append(index)
            return offsets
        if len(text) > 0 and self.matchBase(text[0]):
            return [1]
        return []

    def matchBase(self, char):
        if self.dot or char in self.chars:
            return True
        return False


def tokenize(pattern):
    tokens = []
    i = 0
    while i < len(pattern):
        sub = str(pattern[i])
        if pattern[i] == "[":
            start = i
            while pattern[i] != "]":
                i = i + 1
            sub = pattern[start + 1 : i]
        if i + 1 < len(pattern) and pattern[i + 1] == "*":
            tokens.append(Token(sub, "*"))
            i = i + 2
        else:
            tokens.append(Token(sub, "base"))
            i = i + 1

    return tokens


def matchWorker(tokens, text):
    if len(tokens) == 0 and len(text) == 0:
        return True
    if len(tokens) == 0 and len(text) > 0:
        return False
    offsets = tokens[0].match(text)
    for offset in offsets:
        if matchWorker(tokens[1:], text[offset:]):
            return True
    return False


def match(pattern, text):
    tokens = tokenize(pattern)
    return matchWorker(tokens, text)


def testMatch(pattern, test, expected):
    actual = match(pattern, test)
    result = "FAIL"
    if expected == actual:
        result = "SUCCESS"
    print(pattern, test, result)


def main():
    testMatch("abc", "abc", True)
    testMatch("a.c", "abc", True)
    testMatch("aa*", "a", True)
    testMatch("aa*", "aaaaaab", False)
    testMatch("a[abc]*", "aacacbaaab", True)
    testMatch("a[abc]*", "aacacbavab", False)
    testMatch("a[abc]*gg", "aacacbaabgg", True)
    testMatch("a[a.bc]*", "aacacbavab", True)


if __name__ == "__main__":
    main()
