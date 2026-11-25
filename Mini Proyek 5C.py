import csv
import os

FILE_DATA = "pengaduan_jatim_60_baris.csv"
FILE_USER = "users.csv"
STATUS = ["belum_terverifikasi", "belum_ditindaklanjuti", "proses",
          "selesai", "tunda", "arsip"]
KOLOM = ["id", "kabupaten_kota"] + STATUS + ["jumlah_pengaduan", "kode_provinsi",
                                             "nama_provinsi", "satuan", "periode_update"]
SARAN = {
    "belum_ditindaklanjuti": "Tugaskan petugas untuk segera menangani laporan.",
    "belum_terverifikasi": "Segera lakukan verifikasi laporan.",
    "tunda": "Periksa penyebab penundaan dan tentukan langkah penyelesaian.",
    "proses": "Pantau perkembangan dan lakukan koordinasi.",
}


def baca_user():
    users = {"admin": "admin123"}
    if os.path.exists(FILE_USER):
        with open(FILE_USER, encoding="utf-8") as f:
            for baris in csv.reader(f):
                if len(baris) == 2:
                    users[baris[0]] = baris[1]
    return users

def simpan_user(users):
    with open(FILE_USER, "w", newline="", encoding="utf-8") as f:
        tulis = csv.writer(f)
        for nama in users:
            tulis.writerow([nama, users[nama]])


def login(users):
    for sisa in range(3, 0, -1):
        nama = input("Username: ").strip()
        sandi = input("Password: ").strip()
        if nama in users and users[nama] == sandi:
            return nama
        print("Username/password salah. Sisa percobaan:", sisa - 1)
    return None


def baca_data():
    data = []
    if not os.path.exists(FILE_DATA):
        return data
    with open(FILE_DATA, encoding="utf-8-sig") as f:
        for baris in csv.DictReader(f):
            try:
                baris["id"] = int(float(baris["id"]))
                baris["total"] = 0
                for k in STATUS:
                    baris[k] = int(float(baris[k]))
                    baris["total"] += baris[k]
                data.append(baris)
            except ValueError:
                pass
    return data


def simpan_data(data):
    with open(FILE_DATA, "w", newline="", encoding="utf-8") as f:
        tulis = csv.DictWriter(f, fieldnames=KOLOM, extrasaction="ignore")
        tulis.writeheader()
        for b in data:
            tulis.writerow(b)


def tambah_data(data):
    wilayah = input("Kabupaten/Kota: ").strip().upper()
    periode = input("Periode (contoh JUNI 2026): ").strip().upper()
    if wilayah == "" or periode == "":
        print("Wilayah dan periode tidak boleh kosong.")
        return
    baru = {"id": len(data) + 1, "kabupaten_kota": wilayah, "periode_update": periode,
            "kode_provinsi": 35, "nama_provinsi": "JAWA TIMUR", "satuan": "Pengaduan",
            "total": 0}
    for k in STATUS:
        isi = input(k.replace("_", " ").title() + ": ").strip()
        while not isi.isdigit():
            isi = input("Harus angka bulat, ulangi: ").strip()
        baru[k] = int(isi)
        baru["total"] += baru[k]
    baru["jumlah_pengaduan"] = baru["total"]
    data.append(baru)
    simpan_data(data)
    print("Data berhasil disimpan.")


def tampil(data):
    print("\n" + "=" * 180)

    print(f"{'No':<4}{'Wilayah':<18}{'Periode':<17}"
          f"{'BlmVer':>8}{'BlmTL':>8}{'Proses':>8}"
          f"{'Selesai':>8}{'Tunda':>8}{'Arsip':>8}"
          f"{'Total':>8}{'Tindak Lanjut':>17}{'Rekomendasi':<65}")

    print("=" * 180)

    for no, b in enumerate(data, start=1):

        if b["belum_ditindaklanjuti"] > 0:
            tindak = "YA"
            utama = "belum_ditindaklanjuti"

            for k in ["belum_terverifikasi", "tunda", "proses"]:
                if b[k] > b[utama]:
                    utama = k

            rekomendasi = SARAN[utama]
        else:
            tindak = "TIDAK"
            rekomendasi = "Tidak perlu tindak lanjut."

        print(f"{no:<4}{b['kabupaten_kota']:<18}"
              f"{b['periode_update']:<17}"
              f"{b['belum_terverifikasi']:>8}"
              f"{b['belum_ditindaklanjuti']:>8}"
              f"{b['proses']:>8}"
              f"{b['selesai']:>8}"
              f"{b['tunda']:>8}"
              f"{b['arsip']:>8}"
              f"{b['total']:>8}"
              f"{tindak:>17}"
              f"{rekomendasi:<65}")

        print("-" * 180)


def cari(data):
    kata = input("Nama wilayah yang dicari: ").strip().upper()
    hasil = []
    for b in data:
        if kata in b["kabupaten_kota"].upper():
            hasil.append(b)
    if len(hasil) == 0:
        print("Data tidak ditemukan.")
    else:
        tampil(hasil)

def ringkasan(data):
    jumlah = {}
    total = 0
    for k in STATUS:
        jumlah[k] = 0
        for b in data:
            jumlah[k] += b[k]
        total += jumlah[k]
    print("\n=== JUMLAH PER STATUS ===")
    for k in STATUS:
        persen = jumlah[k] / total * 100 if total > 0 else 0
        print(k.replace("_", " ").title(), ":", jumlah[k], "(", format(persen, ".1f"), "%)")
    print("TOTAL :", total)

    aktif = total - jumlah["arsip"]
    persen = jumlah["selesai"] / aktif * 100 if aktif > 0 else 0
    if persen >= 80:
        kategori = "Baik"
    elif persen >= 60:
        kategori = "Cukup"
    else:
        kategori = "Perlu Perhatian"
    print("\n=== EVALUASI ===")
    print("Selesai:", format(persen, ".1f"), "% dari pengaduan aktif ->", kategori)


def tindak_lanjut(data):
    hasil = []

    for b in data:
        if b["belum_ditindaklanjuti"] > 0:
            hasil.append(b)

    print("\n=== PERLU TINDAK LANJUT ===")

    if len(hasil) == 0:
        print("Semua pengaduan sudah ditindaklanjuti.")
    else:
        tampil(hasil)

def menu_utama(nama, data):
    pilih = ""
    while pilih != "0":
        print("\n===== EVALUASI PENGADUAN - JATIM (user:", nama, ") =====")
        print("1. Tambah data pengaduan")
        print("2. Tampilkan semua data")
        print("3. Cari data per wilayah")
        print("4. Ringkasan status + evaluasi")
        print("5. Perlu tindak lanjut + rekomendasi")
        print("0. Logout")
        pilih = input("Pilih menu: ").strip()
        if pilih == "1":
            tambah_data(data)
        elif pilih == "2":
            tampil(data)
        elif pilih == "3":
            cari(data)
        elif pilih == "4":
            ringkasan(data)
        elif pilih == "5":
            tindak_lanjut(data)
        elif pilih != "0":
            print("Pilihan tidak valid.")

users = baca_user()
data = baca_data()