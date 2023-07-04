"""
    PROGRAM SIMULASI AGEN PENYEDOT DEBU V.0.0.1
    abdiansah@unsri.ac.id - Agustus 2021
"""
import random
from os import system

from agen import Agen
from lingkungan import Lingkungan

if __name__ == "__main__":
    """ set sistem """
    clear = lambda: system('cls')  # windows ganti dengan 'cls'
    clear()

    """ set lingkungan """
    baris, kolom, sampah = (6, 6, 12)
    lingkungan = Lingkungan(baris, kolom, sampah)

    """ set dan jalankan agen """
    # no_lokasi_agen = 1
    no_lokasi_agen = random.randint(1, baris * kolom) # lokasi agen random, agen malas bisa habis baterai
    agen = Agen(lingkungan, no_lokasi_agen)
    agen.run()