# literalnie-solver
Program do rozwiązywania gry słownej literalnie.

Program pobiera listę słów z PWN, wybiera tylko te o odpowiedniej długości, a następnie podaje sugestie na podstawie częstotliwości występowania liter na danej pozycji.

Użytkownik podaje informację zwrotną na podstawie sugestii w formacie _____, gdzie w miejscu _ należy wpisać litery C(orrect), P(resent) lub A(bsent).
Przykładowo dla sugestii KROWA, jeżeli K, R i W zotaną oznaczone jako niewsytępujące w haśle (oznaczone na szaro), O jako prawidłowe (oznaczone na zielono), a A jako prawidłowe (oznaczone na zielono), należy wpisać AACAP.

Do testowania programu najlepiej wykorzystać stronę literalnie.fun lub wordleplay.com/pl, przy czym wordleplay zawiera bardziej ograniczony zasób słów. W sytuacji, kiedy gra nie rozpoznaje słowa należy wpisać do programu "#", aby pominąć słowo.

Ze względu na ograniczenia GitHuba, plik ze słowami został podzielony na dwa. Można pobrać go również osobno ze strony PWN.
