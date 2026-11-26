judul_1 = "Evaluasi Penanganan Pengaduan Masyarakat"
judul_2 = "Berdasarkan Status Penyelesaian, Kategori, Wilayah, dan Periode Laporan"
kelompok = "Kelompok 5C"
asisten = "Badra Allam Zonta"
dosen = "(Asmuliardi Muluk, S.T., M.T.)"
tahun = "2026"

LEBAR = 90  


def baris(teks=""):
   
    print("|" + teks.center(LEBAR) + "|")


print("+" + "-" * LEBAR + "+")   

baris()
baris()
baris()


baris("MINI PROJECT")
baris()
baris("PEMROGRAMAN KOMPUTER")
baris()
baris("(" + judul_1 + ")")
baris(judul_2 + ")")
baris()
baris()

# ---------- Kelompok ----------
baris("Oleh :")
baris()
baris(kelompok)
baris()
baris()

# ---------- Anggota ----------
baris("Anggota :")
baris()
baris("Anisa Syalsabila                2610931007")
baris("Arya Rahmat Syafendra           2610932006")
baris("Varid Febrian                   2610932018")
baris("Talitha Nava Libna Cahyadi      2610933044")
baris()
baris()
baris()

# ---------- Asisten ----------
baris("Asisten Pembimbing :")
baris()
baris(asisten)
baris()
baris()
baris()

# ---------- Dosen ----------
baris("Dosen Pengampu :")
baris()
baris(dosen)
baris()
baris()
baris()
baris()

# ---------- Institusi ----------
baris("LABORATORIUM SISTEM INFORMASI DAN KEPUTUSAN")
baris()
baris("DEPARTEMEN TEKNIK INDUSTRI")
baris()
baris("FAKULTAS TEKNIK")
baris()
baris("UNIVERSITAS ANDALAS")
baris()
baris(tahun)

baris()
baris()
baris()

print("+" + "-" * LEBAR + "+")  
import csv
import os

FILE_DATA = "pengaduan_jatim_60_baris.csv"
FILE_USER = "users.csv"

STATUS = [
    "belum_terverifikasi",
    "belum_ditindaklanjuti",
    "proses",
    "selesai",
    "tunda",
    "arsip",
]

KOLOM = ["id", "kabupaten_kota",] + STATUS + [""
    "jumlah_pengaduan",
    "kode_provinsi",
    "nama_provinsi",
    "satuan",
    "periode_update",
]

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
            print("Login berhasil.")
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

            except (ValueError, KeyError, TypeError):
                pass
    return data


def simpan_data(data):
    with open(FILE_DATA, "w", newline="", encoding="utf-8") as f:
        tulis = csv.DictWriter(
            f,
            fieldnames=KOLOM,
            extrasaction="ignore")

        tulis.writeheader()

        for b in data:
            tulis.writerow(b)


def tambah_data(data):
    wilayah = input("Kabupaten/Kota: ").strip().upper()
    periode = input("Periode (contoh JUNI 2026): ").strip().upper()

    if wilayah == "" or periode == "":
        print("Wilayah dan periode tidak boleh kosong.")
        return

    baru = {
        "id": len(data) + 1,
        "kabupaten_kota": wilayah,
        "periode_update": periode,
        "kode_provinsi": 35,
        "nama_provinsi": "JAWA TIMUR",
        "satuan": "Pengaduan",
        "total": 0,
    }

    for k in STATUS:
        isi = input(
            k.replace("_", " ").title() + ": "
        ).strip()

        while not isi.isdigit():
            isi = input("Harus angka bulat, ulangi: ").strip()

        baru[k] = int(isi)
        baru["total"] += baru[k]

    baru["jumlah_pengaduan"] = baru["total"]

    data.append(baru)
    simpan_data(data)

    print("Data berhasil disimpan.")


def info_tindak_lanjut(b):
    status_aktif = [
        "belum_ditindaklanjuti",
        "belum_terverifikasi",
        "tunda",
        "proses",
    ]

    utama = max(status_aktif, key=lambda k: b[k])

    if b[utama] > 0:
        return "Perlu TL", SARAN[utama]

    return "Aman", "-"


