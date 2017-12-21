def censor(text, word):
    temp = ''
    result = ''
    for c in text:
        print("c: " + c)
        if(len(temp) == len(word)):
            for letter in temp:
                result += '*'
            temp = ''
        if(c == word[len(temp)]):
            temp += c
        else:
            result += temp
            result += c
            temp = ''
        print("temp: " + temp)
        print("Length of temp: " + str(len(temp)))
        print("Length of word: " + str(len(word)))
        print("Result: " + result)
    result += temp
    return result


print (censor("hey hey hey", "hey"))
