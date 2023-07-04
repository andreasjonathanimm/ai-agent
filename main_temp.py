import sys
from os import system
import random

class Lingkungan:

    __lantai = []
    __dimensi = 0

    def __init__(self, baris, kolom, sampah):
        print('\nINFORMASI LINGKUNGAN')
        self.__dimensi = (baris, kolom)
        self.__set_lantai(baris, kolom, sampah)  # baris, kolom, sampah

    def __generate_sampah(self, jml_lantai, jml_sampah):
        if jml_lantai > jml_sampah:
            randomlist = random.sample(range(1, jml_lantai), jml_sampah)
            return randomlist
        else:
            print('- Error: Jumlah sampah tidak boleh lebih banyak dari jumlah lantai!')
            return []

    def __set_lantai(self, baris, kolom, sampah):
        lantai2d = [[0 for i in range(kolom)] for j in range(baris)]
        print(f'- Jumlah baris\t: {baris}')
        print(f'- Jumlah kolom\t: {kolom}')
        print(f'- Jumlah lantai\t: {baris*kolom}')
        print(f'- Jumlah sampah\t: {sampah}')
        lokasi_sampah = self.__generate_sampah((baris*kolom), sampah)
        print(f'- Lokasi sampah\t: {sorted(lokasi_sampah)}')

        no_lantai = 1
        for r in range(len(lantai2d)):
            for c in range(len(lantai2d[r])):
                # lantai2d[r][c] = no_lantai
                if no_lantai in lokasi_sampah:
                    self.__lantai.append([r, c, 1])
                else:
                    self.__lantai.append([r, c, 0])
                no_lantai+=1

        self.info_lantai()

    def info_lantai(self):
        print('\nREPRESENTASI LINGKUNGAN')
        baris, kolom = self.__dimensi
        idx_lantai = 0
        for r in range(baris):
            str = ''
            for c in range(kolom):
                # print(f' {self.__lantai[no_lantai]} ')
                str += f'L{idx_lantai + 1}-{self.__lantai[idx_lantai]} \t'
                idx_lantai += 1
            print(str)

    def get_lantai(self):
        return self.__lantai

    def get_status(self, no_lantai):
        return self.__lantai[no_lantai-1][2]

