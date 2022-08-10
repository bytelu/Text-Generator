# Preprocess of the text corpus to random text sentences.
from collections import Counter
from random import choice
import re


def input_to_corpus():
    file = input("> ")
    file = open(file, "r", encoding="utf-8")
    processed_file = file.read()
    file.close()
    processed_file = processed_file.split()
    return processed_file


def corpus_to_bigram(corpus):
    return [[corpus[i], corpus[i + 1]] for i in range(len(corpus) - 1)]


def corpus_to_trigram(corpus):
    return [[corpus[i], corpus[i + 1], corpus[i + 2]] for i in range(len(corpus) - 2)]


def biagram_to_markov(biagram):
    markov_converted = {}
    for i in range(len(biagram)):
        markov_converted.setdefault(biagram[i][0], []).append(biagram[i][1])
    for key in markov_converted:
        markov_converted[key] = Counter(markov_converted[key])
    for key in markov_converted:
        markov_converted[key] = markov_converted[key].most_common()
    return markov_converted


def trigram_to_markov(trigram):
    markov_converted = {}
    for i in range(len(trigram)):
        markov_converted.setdefault(f"{trigram[i][0]} {trigram[i][1]}", []).append(trigram[i][2])
    for key in markov_converted:
        markov_converted[key] = Counter(markov_converted[key])
    for key in markov_converted:
        markov_converted[key] = markov_converted[key].most_common()
    return markov_converted


def markov_statistics(markov_):
    while True:
        option = input("")
        if option == "exit":
            break
        if option in markov_:
            print("Head: {}".format(option))
            for i in range(len(markov_[option])):
                print("Tail: {}\tCount: {}".format(markov_[option][i][0], markov_[option][i][1]))
        else:
            print("Key Error. The request word is not in the model. Please input another word.")


def random_text(markov_, repetitions):
    for _ in range(repetitions):
        text = []
        while True:
            head = choice(list(markov_.keys()))
            if head[len(head) - 1] != "." and head[len(head) - 1] != "!" and head[len(head) - 1] != "?":
                if re.search(r"^[A-Z].*", head):
                    break
        text.append(head)
        while True:
            tail = choice(list(markov_[head]))[0]
            text.append(tail)
            head = tail
            if len(text) >= 5:
                if head[len(head) - 1] == "." or head[len(head) - 1] == "!" or head[len(head) - 1] == "?":
                    break
        print(" ".join(text))


def random_text_trigram(markov, repetitions):
    for _ in range(repetitions):
        text = []
        while True:
            head = choice(list(markov.keys()))
            sub_head = head.split()[0]
            if sub_head[len(sub_head) - 1] != "." and sub_head[len(sub_head) - 1] != "!" and sub_head[len(sub_head) - 1] != "?":
                if re.search(r"^[A-Z].*", sub_head):
                    break
        text.append(head)
        while True:
            tail = choice(list(markov[head]))[0]
            text.append(tail)
            head = "{} {}".format(head.split()[1], tail)
            if len(text) >= 4:
                if tail[len(tail) - 1] == "." or tail[len(tail) - 1] == "!" or tail[len(tail) - 1] == "?":
                    break
        print(" ".join(text))


if __name__ == "__main__":

    words_from_corpus = input_to_corpus()
    trigram = corpus_to_trigram(words_from_corpus)
    markov = trigram_to_markov(trigram)
    random_text_trigram(markov, 10)
