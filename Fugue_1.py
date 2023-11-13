# umozliwienie skracania dowolnie dlugich plikow zadanych nazwa pliku
# umozliwienie ustalenia dlugosci generowanego skrotu w bajtach (od 1 do maksymalnej, oryginalnej dlugosci skrotu:
# generowanie skrotow krotszych odbywa sie poprzez obciecie oryginalnego skrotu do zadanej dlugosci)
# wyswietlanie na ekran: nazwy skracanego pliku, dlugosc generowanego skrotu, wartosc skrotu szestnastkowo
# zapisanie uzyskanego skrotu do pliku +
# sprawdzenie poprzez wektory testowe

import math

# funkcja zapiujaca do pliku
def ZapisDoPliku(skrot):
    file_k = open("plik_skrot.txt", mode = 'w')
    file_k.write(skrot)
    file_k.close()
    return 

# PADDING
# bierze wartosc wejsciowa X o wartosci n bitow
# nastepnie jesli n nie jest wielokrotnoscia 32 to uzupelnia zerami tak aby otrzymac wielokrotnosc 32 bitow (4 bajtow)
# jesli n mod(32) = 0 to nie uzupelniamy zerami
# X' - sekwencja po m bajtow, gdzie m - wielokrotnosc 4
# X' - wartosc wejsciowa + zera
# X' zamieniamy na reprezentacje m bajtowa
# nastepnie dlugosc n przedstawiamy w reprezentacji jako osmiobajtowa liczba calkowita (big-endian)
# X" to X' + osmiobajtowa reprezentacja n
def Padding(zawartosc_pliku):
    # zamieniamy zmienna zawartosc_pliku ktora jest typu string (jest to ciag znakow, liter, liczb) na zapis binarny
    # binary_string - jest to zmienna ktora bedzie przechowywala reprezentacje binanra zmiennej zawartosc_pliku
    binary_string = ""
    # przechodzimy przez kazdy znak w zmiennej zawrtosc_pliku
    for znak in zawartosc_pliku:
        # ord(znak) - uzyskujemy kod Unicode dla kazdego znaku
        znak_code = ord(znak)
        # zamieniamy kod na reprezentacje binarna 
        binary_representation = bin(znak_code)[2:]
        binary_string = binary_string + binary_representation

    # int_representation to reprezentacja binary_string w postaci int
    int_representation = int(binary_string, 2)

    # jesli dlugosc binary_string jest wielokrotnoscia 32 to do X_1 przypisujemy int_representation
    if(len(binary_string) % 32 == 0):
        X_1 = int_representation
    # w przeciwnym przypadku oprocz przypisania uzupelniamy zerami aby dlugosc X_1 byla wielokrotnoscia 32
    else:
        X_1 = int_representation
        while(len(bin(X_1)[2:]) % 32 != 0):
            # przesuniecie bitowe, tak aby po lewej stronie dopisywac '0' aby uzyskac zmienna o dlugosci (w bitach) rowna wielokrotnosci 32
            X_1 = X_1 << 1

    # dlugosc wartosci wejsciowej prezentujemy jako osmiobajtoey integer i dodajemy do X_2
    # dlugosc binary_string zamieniamy na int
    binary_string_len = len(binary_string)
    b_s_len_int = int(binary_string_len)

    # przesuwamy X_1 o 64 bity (8 bajtow) 
    # poniewaz nasze X_2 ma byc X_1 + dlugosc wartosci wejsciowej jako osmiobajtowy integer
    # wiec jak dodamy do X_1 b_s_len_int to otrzymamy wartosc wejsciowa i po niej osmiobajtowy integer dlugosci wartosci wejsciowej
    X_1 = X_1 << 64
    X_2 = X_1 + b_s_len_int

    # podzial otrzymanej wartosci po 4 bajty (32 bity)
    # bedzie to wykorzystywane w pozostalych funkcjach 
    # X_2_koncowa - tablica przegowujaca po 4 bajty wartosci koncowej
    X_2_koncowa = []
    for i in range(0, int((len(bin(X_2)[2:]))/32)):
        # w naszej zmiennej temp pozostaja ostatnie (najmlodsze) bity wartosci wejsciowej 
        temp = X_2 & 0xffffffff
        # wpisujemy je do tablicy
        X_2_koncowa.append(temp)
        # nastepnie przesuwamy o 32 bity w prawo aby zajac sie nastepnymi 32 bitami
        X_2 = X_2 >> 32
    print(X_2_koncowa)

    return X_2_koncowa

# otwieramy plik do odczytu
# przypisujemy zawartosc pliku do zmiennej zawartosc_pliku
# zamykamy plik
file_p = open("plik_tekst.txt", mode = 'r')
zawartosc_pliku = file_p.read()
file_p.close()
X_2 = Padding(zawartosc_pliku)
