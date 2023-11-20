# FUGUE 256 - implementacja

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

# macierz N wykorzystywana W Super-Mix w SMIX
N = np.matrix([[0x01, 0x04, 0x07, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00], 
                [0x00, 0x01, 0x00, 0x00, 0x01, 0x01, 0x04, 0x07, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00], 
                [0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x07, 0x01, 0x01, 0x04, 0x00, 0x00, 0x01, 0x00], 
                [0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x04, 0x07, 0x01, 0x01],
                [0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x07, 0x01, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00],
                [0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x04, 0x07, 0x00, 0x01, 0x00, 0x00],
                [0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x01, 0x00, 0x04],
                [0x04, 0x07, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x06, 0x04, 0x07, 0x01, 0x07, 0x00, 0x00, 0x00],
                [0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x01, 0x06, 0x04, 0x07],
                [0x07, 0x01, 0x06, 0x04, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00],
                [0x00, 0x00, 0x00, 0x07, 0x04, 0x07, 0x01, 0x06, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x05, 0x04, 0x07, 0x01],
                [0x01, 0x05, 0x04, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00],
                [0x00, 0x00, 0x04, 0x00, 0x07, 0x01, 0x05, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00],
                [0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x04, 0x07, 0x01, 0x05, 0x00, 0x00, 0x00, 0x00]])


# funkcja zapiujaca do pliku
def ZapisDoPliku(skrot):
    file_k = open("plik_skrot.txt", mode = 'w')
    file_k.write(skrot)
    file_k.close()
    print("Skrot zostal zapisany do: plik_skrot.txt")
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
# na koniec X" dzielimy na czterobajtowe slowa
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
    # X_2_koncowa - tablica przechowujaca po 4 bajty wartosci koncowej otrzymanej podczas wykonywania paddingu
    X_2_koncowa = []
    for i in range(0, int((len(bin(X_2)[2:]))/32)):
        # w naszej zmiennej temp pozostaja ostatnie (najmlodsze) bity wartosci wejsciowej 
        temp = X_2 & 0xffffffff
        # wpisujemy je do tablicy
        X_2_koncowa.append(temp)
        # nastepnie przesuwamy o 32 bity w prawo aby zajac sie nastepnymi 32 bitami
        X_2 = X_2 >> 32
    #print("Z paddingu otrzymalismy:")
    #print(X_2_koncowa)
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

# RORn
# rotacja kolumn macierzy S w prawo o n kolumn
def RORn(S, n):
    # trzeba zrobic kopie macierzy S, 
    # poniewaz temp = S powoduje ze do zmiennej temp oraz S przypisana jest ta sama macierz i przy zmianie macierzy zmienia sie zarowno S jak i temp
    temp = S.copy()
    for i in range(0, 30):
        # indeks kolumny, modulo 30 zeby uniknac ujemnych wartosci
        j = (i - n) % 30
        S[:, i] = temp[:, j]
    return S

# CMIX
# mieszanie kolumn
def CMIX(S):
    # S_0 += S_4
    S[:, 0] = S[:, 0] ^ S[:, 4]
    # S_1 += S_5
    S[:, 1] = S[:, 1] ^ S[:, 5]
    # S_2 += S_6
    S[:, 2] = S[:, 2] ^ S[:, 6]
    # S_15 += S_4
    S[:, 15] = S[:, 15] ^ S[:, 4]
    # S_16 += S_5
    S[:, 16] = S[:, 16] ^ S[:, 5]
    # S_17 += S_6
    S[:, 17] = S[:, 17] ^ S[:, 6]
    return S

# S-BOX
# skrzynka podstawieniowa
def S_BOX (s_box, W):
    # po wierszach w macierzy W 
    for i in range(0, 4):
        # po kolumnach w macierzy W
        for j in range(0, 4):
            # column to nr kolumny w s_box
            # column to ostatnia 4 bitowa wartosc W[i, j]
            column = W[i, j] & 0xf
            # row to nr wiersza w s_box
            # nastepnie przsuwamy wartosc W[i,j] o 4 bity i odczytujemy 4 ostatnie bity jako row
            row = (W[i, j] >> 4) & 0xf
            # przypisujemy do W[i,j] wartosc z s_box[row][column]
            W[i, j] = s_box[row][ column]
    return W

