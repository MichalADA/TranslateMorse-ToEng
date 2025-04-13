# TranslateMorse-ToEng
Fast project just for fun 
Translator Kodu Morse'a
Program do tłumaczenia tekstu na kod Morse'a i odwrotnie, z graficznym interfejsem użytkownika i funkcją odtwarzania dźwięku.

Do poprawy interfejs graficzny 

Funkcje
Tłumaczenie tekstu na kod Morse'a
Tłumaczenie kodu Morse'a na tekst
Odtwarzanie kodu Morse'a jako dźwięku
Interfejs graficzny oparty na Tkinter
Struktura projektu
morse_translator/
|-- __init__.py
|-- main.py         # Główny moduł z interfejsem GUI
|-- morse_utils.py  # Funkcje translacyjne
|-- morse_sound.py  # Funkcje do odtwarzania dźwięku

README.md           # Ten plik
Wymagania
Python 3.6 lub nowszy
Biblioteka tkinter (standardowo dostępna w większości dystrybucji Pythona)
Uruchomienie
Masz dwie opcje uruchomienia programu:

Opcja 1: Uruchomienie z głównego modułu
bash
python morse_translator/main.py
Opcja 2: Uruchomienie z pliku bezpośredniego (jeśli masz problemy z opcją 1)
bash
python bezposredni_start.py
Rozwiązywanie problemów
Jeśli napotkasz problemy z uruchomieniem programu:

Problemy z importowaniem modułów - użyj pliku bezposredni_start.py, który zawiera cały kod w jednym pliku
Problemy z dźwiękiem - dźwięk jest opcjonalny, program będzie działać nawet jeśli funkcja dźwięku nie działa
Kod Morse'a
Kod Morse'a to metoda kodowania znaków alfabetu jako sekwencji krótkich i długich sygnałów, zwanych kropkami i kreskami:

Kropka (.) to krótki sygnał
Kreska (-) to długi sygnał (trzy razy dłuższy od kropki)
Przerwa między elementami znaku jest równa kropce
Przerwa między znakami jest równa krótce
Przerwa między słowami jest równa siedmiu kropkom
Na przykład:

SOS = ... --- ...
HELLO = .... . .-.. .-.. ---
Licencja
Ten projekt jest dostępny na licencji open source.

