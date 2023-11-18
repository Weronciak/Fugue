import math
import numpy as np

#padding 
# bierze wartosc wejsciowa X o wartosci n bitow
# nastepnie jesli n nie jest wielokrotnoscia 32 to uzupelnia zerami tak aby otrzymac wielokrotnosc 32 bitow (4 bajtow)
# jesli n mod(32) = 0 to nie uzupelniamy zerami
# X' = X_1 - sekwencja po m bajtow, gdzie m - wielokrotnosc 4
# X_1 - wartosc wejsciowa + zera
# X_1 zamieniamy na reprezentacje m bajtowa
# nastepnie dlugosc n przedstawiamy w reprezentacji jako osmiobajtowa liczba calkowita (big-endian)
# X_2 to X_1 + osmiobajtowa reprezentacja n

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

"""
print(b_s_len_int)
print(bin(b_s_len_int)[2:])
b_s_len_bin = bin(b_s_len_int)[2:]
b_s_len_bin = b_s_len_bin.zfill(64)
print(b_s_len_bin)

X_2 = X_1_bin + b_s_len_bin
print(X_2)
X_2_int = int(X_2,2)
print(X_2_int)
"""

"""
# podzial otrzymanej wartosci po 4 bajty
# bedzie to wykorzystywane w pozostalych funcjach 
X_2_koncowa = []
for i in range(0, len(bin(X_2)[2:]), 8):
    X_2_koncowa.append(X_2[i: i + 8])
print(X_2_koncowa)
"""

