# Bukti generalisasi lintas cerita (Phase 4.2)

## 1. Source bersama

| Cerita | Build | `source_hash` di manifest |
|---|---|---|
| Satu Bungkus Lagi | P4-486e18fc49 | `f7ccb35625ca892f68798b6b10541e6810d9a769c139a10ab073e7e045631c8c` |
| Teh Sore untuk Ibu | P4-2d0645d14d | `f7ccb35625ca892f68798b6b10541e6810d9a769c139a10ab073e7e045631c8c` |
| Kopi Sore di Gang | P4-b1767c3b5e | `f7ccb35625ca892f68798b6b10541e6810d9a769c139a10ab073e7e045631c8c` |

- **Cakupan hash:** dihitung dari 40 file (`engine/*.py`, `engine/sets/*.py`, `engine/colab/*.py`, `make.py`). Hash dihitung ulang saat paket dibuat dan cocok dengan ketiga manifest (`15_build_provenance.json` → `verifikasi_paket`). Isi lengkap file ada di `10_source_code.txt`.
- **Tanpa kondisi khusus cerita.** Pencarian `grep` di `engine/` dan `make.py` untuk ID cerita (`benchmark_warung`, `_uji_phase4_rumah`, `uji3_kopi_sore`) dan nama tokoh (darto, jali, sri, dimas, harjo, wulan) hanya menemukan **2 baris komentar**: `blender_build.py:47` dan `kit.py:497`, yang menjelaskan asal temuan kedip. Tidak ada percabangan berdasarkan ID cerita atau nama tokoh.

## 2. Perbedaan konfigurasi cerita (`11_configuration.txt` memuat story.yaml lengkap + diff terhadap 4.1)

| | Benchmark | Generalisasi | Cerita ke-3 (baru) |
|---|---|---|---|
| `latar.lokasi` / waktu | `jalan_kota` / malam, habis hujan | `dalam_rumah` / siang | `gang_kampung` / senja, cerah |
| Properti set | gerobak_makan, motor, meja_lipat, dingklik, aset | kursi, meja ×2, sofa, bufet, karpet, tas_sekolah, tv, pot_tanaman | bangku, meja_lipat, pot_tanaman, sepeda |
| Tokoh (`rupa`) | Darto: sawo, baju putih, celemek, kumis, rambut cepak abu. Jali: langsat, jaket & helm ojol. | Sri: langsat, hijab pink, baju krem. Dimas: sawo, baju kuning, tinggi 1,4 m. | Harjo: kulit gelap, peci, kumis, `umur: tua`, 1,68 m. Wulan: langsat, rambut panjang, 1,58 m. |
| `lakukan` (primitif) | bicara, duduk, makan, masak, melirik, pegang, senyum | ambil, bicara, duduk, minum, serahkan, taruh | ambil, bicara, duduk, hadap, jalan, makan, minum, pegang, senyum, serahkan |
| Shot | 11 | 6 | 7 |
| Parameter kamera deklaratif | `sudut`/`jarak`/`tinggi` di 9 shot (yaw/jarak relatif subjek, bukan posisi manual) | `sudut` di 2 shot | `sudut` di 6 shot |
| Override `komposisi:` | 0 | 0 | 0 |
| Override grading `warna:` per shot | 0 | 0 | 0 |
| Musik | — | `ceria` | `ceria` (awalnya `tenang`, tidak dikenal; dikoreksi) |

## 3. Aset dan modul yang dipakai ulang

- **Set:** `engine/sets/jalan_kota.py`, `dalam_rumah.py` (dibangun ulang di 4.2), `gang_kampung.py` (ada sejak sebelum 4.2; hanya `ujung_gang` digeser 1–2 cm agar tidak sebidang). Semua memakai `engine/sets/kit.py` (gerobak, rumah, meja, kursi, bangku, pot, sepeda, dll.).
- **Tokoh:** satu generator `engine/chars.py` + rig `engine/rig2d.py` / `engine/bl_rig.py`. Tokoh baru hanya **parameter `rupa`** (kulit, peci, kumis, umur, rambut panjang); tidak ada sprite tangan-gambar.
- **Benda dipegang:** profil umum di `engine/grip.py` (sendok, sutil, piring, teh/kopi `kelas: cup`). `kopi` dan `bangku` sudah ada di checkpoint 4.1 (`grip.py`, `bl_rig.py`, `seats.py`).
- **Kamera, jadwal, rencana:** `bl_camsolve.py`, `schedule.py`, `plan.py` sama untuk ketiganya.

## 4. Primitif interaksi yang dipakai ulang