class Agen:

    # LINGKUNGAN
    __lingkungan = None

    # PROPERTY
    __no_lantai_agen = 1
    __koordinat_lantai = []
    __isi_baterai = 0
    __jml_langkah = 0
    __KIRI = 'kiri'
    __ATAS = 'atas'
    __KANAN = 'kanan'
    __BAWAH = 'bawah'
    __SEDOT = 'sedot'

    # FUNGSI
    def __init__(self, lingkungan, no_lantai_agen):
        self.__lingkungan = lingkungan
        self.__no_lantai_agen = no_lantai_agen
        for lantai in self.__lingkungan.get_lokasi():
            self.__koordinat_lantai.append((lantai[0], lantai[1]))
        self.__isi_baterai = len(self.__lingkungan.get_lokasi())  # maksimal langkah (baterai) = jumlah lantai

        print('\nINFORMASI AGEN')
        print(f'- No. lantai awal Agen\t: L{self.__no_lantai_agen}')
        print(f'- Koordinat lantai Agen\t: {self.__get_koordinat_agen(self.__no_lantai_agen)}')
        status = self.__lingkungan.get_status(self.__no_lantai_agen)
        print(f'- Status lantai Agen\t: {status}')
        if status == 1:
            print(f'\t^ Lantai terdapat sampah, lakukan pembersihan...')
            self.__tindakan(self.__SEDOT, no_lantai_agen)
        print(f'- Isi baterai\t\t: {self.__isi_baterai}')
        print(f'- Jumlah langkah\t: {self.__jml_langkah}')
        if status == 1:
            self.__lingkungan.info_lokasi()

    def __get_koordinat_agen(self, no_lantai):
        return (self.__lingkungan.get_lokasi()[no_lantai - 1][0], self.__lingkungan.get_lokasi()[no_lantai - 1][1])

    def __set_no_lantai_agen(self, koordinat):
        a, b  = koordinat
        i = 0
        for lantai in self.__lingkungan.get_lokasi():
            if (lantai[0] == a) and (lantai[1] == b):
                self.__no_lantai_agen = i+1
                break
            i+=1

    def __set_status_bersih(self, no_lantai_agen):
        self.__lingkungan.get_lokasi()[no_lantai_agen - 1][2] = 0

    def __cek_baterai(self):
        if self.__isi_baterai != 0:
            self.__isi_baterai -= 1
            self.__jml_langkah += 1
            return True
        else:
            print('\nError: Agen tidak bisa berjalan, kehabisan baterai!!! :(\n')
            return False

    def __gerakan_legal(self, gerak):
        koordinat_agen = self.__get_koordinat_agen(self.__no_lantai_agen)
        a, b = koordinat_agen
        if gerak == self.__KIRI:
            b-=1
        elif gerak == self.__ATAS:
            a-=1
        elif gerak == self.__KANAN:
            b+=1
        elif gerak == self.__BAWAH:
            a+=1
        else:
            print('\t* Error: Gerakan tidak tersedia!')
        koordinat_agen = (a, b)
        if koordinat_agen in self.__koordinat_lantai:
            self.__set_no_lantai_agen(koordinat_agen)
            return True
        else:
            return False

    def __gerakan(self, gerak):
        if self.__cek_baterai():
            clear = lambda: system('clear')
            clear()
            print('\nINFORMASI AGEN')
            print(f'- Aksi Agen: Bergerak ke {gerak.upper()}')
            if self.__gerakan_legal(gerak):
                no_lantai_agen = self.__no_lantai_agen
                print(f'\t* Agen berhasil bergerak...')
                print(f'\t* No. lantai Agen skg.\t: L{no_lantai_agen}')
                print(f'\t* Koordinat lantai Agen\t: {self.__get_koordinat_agen(no_lantai_agen)}')
                status = self.__lingkungan.get_status(no_lantai_agen)
                print(f'\t* Status lantai Agen\t: {status}')
                if status == 1:
                    print(f'\t\t^ Lantai terdapat sampah, lakukan pembersihan...')
                    self.__tindakan(self.__SEDOT, no_lantai_agen)
                print(f'\t* Isi baterai\t\t: {self.__isi_baterai}')
                print(f'\t* Jumlah langkah\t: {self.__jml_langkah}')
                if self.__cek_lantai_bersih():
                    print('\n- Lantai telah bersih dari kotoran :D\n')
                    sys.exit()
            else:
                print(f'\t* Error: Agen tidak bisa bergerak, terhalang tembok!')
                print(f'\t* No. lantai Agen\t: L{self.__no_lantai_agen}')
                print(f'\t* Koordinat lantai Agen\t: {self.__get_koordinat_agen(self.__no_lantai_agen)}')
                print(f'\t* Status lantai Agen\t: {self.__lingkungan.get_status(self.__no_lantai_agen)}')
            self.__lingkungan.info_lokasi()
        else:
            sys.exit()

    def __tindakan(self, aksi, no_lantai_agen):
        if aksi == self.__SEDOT:
            self.__set_status_bersih(self.__no_lantai_agen)
        else:
            print('Error: Aksi tidak tersedia!')

    def __cek_lantai_bersih(self):
        flag = True
        for lantai in self.__lingkungan.get_lokasi():
            if lantai[2] == 1:
                flag = False
                break
        return flag

    def run(self):
        while(True):
            print('\nINSTRUKSI')
            print('- Gerakan Agen dengan menggunakan tombol KIRI, ATAS, KANAN, dan BAWAH')
            print('- Tekan tombol ESC untuk keluar')
            key = input('\nMasukan perintah: ')
            if key == '\x1b[D':
                self.__gerakan(self.__KIRI)
            elif key == '\x1b[A':
                self.__gerakan(self.__ATAS)
            elif key == '\x1b[C':
                self.__gerakan(self.__KANAN)
            elif key == '\x1b[B':
                self.__gerakan(self.__BAWAH)
            elif key == chr(27):
                break
            else:
                print('Tombol yang anda masukan salah!')


if __name__ == "__main__":
    clear = lambda: system('clear')
    clear()
    baris, kolom, sampah = (3, 3, 5)
    lingkungan = Lingkungan(baris, kolom, sampah)
    no_lantai_agen = random.randint(1, baris*kolom)
    agen = Agen(lingkungan, no_lantai_agen)
    agen.run()