# SMIX
# zawiera S-box oraz Super-Mix 
# S-box jest zdefiniowany w oddzielnej funkcji, tutaj jest tylko wywolywany
# tutaj bedzie zdefiniowany Super-Mix
def SMIX(S):
    # z macierzy S bierzemy pierwsze 4 kolumny i tworzymy z nich 4x4 macierz W
    W = S[:, :4]
    # wszystkie operacje beda wykonywane na macierzy W
    # najpierw wykonany bedzie S-BOX
    W = S_BOX(s_box, W)
    # macierz W przeksztalcamy w wentor W gdzie (i+4j)bajt wektora to bajt z i-tego wiersza i j-tej kolumny macierzy
    W = [W[0, 0], W[0, 1], W[0, 2], W[0, 3], W[1, 0], W[1, 1], W[1, 2], W[1, 3], W[2, 0], W[2, 1], W[2, 2], W[2, 3], W[3, 0], W[3, 1], W[3, 2], W[3, 3]]
    # Super-Mix
    # N_t - transponowana macierz N
    N_t = np.transpose(N)
    # N_W - wynik mnożenia macierzy N oraz wektora W
    N_W = np.dot(N, W)
    # wyniki musza byc w ciele GF(2^8) dlatego wykonywane jest modulo 256
    for i in range(len(N_W)):
        N_W = N_W % 256
    #tworzymy wektor pomocniczy:
    """
    suma(i!=j)=W[0,1]+W[0,2]+W[0,3]                0                           0                                 0
                  0                 suma(i!=j)=W[1,0]+W[1,2]+W[1,3]            0                                 0
                  0                                0               suma(i!=j)=W[2,0]+W[2,1]+W[2,3]               0
                  0                                0                           0                  suma(i!=j)=W[3,0]+W[3,1]+W[3,2] 
    """
    wektor_pom = [W[1]^W[2]^W[3], 0, 0, 0, 0, W[4]^W[6]^W[7], 0, 0, 0, 0, W[8]^W[9]^W[11], 0, 0, 0, 0, W[12]^W[13]^W[14]]
    # N_t_wektor_pom - wynik mnożenia macierzy N_t oraz wektoa pomocniczego
    N_t_wektor_pom = np.dot(N_t, wektor_pom)
    # wyniki musza byc w ciele GF(2^8) dlatego wykonywane jest modulo 256
    for i in range(len(N_t_wektor_pom)):
        N_t_wektor_pom = N_t_wektor_pom % 256
    # teraz W = N_W + N_t_wektor_pom
    W = N_W ^ N_t_wektor_pom
    #S[:, :4] = W
    # teraz macierz W zmieniana jest na macierz 4x4 oraz jej wartosci sa przypisane do pierwszech 4 kolumn i wierszy macierzy S za pomoca reshape
    S[:, :4] = W.reshape((4, 4))
    return S

# ostateczna funkcja tworzenia skrotu wiadomosci
# skrot ma 256 bitow czyli 32 bajty
def Tworzenie_Skrotu(S):
    # skrot - 256 bitow wyjscia
    # skrot tworza S1 S2 S3 S4 S15 S16 S17 S18
    skrot = ""
    nr_kolumn = [1, 2, 3, 4, 15, 16, 17, 18]
    # po kolumnach
    for i in nr_kolumn:
        # po wierszach
        for j in range(4):
            # dopisywanie kolujnych wartosci macierzy jako string do zmiennej skrot
            skrot  = skrot + str(S[j,i])
    # utworzony skrot liczy 256 bitow    
    skrot = int(skrot)    
    return skrot

# generowanie skrotow o okreslonej dlugosci
# obciecie oryginalnego skrotu do zadanej dlugosci
def Skrot_Dlugosc(skrot, dlugosc_skrotu, w_skracania):
    # moj skrot to najstarsze bajty:
    if(int(w_skracania) == 1):
        # przesuniecie bitowe w prawo >> (32 - dlugosc_skrotu) * 8
        skrot = skrot >> ((32 - int(dlugosc_skrotu)) * 8)
    else:
        # moj skrot do najmlodsze bajty
        i = 1
        mnoznik = 0xff
        while(i < int(dlugosc_skrotu)):
            # przesuniecie bitowe w lewo (dodanie 8 bitow 0)
            mnoznik = mnoznik << 8
            # dopisanie na koncu mnoznika (8 ostatnich bitow) wartosc ff czyli 11111111
            mnoznik = mnoznik | 0xff
            i = i + 1
        skrot = skrot & mnoznik 
    return skrot

