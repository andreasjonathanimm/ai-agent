"""
    PROGRAM SIMULASI AGEN PENYEDOT DEBU V.0.0.1
    abdiansah@unsri.ac.id - Agustus 2021
"""

import sys
import time
import math
from msvcrt import getch
from os import system
# from playsound import playsound


class Agen:
    # LINGKUNGAN
    __lingkungan = None

    # PROPERTY
    __no_lokasi_agen = 1
    __koordinat_lokasi = []
    __isi_baterai = 0
    __jml_langkah = 0
    __KIRI = 'kiri'
    __ATAS = 'atas'
    __KANAN = 'kanan'
    __BAWAH = 'bawah'
    __BERSIHKAN = 'sedot'

    # FUNGSI
    def __init__(self, lingkungan, no_lokasi_agen):
        self.__lingkungan = lingkungan
        self.__no_lokasi_agen = no_lokasi_agen
        for lokasi in self.__lingkungan.get_lokasi():
            self.__koordinat_lokasi.append((lokasi[0], lokasi[1]))

        # (baris * kolom) + (baris - 1) (tambahan jika kena tembok (kanan/kiri!)
        self.__isi_baterai = len(self.__lingkungan.get_lokasi()) + (self.__lingkungan.get_dimensi()[0] - 1)

        print('\nINFORMASI AGEN')
        print(f'- No. lokasi awal Agen\t: L{self.__no_lokasi_agen}')
        print(f'- Koordinat lokasi Agen\t: {self.__get_koordinat_agen(self.__no_lokasi_agen)}')
        status = self.__lingkungan.get_status(self.__no_lokasi_agen)
        # playsound('opening.wav')
        if status == 1:
            print(f'- Status lokasi\t\t: {status} - KOTOR')
            print(f'\t^ Lokasi kotor, lakukan pembersihan...')
            self.__tindakan(self.__BERSIHKAN, no_lokasi_agen)
            # playsound('bersihkan.wav')
            print(f'\t^ Lokasi sudah dibersikan')
        else:
            print(f'- Status lokasi\t\t: {status} - BERSIH')
        print(f'- Isi baterai\t\t: {self.__isi_baterai}')
        print(f'- Jumlah langkah\t: {self.__jml_langkah}')
        if status == 1:
            self.__lingkungan.info_lokasi()

    def __get_koordinat_agen(self, no_lokasi):
        return (self.__lingkungan.get_lokasi()[no_lokasi - 1][0], self.__lingkungan.get_lokasi()[no_lokasi - 1][1])

    def __set_no_lokasi_agen(self, koordinat):
        a, b = koordinat
        i = 0
        for lokasi in self.__lingkungan.get_lokasi():
            if (lokasi[0] == a) and (lokasi[1] == b):
                self.__no_lokasi_agen = i + 1
                break
            i += 1

    def __set_status_bersih(self, no_lokasi_agen):
        self.__lingkungan.get_lokasi()[no_lokasi_agen - 1][2] = 0

    def __cek_baterai(self):
        if self.__isi_baterai != 0:
            self.__isi_baterai -= 1
            self.__jml_langkah += 1
            return True
        else:
            return False

    def __gerakan_legal(self, gerak):
        koordinat_agen = self.__get_koordinat_agen(self.__no_lokasi_agen)
        a, b = koordinat_agen
        if gerak == self.__KIRI:
            b -= 1
        elif gerak == self.__ATAS:
            a -= 1
        elif gerak == self.__KANAN:
            b += 1
        elif gerak == self.__BAWAH:
            a += 1
        else:
            print('\t* Error: Gerakan tidak tersedia!')
        koordinat_agen = (a, b)
        if koordinat_agen in self.__koordinat_lokasi:
            self.__set_no_lokasi_agen(koordinat_agen)
            return True
        else:
            return False

    def __gerakan(self, gerak):
        kode = 0  # baterai habis
        if self.__cek_baterai():
            clear = lambda: system('cls')
            clear()
            print('\nINFORMASI AGEN')
            print(f'- Aksi Agen: Bergerak ke {gerak.upper()}')
            if self.__gerakan_legal(gerak):
                no_lokasi_agen = self.__no_lokasi_agen
                # playsound('mesin.wav')
                print(f'\t* Agen berhasil bergerak...')
                print(f'\t* No. lokasi Agen skg.\t: L{no_lokasi_agen}')
                print(f'\t* Koordinat lokasi Agen\t: {self.__get_koordinat_agen(no_lokasi_agen)}')
                status = self.__lingkungan.get_status(no_lokasi_agen)
                if status == 1:
                    print(f'\t* Status lokasi\t\t: {status} - KOTOR')
                    print(f'\t\t^ Lokasi kotor, lakukan pembersihan...')
                    self.__tindakan(self.__BERSIHKAN, no_lokasi_agen)
                    # playsound('bersihkan.wav')
                    print(f'\t\t^ Lokasi sudah dibersihkan')
                else:
                    print(f'\t* Status lokasi\t\t: {status} - BERSIH')
                print(f'\t* Isi baterai\t\t: {self.__isi_baterai}')
                print(f'\t* Jumlah langkah\t: {self.__jml_langkah}')
                if self.__cek_lokasi_bersih():
                    self.__lingkungan.info_lokasi()
                    print('\n- SELURUH LOKASI TELAH BERSIH DARI KOTORAN :D\n')
                    # playsound('win.wav')
                    sys.exit()
                kode = 1  # berhasil bergerak
            else:
                no_lokasi_agen = self.__no_lokasi_agen
                print(f'\t* Error: Agen tidak bisa bergerak, terhalang tembok!')
                # playsound('crash.wav')
                print(f'\t* No. lokasi Agen\t: L{self.__no_lokasi_agen}')
                print(f'\t* Koordinat lokasi Agen\t: {self.__get_koordinat_agen(self.__no_lokasi_agen)}')
                status = self.__lingkungan.get_status(no_lokasi_agen)
                if status == 1:
                    print(f'\t* Status lokasi\t\t: {status} - KOTOR')
                else:
                    print(f'\t* Status lokasi\t\t: {status} - BERSIH')
                print(f'\t* Isi baterai\t\t: {self.__isi_baterai}')
                print(f'\t* Jumlah langkah\t: {self.__jml_langkah}')
                kode = -1  # terhalang tembok
            self.__lingkungan.info_lokasi()
        else:
            print('\nError: Agen tidak bisa berjalan, kehabisan baterai!!! :(\n')
            # playsound('game-over.wav')
            sys.exit()
        return kode

    def __tindakan(self, aksi, no_lokasi_agen):
        if aksi == self.__BERSIHKAN:
            self.__set_status_bersih(self.__no_lokasi_agen)
        else:
            print('Error: Aksi tidak tersedia!')

    def __cek_lokasi_bersih(self):
        flag = True
        for lokasi in self.__lingkungan.get_lokasi():
            if lokasi[2] == 1:
                flag = False
                break
        return flag

    def __alg_manual(self):
        while (True):
            print('\nINSTRUKSI')
            print('- Gunakan tombol panah KIRI, ATAS, KANAN, dan BAWAH untuk menggerakkan Agen')
            print('- Tekan tombol ESC untuk keluar')
            try:
                # key = input('\nMasukan perintah: ')
                print('\nMasukan perintah: ')
                key = getch()
                if (key == b'\x00' or key == b'\xe0'):
                    key = getch()
                    k = ord(key)
                    if k == 75:
                        self.__gerakan(self.__KIRI)
                    elif k == 72:
                        self.__gerakan(self.__ATAS)
                    elif k == 77:
                        self.__gerakan(self.__KANAN)
                    elif k == 80:
                        self.__gerakan(self.__BAWAH)
                elif ord(key) == 27:
                    print('Bye...')
                    break
                else:
                    print('Tombol yang anda masukan salah!')
            except KeyboardInterrupt:
                print()
                print(':-(')
                break

    def __alg_agen_malas(self):
        """ Agen akan bergerak terus sampai lokasi bersih atau habis baterai """
        arah = 'kanan'  # bagian dari problem formulation
        sec = 3
        time.sleep(5)
        while (True):
            if not self.__cek_lokasi_bersih():
                if arah == 'kanan':
                    if self.__gerakan(self.__KANAN) == -1:  # kena dinding!
                        arah = 'kiri'
                        time.sleep(sec)
                        self.__gerakan(self.__BAWAH)
                        time.sleep(sec)
                    else:
                        time.sleep(sec)
                elif arah == 'kiri':
                    if self.__gerakan(self.__KIRI) == -1:  # kena dinding!
                        arah = 'kanan'
                        time.sleep(sec)
                        self.__gerakan(self.__BAWAH)
                        time.sleep(sec)
                    else:
                        time.sleep(sec)

    def __alg_agen_cerdas(self):
        sec = 3
        time.sleep(5)
        lokasi_kotor = []
        target_terdekat = None
        while (True):
            koordinat_agen = self.__get_koordinat_agen(self.__no_lokasi_agen)
            x, y = koordinat_agen
            jarak_kotor_terdekat = float("inf")
            if not self.__cek_lokasi_bersih():
                for lokasi in self.__lingkungan.get_lokasi():
                    if lokasi[2] == 1:
                        lokasi_kotor.append(lokasi)
                for lk in lokasi_kotor:
                    jarak = math.sqrt((lk[0] - x)**2 + (lk[1] - y)**2)
                    if jarak < jarak_kotor_terdekat:
                        jarak_kotor_terdekat = jarak
                        target_terdekat = lk
                a, b, c = target_terdekat
                if a > x:
                    self.__gerakan(self.__BAWAH)
                    time.sleep(sec)
                elif a < x:
                    self.__gerakan(self.__ATAS)
                    time.sleep(sec)
                elif b > y:
                    self.__gerakan(self.__KANAN)
                    time.sleep(sec)
                elif b < y:
                    self.__gerakan(self.__KIRI)
                    time.sleep(sec)
                for lokasi in lokasi_kotor:
                    if lokasi[2] == 0:
                        lokasi_kotor.remove(lokasi)


    def run(self):
        # self.__alg_manual()
        # self.__alg_agen_malas()
        self.__alg_agen_cerdas()
