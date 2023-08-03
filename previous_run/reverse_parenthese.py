def reverseParentheses( s):
    res = ['']
    for c in s:
        print(res)
        if c == '(':
            res.append('')
        elif c == ')':
            print("on right", res)
            res[len(res) - 2] += res.pop()[::-1]
            print("on right", res)
        else:
            res[-1] += c
        print(res)
    return "".join(res)

def reverseParentheses2( s):
    opened = []
    pair = {}
    for i, c in enumerate(s):
        if c == '(':
            opened.append(i)
        if c == ')':
            j = opened.pop()
            pair[i], pair[j] = j, i

    print(pair)

    res = []
    i, d = 0, 1
    while i < len(s):
        print("in",res)
        if s[i] in '()':
            i = pair[i]
            d = -d
        else:
            res.append(s[i])
        i += d
        print("out",res)
    return ''.join(res)



print( reverseParentheses2( "((abc)de(123))"))