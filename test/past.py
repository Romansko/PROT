import re    # For each word in words, remove ending of "e" or "ed" using Regex, add "ed" and append to past_tense.
if __name__ == '__main__':
    words = ["adopt", "bake", "beam", "cook", "time", "grill", "waved", "hire"]
    past_tense = list(map(lambda word: re.sub("(e|ed)$", "", word) + "ed", words))
    print(past_tense)
