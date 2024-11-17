counter = 0


# Importowanie listy słów pobranej z PWN oraz wybór tylko tych, które mają dokładnie 5 liter.
# Ze względu na ograniczenia GitHuba plik ze słowami został podzielony na dwa.
def import_word_list(path1="slowa1.txt", path2="slowa2.txt", word_length=5):
    try:
        with open(path1, "r", encoding="utf-8") as word_list:
            words1 = [word.strip() for word in word_list.readlines() if len(word.strip()) == word_length]
        with open(path2, "r", encoding="utf-8") as word_list:
            words2 = [word.strip() for word in word_list.readlines() if len(word.strip()) == word_length]
        return words1 + words2
    except FileNotFoundError as err:
        print('file does not exist')
        raise err


# Obliczanie częstotliwości występowania słów
def letter_frequency(words):
    frequencies = {}

    for word in words:
        for pos, letter in enumerate(word):
            if letter not in frequencies:
                frequencies[letter] = [0, 0, 0, 0, 0]

            frequencies[letter][pos] += 1

    return frequencies


# Utworzenie rankingu słów, poprzez zsumowanie łącznej częstotliwości występowania danej litery w konkretnej pozycji.
# Zasugerowanie słowa, które osiąga najlepszy wynik. Podczas pierwszej iteracji odrzuamy słowa z powtarzającymi się
# literami, gdyż zwiększa to szansę na to, aby uzyskać większą informację początkową.
def score_words(words, frequencies, first_iteration=False):
    max_score = 0
    suggestion = ""

    for word in words:
        score = sum(frequencies[letter][i] for i, letter in enumerate(word))

        if score > max_score:

            if first_iteration:
                if not len(set(word)) == len(word):
                    continue

            max_score = score
            suggestion = word

    return suggestion


# Algorytm odfiltrowywania słów
def filter_words(words, correct, present, absent, suggestion):
    filtered = []

    for word in words:
        match = True

        # Zapewnia, że sugestia nie zostanie powtórzona.
        if word == suggestion:
            match = False

        for i, letter in enumerate(word):
            # Odrzucenie słów z literami, które nie występują w haśle.
            if letter in absent:
                # Zapewnia, aby sugestia nie została powtórzona w rzadkich sytuacjach, gdy w haśle będą występowały
                # dwie te  same litery, gdzie jedna będzie oznaczona jako prawidłowa, a druga jako błędna.
                if letter not in correct and letter not in present:
                    match = False
                    break

            # Odrzucenie słów, które nie zawierają poprawnej litery na tym samym miejscu, co w haśle.
            if correct[i] and word[i] != correct[i]:
                match = False
                break

            if not present[i] is None:
                # Odrzucenie słów, w których dana litera została oznaczona jako obecna, ale występująca
                # na innym miejscu w haśle.
                if letter in present and word[i] == present[i]:
                    match = False
                    break
                # Odrzucenie słów, które nie zawierają litery wskazanej jako obecnej na innym miejscu w haśle.
                if present[i] not in word:
                    match = False
                    break

        if match:
            filtered.append(word)

    return filtered


# Interpretacja liter zwracanych przez użytkownika, jako poszczególne listy liter i pozycji.
def process_feedback(words, suggestion, feedback):
    global counter

    correct = [None, None, None, None, None]
    present = [None, None, None, None, None]
    absent = [None, None, None, None, None]

    if feedback == "#":
        pass
    else:
        counter += 1
        for i, letter in enumerate(feedback):
            if feedback[i] == 'c' or feedback[i] == 'C':
                correct[i] = suggestion[i]
            if feedback[i] == 'p' or feedback[i] == 'P':
                present[i] = suggestion[i]
            if feedback[i] == 'a' or feedback[i] == 'A':
                absent[i] = suggestion[i]

    filtered_word = filter_words(words, correct, present, absent, suggestion)
    return filtered_word


# Interakcja z użytkownikiem
def get_feedback(suggestion):
    print("Proszę podać informację zwrotną w formacie _____,")
    print("Gdzie w miejscu _ należy wpisać:")
    print("C - jeżeli litera znajduje się w odpowiednim miejscu (kolor zielony),")
    print("P - jeżeli litera znjaduje się w innym miejscu (kolor żółty),")
    print("A - jeżeli litera nie znajduje się w haśle (kolor szary).")
    print()
    print("Sugestia: " + suggestion)

    feedback = input()
    return feedback


# Wywoływanie w pętli poszczególnych funkcji, aż do rozwiązania zagadki lub wystąpienia błędu.
#
# Symoble nadpisujące:
#
# "#" - do pominięcia słowa, kiedy program z zagadką nie rozpoznaje danego słowa (lista wszystkich słów z PWN zawiera
# słowa, które często nie przypominają nawet prawdziwych słów lub są odmienione w takiej liczbie, bądź przypadku, że nie
# jest ono rozpoznawane).
def main():
    global counter
    is_finished = False

    words = import_word_list()
    initial_words = len(words)
    print("Zaimportowano " + str(initial_words) + " słów.")

    frequencies = letter_frequency(words)
    suggestion = score_words(words, frequencies, first_iteration=True)
    feedback = get_feedback(suggestion)

    if feedback == "ccccc" or feedback == "CCCCC":
        counter += 1
        is_finished = True

    while not is_finished:
        words = process_feedback(words, suggestion, feedback)
        reduced = initial_words - len(words)
        initial_words = len(words)
        print("Zredukowano ilość możliwych słów o " + str(reduced) + ", możliwych " + str(len(words)) + " słów.")

        if len(words) < 10:
            print("Możliwe słowa to:")
            print(words)
        if len(words) == 0:
            print("Wystąpił błąd w dopasowaniu słowa.")
            exit()

        suggestion = score_words(words, frequencies)
        feedback = get_feedback(suggestion)

        if feedback == "ccccc" or feedback == "CCCCC":
            counter += 1
            is_finished = True

    print("Odgadnięto hasło w " + str(counter) + " próbach.")
    exit()


main()