"""
# S-box to tablica sluzaca do nieliniowej permutacji bajtow
# S-box piwinien byc wymiaru FxF, ale u mnie bedzie 15x15 bo nie zrobie s_box[F]
s_box = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'], 
         ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
         ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
         ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
         ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
         ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
         ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
         ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
         ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
         ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
         ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
         ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
         ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
         ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
         ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
         ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]

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

"""
s_box = [[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118], 
         [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
         [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
         [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
         [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
         [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
         [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
         [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
         [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
         [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
         [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
         [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
         [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
         [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
         [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
         [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]]


"""
# wektor inicjalizujacy vector_IV to macierz
vector_IV = np.matrix([
                       ['e9', '66', 'e0', 'd2', 'f9', 'fb', '91', '34'], 
                       ['52', '71', 'd4', 'b0', '6c', 'f9', '49', 'f8'], 
                       ['bd', '13', 'f6', 'b5', '62', '29', 'e8', 'c2'], 
                       ['de', '5f', '68', '94', '1d', 'de', '99', '48']
                       ])
"""
vector_IV = np.matrix([
                       [233, 102, 224, 210, 249, 251, 145, 52], 
                       [82, 113, 212, 176, 108, 249, 73, 248], 
                       [189, 19, 246, 181, 98, 41, 232, 194], 
                       [222, 95, 104, 148, 29, 222, 153, 72]
                       ])

"""
# zamiana string na int i dzialanie xor na tych wartosciach
z = int(vector_IV[0,0],16)
print(z)
print(type(z))
z_1 =int(vector_IV[0,1], 16)
w = z ^ z_1
print(w)
"""
"""
vector_IV = np.matrix([[0xe9, 0x66, 0xe0, 0xd2, 0xf9, 0xfb, 0x91, 0x34], 
                       [0x52, 0x71, 0xd4, 0xb0, 0x6c, 0xf9, 0x49, 0xf8], 
                       [0xbd, 0x13, 0xf6, 0xb5, 0x62, 0x29, 0xe8, 0xc2], 
                       [0xde, 0x5f, 0x68, 0x94, 0x1d, 0xde, 0x99, 0x48]])
print(vector_IV)
"""
# parametry:
# s - rozmiar stanu, liczba 4 bajtowych kolumn 
s = 30
# n - rozmiar wyjscia
n = 8
# k - liczba pod-rund na jedna runde
k = 2
# r - liczba rund w pierwszej fazie koncowej transformacji G
r = 5
# t - liczba rund w drugiej fazie koncowej transformacji G
t = 13

# Inicjalize State
# for j in range(0, s - 1 - n):
# S[:,j] = 0
# for j in range(0, n-1):
# S[:, s-n+j] = IV[:,j]
# zamiast wykonac for powyzej stworzylam macierz zerowa 4x30 
# i ostatnie kolumny zamieniam na wektor inicjalizujacy
S = np.zeros((4, 30), dtype = int)
for j in range(0, n):
    S[:, (s - n + j)]= vector_IV[:, j].flatten()
print(S)


# TIX[s,k](P)
for j in range(0, len(X_2_koncowa)):
    # tworze wektor 4 bajtowy 
    # biore wartosc zmiennej i przesuwam o podana ilosc bitow za pomoca >> w prawo a nastepnie biore otatnie (najmlodsze) 8 bitow
    P = [(X_2_koncowa[j] >> 24) & 0xff, (X_2_koncowa[j] >> 16) & 0xff ,(X_2_koncowa[j] >> 8) & 0xff, X_2_koncowa[j] & 0xff]
    # S_6k-2 += S_0
    S[:, 6*k - 2] = S[:, 6*k - 2] ^ S[:, 0]
    # S_0 = P
    S[:, 0] = P
    # S_8 += S_0
    S[:, 8] = S[:, 8] ^ S[:, 0]
    for i in range(0, k-1):
        # S_3i+1 += S_s-3k+3i
        S[:, 3*i + 1] = S[:, 3*i + 1] ^ S[:, s - 3*k + 3*i]
print(S)

# ROR3
# rotacja kolumn macierzy S w prawo o 3 kolumny
# trzeba zrobic kopie macierzy S, 
# poniewaz temp = S powoduje ze do zmiennej temp oraz S przypisana jest ta sama macierz
temp = S.copy()
for i in range(0, s):
    # indeks kolumny, modulo 30 zeby uniknac ujemnych wartosci
    j = (i - 3) % 30
    S[:, i] = temp[:, j]
print(S)

# CMIX[s]
# mieszanie kolumn
# S_0 += S_4
S[:, 0] = S[:, 0] ^ S[:, 4]
# S_s/2 += S_4
S[:, (s//2)] = S[:, (s//2)] ^ S[:, 4]
# S_1 += S_5
S[:, 1] = S[:, 1] ^ S[:, 5]
# S_s/2+1 += S_5
S[:, (s//2 + 1)] = S[:, (s//2 + 1)] ^ S[:, 5]
# S_2 += S_s_6
S[:, 2] = S[:, 2] ^ S[:, 6]
# S_s/2+2 += S_6
S[:, (s//2 + 2)] = S[:, (s//2 + 2)] ^ S[:, 6]
print(S)

"""
# Inicjalize State
# for j in range(0, 22):
# S[:,j] = 0
# for j in range(0, 8):
# S[:, 22 + j] = IV[:,j]
# zamiast wykonac for powyzej stworzylam macierz int zerowa 4x30 
# i ostatnie kolumny zamieniam na wektor inicjalizujacy
S = np.zeros((4, 30), dtype = int)
for j in range(0, 8):
    S[:, 22 + j] = vector_IV[:, j].flatten()
print(S)

# TIX(P_i)
# dla kazdego elementu P_i ktory jest elementem z x_2_koncowa
def TIX(P_i, S):
    # tworze wektor 4 bajtowy  P
    # biore wartosc zmiennej i przesuwam o podana ilosc bitow za pomoca >> w prawo a nastepnie biore otatnie (najmlodsze) 8 bitow
    vector_P = [(P_i >> 24) & 0xff, (P_i >> 16) & 0xff ,(P_i >> 8) & 0xff, P_i & 0xff]
    print("przed", S)
    # S_10 += S_0
    S[:, 10] = S[:, 10] ^ S[:, 0]
    # S_0 = I
    S[:, 0] = vector_P
    # S_8 += S_0
    S[:, 8] = S[:, 8] ^ S[:, 0]
    # S_1 += S_24
    S[:, 1] = S[:, 1] ^ S[:, 24]
    return S

for i in range(0, len(X_2_koncowa)):
    S = TIX(X_2_koncowa[i], S)
print("po tix", S)

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

S = RORn(S, 3)
print("R", S)

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
S = CMIX(S)
print("C", S)

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

S = S_BOX(s_box, S)
print("S-box", S)