def replace_text(n):
    Vowels = "aeiouAEIOU"
    for chrachter in n:
        if chrachter in Vowels:
            n = n.replace(chrachter, "!")
    return n


print(replace_text("saaaddd"))
