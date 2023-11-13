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

# otwieramy plik do odczytu
# przypisujemy zawartosc pliku do zmiennej zawartosc_pliku
# zamykamy plik
file_p = open("plik_tekst.txt", mode = 'r')
zawartosc_pliku = file_p.read()
file_p.close()

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
    # uzupelniamy zerami tak aby kazda reprezentacja bianarna miala dokladnie 8 znakow 
    # binary_string = binary_string + binary_representation.zfill(8)
print(binary_string)
print(type(binary_string))
# int_representation to reprezentacja binary_string w postaci int
int_representation = int(binary_string, 2)
print(int_representation)
print(type(int_representation))

# jesli dlugosc binary_string jest wielokrotnoscia 32 to do X_1 przypisujemy int_representation
if(len(binary_string) % 32 == 0):
    X_1 = int_representation
# w przeciwnym przypdaku oprocz przypisania uzupelniamy zerami aby dlugosc X_1 byla wielokrotnoscia 32
else:
    X_1 = int_representation
    while(len(bin(X_1)[2:]) % 32 != 0):
        # przesuniecie bitowe, tak aby po lewej stronie dopisywac '0' aby uzyskac zmienna o dlugosci (w bitach) rowna wielokrotnosci 32
        X_1 = X_1 << 1
print(X_1)
print(bin(X_1)[2:])