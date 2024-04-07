def replace_text(n):
    vowels = "aeiouAEIOU"
    for chrachter in n:
        if chrachter in vowels:
            n = n.replace(chrachter, "!")
    return n


print(replace_text("aeion"))
