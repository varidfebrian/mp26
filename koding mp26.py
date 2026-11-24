import csv

nama_file = "pengaduan_jatim_60_baris.csv"

STATUS = ["belum_terverifikasi", "belum_ditindaklanjuti", "proses",
          "selesai", "tunda", "arsip"]
ANGKA = ["id"] + STATUS + ["jumlah_pengaduan", "kode_provinsi"]
WAJIB = ["id", "kabupaten_kota"] + STATUS + ["jumlah_pengaduan", "kode_provinsi",
                                             "nama_provinsi", "satuan", "periode_update"]

SARAN = {
    "belum_ditindaklanjuti": "Tugaskan petugas untuk segera memeriksa dan menangani laporan.",
    "belum_terverifikasi": "Segera lakukan pemeriksaan dan verifikasi laporan.",
    "tunda": "Periksa penyebab penundaan dan tentukan langkah penyelesaian.",
    "proses": "Pantau perkembangan dan lakukan koordinasi.",
}


def baca_data():
    data = []
    tidak_valid = []
    beda = 0
    with open(nama_file, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for kolom in WAJIB:
            if reader.fieldnames is None or kolom not in reader.fieldnames:
                return None, None, None
        nomor = 1
        for baris in reader:
            nomor += 1
            alasan = ""
            for kolom in WAJIB:
                if baris[kolom] is None or baris[kolom].strip() == "":
                    alasan = kolom + " kosong"
            if alasan == "":
                try:
                    for kolom in ANGKA:
                        angka = float(baris[kolom])
                        if angka < 0 or angka != int(angka):
                            alasan = kolom + " negatif / bukan bilangan bulat"
                        baris[kolom] = int(angka)
                except ValueError:
                    alasan = "Format angka tidak valid"
            if alasan != "":
                tidak_valid.append([nomor, alasan])
                continue
            baris["total"] = 0
            for kolom in STATUS:
                baris["total"] += baris[kolom]
            if baris["total"] != baris["jumlah_pengaduan"]:
                beda += 1
            data.append(baris)
    return data, tidak_valid, beda


def hitung_status(data):
    hasil = {}
    for kolom in STATUS:
        hasil[kolom] = 0
        for baris in data:
            hasil[kolom] += baris[kolom]
    return hasil


def ambil_total(baris):
    return baris["total"]


def ambil_belum_tl(baris):
    return baris["belum_ditindaklanjuti"]


def tampil_semua(data):
    print(f"{'No':<4}{'Wilayah':<22}{'Periode':<13}{'BlmVer':>7}{'BlmTL':>7}"
          f"{'Proses':>7}{'Selesai':>8}{'Tunda':>7}{'Arsip':>7}{'Total':>7}")
    print("-" * 89)
    no = 1
    for b in data:
        print(f"{no:<4}{b['kabupaten_kota']:<22}{b['periode_update']:<13}"
              f"{b['belum_terverifikasi']:>7}{b['belum_ditindaklanjuti']:>7}"
              f"{b['proses']:>7}{b['selesai']:>8}{b['tunda']:>7}"
              f"{b['arsip']:>7}{b['total']:>7}")
        no += 1
    print("Keterangan: BlmVer = belum terverifikasi, BlmTL = belum ditindaklanjuti")


def tampil_status(data):
    hasil = hitung_status(data)
    total = sum(hasil.values())
    print("=== JUMLAH PENGADUAN PER STATUS ===")
    for kolom in STATUS:
        persen = hasil[kolom] / total * 100 if total > 0 else 0
        print(kolom.replace("_", " ").title(), ":", hasil[kolom], "(", format(persen, ".1f"), "%)")
    print("TOTAL :", total)


def tindak_lanjut(data):
    daftar = []
    for b in data:
        if b["belum_ditindaklanjuti"] > 0:
            daftar.append(b)
    daftar.sort(key=ambil_belum_tl, reverse=True)
    print("=== PENGADUAN PERLU TINDAK LANJUT ===")
    if len(daftar) == 0:
        print("Tidak ada pengaduan yang belum ditindaklanjuti.")
    for b in daftar:
        utama = "belum_ditindaklanjuti"
        for k in ["belum_terverifikasi", "tunda", "proses"]:
            if b[k] > b[utama]:
                utama = k
        print("\nWilayah:", b["kabupaten_kota"], "(", b["periode_update"], ")")
        print("Belum ditindaklanjuti:", b["belum_ditindaklanjuti"])
        print("Rekomendasi:", SARAN[utama])


def evaluasi(data):
    hasil = hitung_status(data)
    aktif = sum(hasil.values()) - hasil["arsip"]
    persen = hasil["selesai"] / aktif * 100 if aktif > 0 else 0
    if persen >= 80:
        kategori = "Baik"
    elif persen >= 60:
        kategori = "Cukup"
    else:
        kategori = "Perlu Perhatian"
    print("=== RINGKASAN EVALUASI ===")
    print("Selesai       :", hasil["selesai"], "(", format(persen, ".1f"), "% dari pengaduan aktif )")
    print("Belum selesai :", aktif - hasil["selesai"])
    print("Diarsipkan    :", hasil["arsip"])
    print("Kategori      :", kategori, "(Baik >= 80%, Cukup >= 60%)")


# ===== PROGRAM UTAMA =====
try:
    data, tidak_valid, beda = baca_data()
except FileNotFoundError:
    print("ERROR: File CSV tidak ditemukan:", nama_file)
    data = None

if data is None:
    print("Program berhenti karena data tidak dapat dibaca.")
elif len(data) == 0:
    print("Tidak ada data valid untuk dianalisis.")
else:
    pilih = ""
    while pilih != "0":
        print("\n===== EVALUASI PENGADUAN - JAWA TIMUR =====")
        print("1. Hasil validasi data")
        print("2. Tampilkan semua data")
        print("3. Jumlah per status")
        print("4. Wilayah terbanyak")
        print("5. Perlu tindak lanjut + rekomendasi")
        print("6. Ringkasan evaluasi")
        print("0. Keluar")
        pilih = input("Pilih menu: ").strip()
        print()

        if pilih == "1":
            print("Total data dibaca      :", len(data) + len(tidak_valid))
            print("Data valid             :", len(data))
            print("Data tidak valid       :", len(tidak_valid))
            print("Ketidaksesuaian jumlah :", beda)
            for item in tidak_valid:
                print("Baris", item[0], ":", item[1])
        elif pilih == "2":
            tampil_semua(data)
        elif pilih == "3":
            tampil_status(data)
        elif pilih == "4":
            print("=== 10 WILAYAH DENGAN PENGADUAN TERBANYAK ===")
            for b in sorted(data, key=ambil_total, reverse=True)[:10]:
                print(b["kabupaten_kota"], ":", b["total"])
        elif pilih == "5":
            tindak_lanjut(data)
        elif pilih == "6":
            evaluasi(data)
        elif pilih == "0":
            print("Terima kasih.")
        else:
            print("Pilihan tidak valid.")