nazwa_pliku = input("Podaj nazwe pliku do skrocenia:")
print("Skracany plik: ", nazwa_pliku)
dlugosc_skrotu = input("\nPodaj dlugoc generowanego skrotu w bajtach od 1 do 32: ")
# dopoki nie zostanie podana wartosc dlugosci skrotu z przedzialu od 1 do 32
while ((int(dlugosc_skrotu) < 1) or (int(dlugosc_skrotu) > 32)):
    print("Bledna wartosc dlugosci skrotu")   
    dlugosc_skrotu = input("Podaj dlugoc generowanego skrotu w bajtach od 1 do 32: ")
print("Dlugosc generowanego skrotu: ", dlugosc_skrotu)

print("\nWybor sposob skaracania oryginalnego skrotu:")
print("Wybierz 1 jesli chcesz aby skrot skladal sie z najstarszych bajtow")
print("Wybierz 2 jesli chcesz aby skrot skladal sie z najmlodszych bajtow")
w_skracania = input("Twoj wybor: ")
while ((int(w_skracania) != 1) and (int(w_skracania) != 2)):
    print("Wybor sposob skaracania oryginalnego skrotu:")
    print("Wybierz 1 jesli chcesz aby skrot skladal sie z najstarszych bajtow")
    print("Wybierz 2 jesli chcesz aby skrot skladal sie z najmlodszych bajtow")
    w_skracania = input("Twoj wybor: ")

# otwieramy plik do odczytu
# przypisujemy zawartosc pliku do zmiennej zawartosc_pliku
# zamykamy plik
file_p = open(nazwa_pliku, mode = 'r')
zawartosc_pliku = file_p.read()
file_p.close()

# wykonanie paddingu na zawartosci z pliku
X_2 = Padding(zawartosc_pliku)

# tworzenie macierzy stanu S
S = Inicjalize_State(vector_IV)
#print("Macierz po Inicjalize State:")
#print(S)

# The Round Transformation R
for i in range(0, len(X_2)):
    # wykonanie TIX
    S = TIX(X_2[i], S)
    # wykonanie ROR3
    S = RORn(S, 3)
    # wykonanie CMIX
    S = CMIX(S)
    # wykonanie SMIX
    S = SMIX(S)
    # wykonanie ROR3
    S = RORn(S, 3)
    # wykonanie CMIX
    S = CMIX(S)
    # wykonanie SMIX
    S = SMIX(S)

#print("Macierz S po Round Transfotmatoin R")
#print(S)

# The Final Round G
# wykonanie 10 razy {ROR3;CMIX;SMIX}
for i in range(0, 10):
    # wykoanie ROR3
    S = RORn(S, 3)
    # wykonanie CMIX
    S = CMIX(S)
    # wykonanie SMIX
    S = SMIX(S)
# wykonanie 13 razy:
# S_4 += S_0; S_15 += S_0; ROR15; SMIX
# S_4 += S_0; S_16 += S_0; ROR14; SMIX
for j in range(0, 13):
    S[:, 4] = S[:, 4] ^ S[:, 0]
    S[:, 15] = S[:, 15] ^ S[:, 0]
    # wykoanie ROR15
    S = RORn(S, 15)
    # wykonanie SMIX
    S = SMIX(S)
    S[:, 4] = S[:, 4] ^ S[:, 0]
    S[:, 16] = S[:, 16] ^ S[:, 0]
    # wykoanie ROR14
    S = RORn(S, 14)
    # wykonanie SMIX
    S = SMIX(S)
# S_4 += S_0
S[:, 4] = S[:, 4] ^ S[:, 0]
# S_15 += S_0
S[:, 15] = S[:, 15] ^ S[:, 0]

#print("Macierz S po The Final Round G")
#print(S)

# tworzenie ostatecznego skrotu
skrot = Tworzenie_Skrotu(S)
print("\nSkrot: ", hex(skrot)[2:])   

# generowanie skrotow o okreslonej dlugosci
skrot = Skrot_Dlugosc(skrot, dlugosc_skrotu, w_skracania)
print("Skrot: ", hex(skrot)[2:])

# zapis skrotu do pliku
ZapisDoPliku(hex(skrot)[2:])