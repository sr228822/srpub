# Given a string with alpha-numeric characters and parentheses,
# return a string with balanced parentheses by removing the fewest
# characters possible. You cannot add anything to the string.

# Examples:
#  balance("()") == "()"
#  balance("a(b)c)") == "a(b)c"
#  balance(")(") == ""
#  balance("(((((") == ""
#  balance("(()()(") == "()()"
#  balance(")(())(") == "(())"
#  balance(")())(()()(") == "()()()"


def balance(txt):
    print(f"\n==== {txt} ===\n")
    res = txt
    remove = {}
    unclosed = []
    openp = 0
    for i, c in enumerate(txt):
        print(i, c, openp)
        if c == "(":
            openp += 1
            unclosed.append(i)

        if c == ")":
            if openp > 0:
                openp -= 1
                unclosed.pop()
            else:
                remove[i] = True

    print(f"openp: {openp}")
    print(f"remove: {remove}")
    print(f"unclosed: {unclosed}")

    for i in range(openp):
        toclose = unclosed.pop()
        remove[toclose] = True

    res = "".join(c for i, c in enumerate(txt) if i not in remove)
    print(f"res: {res}")

    if openp > 0:
        print("extra open")

    print(f"{txt}    =>    {res}")
    return res


if __name__ == "__main__":
    assert balance("()") == "()"
    assert balance("a(b)c)") == "a(b)c"
    assert balance(")(") == ""
    assert balance("(((((") == ""
    assert balance("(()()(") == "()()"
    assert balance(")(())(") == "(())"
    assert balance(")())(()()(") == "()()()"
    assert balance("((()))x(()") == "((()))x()"
    assert balance("(()x((()))") == "()x((()))" or "(()x(()))"
    assert balance("(()x(()") == "()x()"
