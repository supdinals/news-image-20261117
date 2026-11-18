# EVAL — Fase D: evaluasi ala juri (news-image-20261117)

Metode: ketiga varian dilihat pada ukuran penuh (1024px) dan versi kecil 512px.
Setiap pasangan dibandingkan dengan pertanyaan brief — *"gambar mana yang paling
merangkum berita dunia 17 Nov 2026 bagi editor foto yang teliti?"* — dengan urutan
penyajian ditukar, 3 ronde per pasangan (6 penilaian per pasangan), memakai urutan
kriteria RULES: menyebut hari + peristiwa spesifik; pilihan/luas cakupan wilayah &
bidang; terbaca jelas dari gambar saja; setia pada fakta; craft & keterbacaan di
ukuran kecil. Ketiga varian memuat 6 berita yang sama dari SOURCES.md, jadi
penilaian bertumpu pada kelengkapan detail, keterbacaan, dan craft.

## Hasil berpasangan

| Pasangan | Skor | Catatan penentu |
|---|---|---|
| A vs B | **A 6–0** | Ubin A lebih cepat dipindai; kolom B padat (headline campak 4 baris), ~15% kanvas kosong di bawah, gelombang ikon B menimpa garis di bawah lead. Headline B "IRAN DRONES TARGET…" juga lebih lemah secara faktual daripada "FIRES DRONES AT…". B unggul hanya di detail COP ($120bn). |
| A vs C | **C 5–1** | Lead C jauh lebih besar (58px vs 44px), daftar bernomor terbaca satu arah, ikon per berita membantu ingatan, pita tanggal paling mencolok, tak ada ruang mati. A menang 1 penilaian: sub ubinnya sedikit lebih lengkap per berita. |
| B vs C | **C 6–0** | C lebih rapat dan terbaca di 512px; B kalah di ruang kosong + ikon menimpa garis. |

**Total kemenangan: C 11, A 7, B 0 (dari 12 penilaian per varian). Pemenang: Varian C**
(lead besar + daftar bernomor).

## Kelemahan per varian

- **A (grid ubin):** lead hanya 44px; sub lead paling pendek (kehilangan "Kremlin
  vows to rebuild"); ubin COP kehilangan angka $120bn; ada ruang mati di dasar ubin;
  pola baca zig-zag. (Dua cacat render awal — ikon menimpa teks sub lead dan sub
  ubin Sudan — sudah diperbaiki sebelum evaluasi final.)
- **B (halaman depan koran):** ruang kosong besar di paruh bawah; gelombang ikon
  jembatan menimpa garis horizontal di bawah lead; headline kolom sempit berliku
  sampai 4 baris; sub kolom paling pendek.
- **C (pemenang, sebelum perbaikan):** (1) sub daftar kehilangan atribusi konteks —
  Sudan tanpa "UN report", Iran hanya "no damage"; (2) ikon jembatan terbaca seperti
  dua huruf "A" karena kabel hanya menyebar ke luar.

## Perbaikan pada pemenang (sudah diterapkan & dirender ulang)

1. Sub Iran → "Intercepted — no casualties or damage. Tanker attacks rise."
2. Sub Sudan → "UN report, Jan–Oct: 1,630+ killed by drones; toll likely higher."
3. Ikon jembatan digambar ulang sebagai jembatan cable-stayed: kipas kabel dari
   kedua tiang ke dek, bentang tengah putus, segmen jatuh miring di air, gelombang.
   (Ikon radar dan daun juga digambar ulang di semua varian: radar tanpa drone mini
   yang membingungkan; daun bezier menggantikan lingkaran-garis yang terbaca seperti
   tanda larangan.)

## Penetapan

Varian C final disalin menjadi `entry.png` di root repo:
1024×1024 PNG, 126.789 byte (≤ 1 MiB). Semua teks Inggris gaya headline, tanggal
"TUESDAY 17 NOVEMBER 2026" pada pita emas di atas, 6 blok berita, tanpa foto/logo/
wajah/kekerasan eksplisit, tanpa teks tersembunyi.
