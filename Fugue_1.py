# umozliwienie skracania dowolnie dlugich plikow zadanych nazwa pliku +
# umozliwienie ustalenia dlugosci generowanego skrotu w bajtach (od 1 do maksymalnej, oryginalnej dlugosci skrotu:
# generowanie skrotow krotszych odbywa sie poprzez obciecie oryginalnego skrotu do zadanej dlugosci)
# wyswietlanie na ekran: nazwy skracanego pliku, dlugosc generowanego skrotu, wartosc skrotu szestnastkowo
# zapisanie uzyskanego skrotu do pliku +
# sprawdzenie poprzez wektory testowe

import math
import numpy as np

# s-box
s_box = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76], 
         [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
         [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
         [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
         [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
         [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
         [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
         [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
         [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
         [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
         [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
         [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
         [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
         [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
         [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
         [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

# vektor inicjalizujacy IV
vector_IV = np.matrix([[0xe9, 0x66, 0xe0, 0xd2, 0xf9, 0xfb, 0x91, 0x34], 
                       [0x52, 0x71, 0xd4, 0xb0, 0x6c, 0xf9, 0x49, 0xf8], 
                       [0xbd, 0x13, 0xf6, 0xb5, 0x62, 0x29, 0xe8, 0xc2], 
                       [0xde, 0x5f, 0x68, 0x94, 0x1d, 0xde, 0x99, 0x48]])

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
    print("Z paddingu otrzymalismy:")
    print(X_2_koncowa)
    return X_2_koncowa

# Inicjalize State
# tworzymy macierz S o 30 4 bajtowych kolumnach taka ze S_0,...,21 = 0   S_22,...,29 = IV
# for j in range(0, 22):
# S[:,j] = 0
# for j in range(0, 8):
# S[:, 22 + j] = IV[:,j]
def Inicjalize_State(vector_IV):
    # zamiast wykonac for powyzej stworzylam macierz int zerowa 4x30 
    # i ostatnie kolumny zamieniam na wektor inicjalizujacy
    S = np.zeros((4, 30), dtype = int)
    for j in range(0, 8):
        S[:, 22 + j] = vector_IV[:, j].flatten()
    print("Macierz po Inicjalize State:")
    print(S)
    return S

# TIX(P_i)
# dla kazdego elementu P_i ktory jest elementem z x_2
def TIX(P_i, S):
    # tworze wektor 4 bajtowy  P
    # biore wartosc zmiennej i przesuwam o podana ilosc bitow za pomoca >> w prawo a nastepnie biore otatnie (najmlodsze) 8 bitow
    vector_P = [(P_i >> 24) & 0xff, (P_i >> 16) & 0xff ,(P_i >> 8) & 0xff, P_i & 0xff]
    # S_10 += S_0
    S[:, 10] = S[:, 10] ^ S[:, 0]
    # S_0 = I
    S[:, 0] = vector_P
    # S_8 += S_0
    S[:, 8] = S[:, 8] ^ S[:, 0]
    # S_1 += S_24
    S[:, 1] = S[:, 1] ^ S[:, 24]
    return S


# otwieramy plik do odczytu
# przypisujemy zawartosc pliku do zmiennej zawartosc_pliku
# zamykamy plik
file_p = open("plik_tekst.txt", mode = 'r')
zawartosc_pliku = file_p.read()
file_p.close()
# wykonanie paddingu na zawartosci z pliku
X_2 = Padding(zawartosc_pliku)
# tworzenie stanu S
S = Inicjalize_State(vector_IV)