def tampil(data):
    lebar_rekom = 66
    lebar_total = 98 + lebar_rekom

    garis_atas_bawah = "=" * lebar_total
    garis_header = "-" * lebar_total

    print()
    print(garis_atas_bawah)

    print(
        f"{'No':<4} | {'Wilayah':<12} | {'Periode':<15} | "
        f"{'BlmVer':>6} | {'BlmTL':>5} | {'Proses':>6} | "
        f"{'Selesai':>7} | {'Tunda':>5} | {'Arsip':>5} | "
        f"{'Total':>5} | {'Tindak Lanjut':<13} | "
        f"{'Rekomendasi':<{lebar_rekom}}"
    )

    print(garis_header)

    no = 1

    for b in data:
        status_tl, rekomendasi = info_tindak_lanjut(b)

        print(
            f"{no:<4} | {b['kabupaten_kota']:<12} | "
            f"{b['periode_update']:<15} | "
            f"{b['belum_terverifikasi']:>6} | "
            f"{b['belum_ditindaklanjuti']:>5} | "
            f"{b['proses']:>6} | "
            f"{b['selesai']:>7} | "
            f"{b['tunda']:>5} | "
            f"{b['arsip']:>5} | "
            f"{b['total']:>5} | "
            f"{status_tl:<13} | "
            f"{rekomendasi:<{lebar_rekom}}"
        )

        no += 1

    print(garis_atas_bawah)


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

        print(
            k.replace("_", " ").title(),
            ":",
            jumlah[k],
            "(",
            format(persen, ".1f"),
            "%)",
        )

    print("TOTAL :", total)

    aktif = total - jumlah["arsip"]
    persen = (jumlah["selesai"] / aktif * 100 
              if aktif > 0 else 0)

    if persen >= 80:
        kategori = "Baik"
    elif persen >= 60:
        kategori = "Cukup"
    else:
        kategori = "Perlu Perhatian"

    print("\n=== EVALUASI ===")

    print(
        "Selesai:",
        format(persen, ".1f"),
        "% dari pengaduan aktif ->",
        kategori
    )


def analisis_pareto(data):
    wilayah = {}

    for b in data:
        nama = b["kabupaten_kota"]

        belum_selesai = (
            b["belum_terverifikasi"]
            + b["belum_ditindaklanjuti"]
            + b["proses"]
            + b["tunda"]
        )

        if nama not in wilayah:
            wilayah[nama] = 0

        wilayah[nama] += belum_selesai

    hasil = sorted(
        wilayah.items(),
        key=lambda x: x[1],
        reverse=True
    )

    total = sum(wilayah.values())

    if total == 0:
        print("Tidak ada pengaduan yang perlu ditindaklanjuti.")
        return

    print("\n========== ANALISIS PARETO PENGADUAN ==========")
    print("Total pengaduan belum selesai:", total)
    print("-" * 85)

    print(
        f"{'Wilayah':<22} | {'Jumlah':>8} | "
        f"{'Persentase':>11} | {'Kumulatif':>11} | "
        f"{'Keterangan'}"
    )

    print("-" * 85)

    kumulatif = 0
    prioritas = []

    for nama, jumlah in hasil:
        persen = jumlah / total * 100
        kumulatif_sebelumnya = kumulatif

        kumulatif += persen

        if kumulatif_sebelumnya < 80:
            keterangan = "PRIORITAS"
            prioritas.append(nama)
        else:
            keterangan = "-"

        print(
            f"{nama:<22} | {jumlah:>8} | "
            f"{persen:>10.2f}% | {kumulatif:>10.2f}% | "
            f"{keterangan}"
        )

    print("-" * 85)
    print("\n========== HASIL ANALISIS ==========")
    print("Wilayah yang menjadi prioritas penanganan:")

    for nama in prioritas:
        print("-", nama)

    print(
        "\nWilayah prioritas merupakan wilayah yang secara "
        "kumulatif menyumbang hingga ambang 80% "
        "pengaduan belum selesai."
    )


def menu_utama(nama, data):
    pilih = ""

    while pilih != "0":
        print("\n===== EVALUASI PENGADUAN - JATIM " "(user:", nama, ") =====")

        print("1. Tambah data pengaduan")
        print("2. Tampilkan semua data")
        print("3. Cari data per wilayah")
        print("4. Ringkasan status + evaluasi")
        print("5. Analisis Pareto wilayah")
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
            analisis_pareto(data)
        elif pilih != "0":
            print("Pilihan tidak valid.")

users = baca_user()
data = baca_data()

pilih = ""

while pilih != "0":
    print("\n===== SELAMAT DATANG =====")
    print("1. Login")
    print("2. Registrasi")
    print("0. Keluar")

    pilih = input("Pilih: ").strip()

    if pilih == "1":
        nama = login(users)

        if nama is None:
            print("Gagal login 3 kali.")
        else:
            menu_utama(nama, data)

    elif pilih == "2":
        nama = input("Username baru: ").strip()
        sandi = input("Password (min 4 karakter): ").strip()

        if nama == "" or nama in users or len(sandi) < 4:
            print(
                "Gagal: username kosong/sudah dipakai "
                "atau password terlalu pendek."
            )

        else:
            users[nama] = sandi
            simpan_user(users)

            print("Registrasi berhasil, silakan login.")

    elif pilih != "0":
        print("Pilihan tidak valid.")

print("Program selesai. Terima kasih.")