| Primitif | Benchmark | Generalisasi | Cerita ke-3 |
|---|---|---|---|
| Genggam utensil + orientasi anatomis | sutil, sendok | — | sendok |
| Makan (fase eksplisit, kontak cekung–mulut) | Jali (kontak f102–106, 147–151, 192–196, 233–235) | — | Harjo (f85–90) |
| Pegang piring (geser presentasi terbatas) | Jali | — | Harjo |
| Taruh benda (place / release / retract) | sendok f254–278 | teh f549–571 | sendok f118–142 |
| Ambil dari permukaan (reach / grip / lift) | — | teh f119–143 | kopi f150–174 |
| Bawa sambil berjalan | — | Dimas | Wulan |
| Serah-terima sadar-tabrakan | — | f325 (Dimas → Sri, pindah tangan) | f398 (Wulan → Harjo) |
| Minum (fase teguk, bibir gelas–mulut) | — | Sri f483–537 | Harjo f605–676 |
| Duduk (dudukan + celah jejak kotak) | Jali (dingklik) | Sri (kursi) | Harjo (bangku panjang) |

Fase per frame tercatat di `17_interaction_reports/interaksi_*.json` → `fase`, dan ditampilkan sebagai anotasi di `05_interaction_diagnostic_*.mp4`.

## 5. Aset baru yang dibutuhkan cerita ke-3

**Tidak ada aset baru khusus cerita.** Cerita ke-3 memakai set, properti, profil benda, dan parameter tokoh yang sudah ada.

Perubahan engine **yang dipicu** cerita ke-3 bersifat generik dan berlaku untuk semua cerita (§6 laporan penyelesaian). Contohnya:
- `avoid` pada `kit.house`;
- celah duduk untuk bangku panjang;
- pivot betis, yang juga memperbaiki Sri di generalisasi;
- gorden tidak lagi sebidang dengan kaca, yang juga berlaku di rumah latar benchmark.

## 6. Intervensi manual & override khusus cerita

| Cerita | Intervensi (semua di `story.yaml`, tidak di engine) | Alasan |
|---|---|---|
| Cerita ke-3 | Blocking Wulan diulang beberapa kali: jarak serah-terima 0,74 m → ~0,45 m; arah datang diubah; Wulan menghadap meja saat mengambil lalu berbalik (`hadap`) saat berjalan | Rig chibi tidak menjangkau 0,74 m; kamera di tengah gang harus melihat kedua wajah; engine **belum** otomatis menghadap tujuan saat berjalan (lihat daftar belum selesai #7) |
| Cerita ke-3 | `musik.suasana: tenang` → `ceria` | Nilai tidak dikenal mesin audio; validasi engine belum ada (#17) |
| Generalisasi | Titik taruh gelas digeser 14 cm (masih di atas meja) | Jangkauan IK 2D bergantung sudut kamera baru (#10) |
| Ketiga cerita | Tidak ada override `komposisi:`, `warna:`, atau kamera manual berupa posisi absolut | — |
| Render | Tidak ada pemulihan manual frame (`pemulihan_manual` = [] di ketiga provenance) | — |

## 7. Apakah source perlu diubah di antara cerita?

- **Selama pengembangan Phase 4.2: ya.** Cerita ke-3 menemukan 8 bug generik di engine (§6 laporan penyelesaian), dan QA video menemukan 2 sumber kedip. Semuanya diperbaiki di engine secara generik.
- **Untuk build final: tidak.** Ketiga build final dibangun dari source yang sama (hash identik). Tidak ada perubahan source di antara build final cerita satu dan cerita lain. Ketiga cerita dibangun ulang dan dirender ulang sesudah perubahan engine terakhir.

## 8. Generalisasi fungsional vs artistik

- **Fungsional (diukur):** terbukti untuk cakupan tiga cerita ini.
  - satu source hash;
  - primitif interaksi yang sama di tiga layout berbeda (jalan malam, interior siang, gang senja);
  - 0 FAIL validator dan 0 FAIL QA video;
  - serah-terima di dua layout tanpa kode khusus;
  - konfigurasi deklaratif saja.

  Batasnya: authoring blocking masih perlu disesuaikan manual (arah hadap saat berjalan, jarak jangkau, titik taruh).
- **Artistik (tidak dinilai pembuat):**
  - kualitas antar-cerita **tidak seragam menurut pengamatan pembuat**: interior generalisasi dan gang cerita ke-3 tidak mendapat art direction setingkat benchmark;
  - tokoh baru memakai gaya yang sama tanpa perbaikan siluet;
  - penilaian konsistensi artistik lintas cerita diserahkan ke reviewer.
