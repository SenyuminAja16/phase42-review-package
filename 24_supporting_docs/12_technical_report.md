# Phase 4.2 — Laporan Teknis (Production Quality Gate & Cross-Story Refinement)

Laporan ini berisi **bukti teknis**, bukan penilaian artistik. Saya tidak memberi skor penerimaan artistik untuk pekerjaan sendiri. Angka di bawah adalah indikator yang terukur.

## 0. Build dan basis

| Cerita | Build final | Catatan |
|---|---|---|
| Benchmark `benchmark_warung` | **P4-486e18fc49** | `jalan_kota` malam; Darto memasak, Jali makan |
| Generalisasi `_uji_phase4_rumah` | **P4-2d0645d14d** | `dalam_rumah`; Dimas mengambil teh, menyerahkan ke Sri yang duduk; Sri minum lalu menaruh |
| Uji ke-3 `uji3_kopi_sore` (BARU) | **P4-b1767c3b5e** | `gang_kampung` senja; Harjo makan di bangku; Wulan mengambil kopi dari meja, berjalan, menyerahkan; Harjo minum |

- Basis 4.1: P4-4b69684991 (benchmark) dan P4-21e3aadc90 (generalisasi).
- Checkpoint: `backups/phase41_final_P4-4b69684991_20261127_1031.tar.gz` (SHA-256 `1583201f…f4ac`).
- Proyek bukan repo git.
- Audit temuan reviewer terhadap kode dan rencana: `docs/PHASE42_PLAN.md` (disalin sebagai `19_rencana_dan_audit.md`).

## 1. Analisis akar masalah (ringkas)

| Temuan reviewer | Akar masalah di kode | Perbaikan |
|---|---|---|
| Genggam sutil/sendok terbalik (140 / 178 frame) | `_grip_ik` diam-diam mengganti target `th` dengan `th+180°`, lalu mengukur galat terhadap target yang sudah dibalik | **Supinasi = tangan dicerminkan** (wrist `scale.x −1`, overlay ikut). Rotasi hanya boleh bila profil menyatakannya (`rotasi_lengan`). Galat selalu diukur terhadap pronasi desain. Pergantian di tengah shot memakai ramp 4 frame; di potongan kamera langsung. |
| Sendok di dagu f240; residual 46,5–49,6 px f245–253 | Tangan mendahului cekung sendok (lerp vektor); titik mulut tidak ikut pose kepala | `engine/actions.py`: primitif makan/minum berfase eksplisit; sendok didatarkan **dulu**, baru naik. `_mouth_anchor` mengikuti tampak, anggukan, dan duduk. Kontak diukur dari **cekung sendok/bibir gelas ↔ mulut**. |
| Geser presentasi piring 7,6 cm; piring menembus meja | Benda bulat diukur dengan sudut bbox; tidak ada uji tabrakan dunia | Sampel cincin tepi; `geser_maks` 0,04 m per profil; proxy OBB + `_resolve` |
| Pergelangan Sri 74,8° (f500–501) | Cabang siku berganti di awal minum; pergelangan mengompensasi penuh | Pergelangan menekuk **minimal** di dalam 0,8 × toleransi profil; penalti siku anatomis |
| Blush menimpa hijab (f420/f475) | Elips blush tanpa mask kulit | `chars.skin_mask` per tampak; blush dikalikan mask (VERSION 20) |
| Establishing/penutup: plafon/lantai kosong | Solver hanya menilai halangan, bukan komposisi | `bl_camsolve.frame_shots`: pita okupansi, headroom, letak vertikal per tipe shot; dolly → lensa → kemiringan; semua kepala di dalam tepi aman |
| Kedip f466 | Noise energi api kompor 60 ± 25 W setiap ~2 frame | ±8 W, skala 6 frame (api gas stabil) |
| Crush f214 | — | Diukur: pada video benchmark 4.1, piksel ≤3 hanya 0,01% dan tidak ada clipping. Crush 1,12% ada di video **generalisasi** 4.1 (grading). Di video generalisasi 4.2: `black_crush` PASS. |
| Provenance lemah | `config_hash` tidak divalidasi; identitas yang hilang bisa lolos sebagai PASS | Lihat §5 |

Temuan **baru** dari uji ke-3. Semuanya diperbaiki secara generik, tanpa kondisi nama cerita atau tokoh:

1. **`kit.house` menaruh pot tanaman tanpa memeriksa `avoid`.** Pot set dressing muncul tepat di bangku cerita, dan piring "menembus" daun pot selama 205 frame. → `avoid` diteruskan ke `kit.house`.
2. **Tangan pemegang piring saat makan tidak tercatat "sibuk".** Akibatnya serah-terima bisa memakai tangan yang sedang memegang piring. → Tangan dicatat sibuk, dan penerima memakai tangan yang bebas.
3. **Sprite duduk disajikan di depan dudukan sejauh "jari-jari".** Untuk bangku panjang (0,4 × 1,5 m) yang dilihat serong, badan bangku menutupi kaki. → Celah dihitung dari jejak kotak dudukan sepanjang arah pandang (`seats.kotak`, `setengah`).
4. **Regangan betis duduk memakai pivot di dasar kanvas.** Untuk dudukan setinggi 0,475 m (skala 2,2), lapisan kaki terangkat ke z 0,64–1,17 m, ke belakang badan, sehingga **tokoh tampak duduk tanpa kaki**. Bug ini juga mengenai Sri di generalisasi. → Pivot dipindah ke garis lutut.
5. **Kamera dolly maju untuk okupansi**, lalu two-shot menjadi terlalu lebar dan tokoh terpotong di tepi (uji3 shot 3, f150). → Penyesuaian horizontal; dolly dibatalkan sebagian bila lensa sudah minimum.
6. **Wajah subjek berpaling dari kamera tidak dinilai.** → Penalti `arah_wajah_thd_kamera` (maks 110°) di solver, ditambah aturan QA.
7. **Dorongan tabrakan saat membawa benda juga aktif di titik ambil/letak.** Kontak dengan meja yang sah malah didorong, sehingga gelas melompat 6 cm (f131) dan 19,7 cm (f561) di generalisasi. → Bobot memudar di ujung yang menyentuh dunia. Kontak permukaan dicatat terpisah (`kontak_permukaan_ambil_letak_per_frame`), tidak disembunyikan.
8. **Cek jangkauan rencana hanya menilai `tempat` berupa koordinat.** → Kini jangkar bernama juga dicek, memakai pusat properti.
9. **Suapan tidak terlihat di shot makan.** Ditemukan saat menyiapkan before/after benchmark: shot 5 (f226–281, medium Jali, khusus interaksi makan) hanya memuat kontak sendok–mulut di frame potongan pertama, f226. Validator lama tidak menangkapnya. → `schedule.eat_cycles_visible` menjangkarkan satu siklus agar kontaknya jatuh di dalam setiap shot yang membingkai pemakan; bila ruang sempit, siklus terakhir dipendekkan (≥ 32 frame). Ditambah aturan QA baru `suapan_dalam_shot`.
10. **Kedip benchmark f466 (4.1) / f478, f482 (4.2): bukan cahaya api, tetapi pantulan meja gerobak.** Ditemukan oleh QA video final 4.2 pertama (P4-555dd710c7): `flicker_temporal` FAIL, global 2,37, ubin 18,1 di f478, shot 7 OTS. Penyebabnya bagian atas meja aluminium kasar 0,25 / metal 1,0. Di bawah batas kekasaran raytracing EEVEE (0,5), pantulan ruang-layar dari etalase dan piring tampak berbintik di setiap frame. Pada GPU Colab, sesekali satu frame "menyala" menjadi bidang terang. Render lokal (RTX 3050) hanya menunjukkan bintiknya, tanpa bidang terang, sehingga still lokal f459–468 sebelumnya PASS dan tidak bisa menangkap masalah ini. → Permukaan kerja dibuat aluminium brushed (warna 0,32, kasar 0,6), sehingga pantulannya dari probe yang stabil. Ubin maks lokal f478 turun dari bintik-bintik menjadi 1,4. Perbaikan api kompor (±8 W) tetap berlaku, tetapi bukan penyebab utama. Selain itu, metode pantulan EEVEE untuk semua adegan diganti dari pelacakan ruang-layar (`SCREEN`) ke `PROBE` (`blender_build.py`), karena masalah kelas ini hanya muncul di GPU Colab dan tidak bisa dicek dengan still lokal.
11. **Musik suasana tidak divalidasi di tahap rencana.** `suasana: tenang` (tidak dikenal) di uji ke-3 baru gagal di langkah audio, setelah 750 frame selesai dirender di Colab. Diperbaiki di `story.yaml` (`ceria`), lalu dirender ulang. Validasi mesin belum ditambahkan (lihat 17).
12. **Kedip jendela uji ke-3 (shot 2, f63–145, QA video FAIL 5,52): z-fighting, bukan pantulan.** Muka depan `gorden` dan muka depan `kaca` pada jendela `kit.house` berada di bidang yang persis sama (fx 0,07 m). Bergantung pada goyang kamera genggam, kadang tirai yang menang, kadang kaca, sehingga jendela berganti krem/hijau per frame. Raycast di f140–142 memastikannya, dan kedip ini juga muncul di render lokal. Dugaan awal saya (pantulan ruang-layar) **salah** untuk kasus ini. → Gorden dipindah 2,5 mm di depan kaca. Ini berlaku untuk semua rumah, termasuk latar benchmark. Lokal f141: global 4,49 → 0,30, ubin 46,7 → 0,6.
13. **Pemeriksa z-fighting baru `scripts/dev/cek_sebidang.py`.** Memindai muka sejajar sumbu yang sebidang (≤ 0,8 mm) dan tumpang tindih di antara objek berbeda. Hasil per cerita ada di `build/sebidang.json`. Pemeriksa ini langsung menemukan pasangan gorden–kaca di semua jendela, lalu dinding `ujung_gang` yang sebidang dengan rumah terakhir (diperbaiki). Sisa pasangan kecil tidak diperbaiki (lihat 18): jendela jauh, jari roda, bayangan kontak, poster di balik kaca, dan plafon turun.

## 2. Hasil interaksi (build final)

**Benchmark P4-486e18fc49**

| Benda | Residual genggam maks | Orientasi maks / median (tol) | Pergelangan maks / p95 | Terbalik tanpa izin | Supinasi (sah) | Lainnya |
|---|---|---|---|---|---|---|
| sutil | 0 px | 8,3° / 5,1° (10) | 35,9° / 22,1° | **0** (4.1: 140) | 356 frame | — |
| piring | 0 px | 13,8° / 2,9° (20) | 0° | 0 | — | Geser presentasi 0,0 m (batas 0,04; 4.1: 0,076). Tembus meja 0 frame (4.1: ~225 frame, ~10 cm). 6 frame jarak bebas +4 mm. |
| sendok | 0 px | 8,2° / 4,8° (10) | 33,8° / 25,6° | **0** (4.1: 178) | 140 frame | Kontak cekung–mulut maks 0,0 px dari lebar cekung 35,2 px (18 frame kontak; suapan f233–235 di dalam shot makan) |

IK meleset: 0 frame.

**Generalisasi P4-2d0645d14d**

- **teh:** residual 0 px; orientasi 20,2° (tol 25); pergelangan maks **43,8°** (4.1: 74,8°); kontak bibir gelas–mulut maks 0,2 px dari diameter 64 px.
- **Serah-terima f325:** residual 0/0 px. Status `mepet`: jarak bebas titik 6,2 cm, lintasan 0,39 cm.
- **Ambil/letak:** 6 frame kontak permukaan (dicatat terpisah). Tabrakan dunia 0.

**Uji ke-3 P4-b1767c3b5e**

- **piring Harjo:** residual 0. Pergelangan maks 59,7°, hanya pada **1 frame** (f40, frame pertama segmen genggam); p95 0°.
- **sendok:** residual 0; orientasi 8,2°; pergelangan 30,3°; kontak 0,0 px.
- **kopi:** residual maks 15,3 px (p95 0,4 mm); kontak bibir maks 1,3 px dari 66,7 px; 1 frame −5 mm saat diambil (pada batas toleransi).
- **Serah-terima f398:** 0/0 px, status `ok`, jarak bebas 0,49 m.
- **IK meleset:** 7 frame (Harjo f619–625, 8–15 px) saat cangkir diangkat untuk minum.

## 3. Validator (status PASS / WARN / FAIL / NOT_TESTED / NOT_APPLICABLE)

| Cerita | Interaksi (`validasi_interaksi.py`) | Kamera (`validasi_kamera.py`) |
|---|---|---|
| Benchmark | 33 PASS / 0 WARN / 0 FAIL / 3 NOT_TESTED / 8 NOT_APPLICABLE | `komposisi_pita` WARN; `wajah_subjek` PASS; `aksi_dalam_shot` NOT_APPLICABLE; `suapan_dalam_shot` PASS |
| Generalisasi | 21 PASS / 1 WARN (`serah_terima_tabrakan` mepet) / 0 FAIL / 3 NOT_TESTED / 3 NOT_APPLICABLE | WARN / PASS / PASS / PASS |
| Uji ke-3 | 33 PASS / 2 WARN (`tembus_tubuh`; pergelangan piring 59,7° 1 frame) / 0 FAIL / 3 NOT_TESTED / 6 NOT_APPLICABLE | WARN / PASS / PASS / PASS |

- **`komposisi_pita` WARN:** sebagian besar karena "dibatasi lebar kelompok". Dalam format potret 9:16, two-shot dengan semua kepala di dalam tepi aman tidak bisa mencapai okupansi tinggi minimum. Alasannya tercatat per kunci kamera. Ada juga 2 kunci MCU/closeup dengan garis mata 0,179 (pita 0,18–0,42).
- **Uji unit:** 36 tes Phase 4.2 OK (`14_unittest_phase42.log`). Suite regresi: 89/89 PASS (`14_regression_tests.json`). Keduanya dijalankan setelah render final, dan `plan.json` diverifikasi tidak berubah. 
- **QA render video generalisasi:** 8 PASS dan 1 NOT_TESTED (lip-sync perseptual). `black_crush` PASS (4.1: WARN 1,12%). `flicker_temporal` PASS.
- **Kedip benchmark:** lihat temuan 10 di §1. Still lokal tidak bisa menangkap kedip ini; hanya QA video Colab yang bisa. Hasil QA video final ada di §7 dan `00_STATUS_RENDER.md`.

## 4. Kamera dan lingkungan

- **Komposisi** dicatat per kunci kamera di `13_kamera_komposisi_*.json` → `komposisi`. Isinya nilai awal/akhir, koreksi (lensa, geser bidik, dolly), pita, dan lebar total.
  - Contoh generalisasi (build yang sama sebelum dan sesudah tahap komposisi): okupansi establishing naik dari 0,10 ke 0,24; medium dari 0,28 ke 0,40; plafon kosong medium turun dari 40% ke 20%.
- **Override deklaratif** di `story.yaml` per shot: `komposisi: {tinggi: [a,b], …}` atau `komposisi: false`.
- **Interior `dalam_rumah`** dibangun ulang dengan palet `hangat`/`sejuk`. Isinya:
  - wainscot, lis, plint, drop ceiling, cornice;
  - kusen jati, teralis, gorden lipit, vitrase, roster;
  - pintu panel, foto keluarga, kalender, stop kontak, kipas plafon, sinar matahari dari jendela.
- **Perabot kit:** meja (apron, kaki bubut, taplak, toples), kursi kayu bersandaran, kursi tamu, bufet pajangan, tas sekolah, sandal.
- **Dekorasi cerita generalisasi:** bufet, meja tamu, karpet, tas. Semuanya jenis umum dari kit, didokumentasikan di `story.yaml`.

## 5. Provenance (diperketat)

- **`config_hash`** (story.yaml + plan.json + setelan render) divalidasi per potongan. Bila berubah sesudah render: **FAIL**.
- **Identitas kritis yang hilang** (build ID, scene checksum, source hash, config hash) kini **FAIL**. Sebelumnya bisa lolos sebagai NOT_TESTED atau PASS.
- **Potongan tumpang-tindih:** dipilih yang checksum-nya cocok dengan PNG di disk; semua kandidat dicatat (`potongan_tumpang_tindih`).
- **Pemulihan manual:** dicatat sebagai `peristiwa: pemulihan_manual` (`colab_ambil.py`) dan dilaporkan di `pemulihan_manual`.
- **Checksum video:** asli (hasil rakit) dan distribusi dicatat oleh `provenance.record_video` di `build/video_checksum.json`.
- **Status video:** generalisasi provenance PASS (6 potongan bermetadata), file `_provenance_generalisasi_*.json`.

## 6. Generalisasi lintas cerita

- **Ketiga cerita** dibangun dari source yang sama. Tidak ada percabangan berdasarkan ID cerita atau nama tokoh. Yang berbeda hanya `story.yaml`: tokoh, blocking, shot, dan properti.
- **Uji ke-3:**
  - Tokoh baru: Harjo (tua, peci, kumis, kulit gelap) dan Wulan (muda, rambut panjang).
  - Lingkungan luar yang sudah ada (`gang_kampung`), waktu senja.
  - Primitif yang sama: makan, pegang piring, ambil dari meja, jalan sambil membawa, serah-terima, minum.
- **Penyesuaian authoring** (bukan kode mesin; dicatat di `story.yaml`):
  - **Uji ke-3:** blocking Wulan diulang beberapa kali.
    - Jarak serah-terima 0,74 m ternyata tak terjangkau rig chibi; sekarang ~0,45 m.
    - Arah datang diubah supaya kamera di tengah gang melihat kedua wajah.
    - Wulan menghadap meja saat mengambil, lalu berbalik saat berjalan.
  - **Generalisasi:** titik taruh gelas digeser 14 cm (masih di atas meja), karena jangkauan IK 2D bergantung pada sudut kamera baru.

## 7. Render final

- **GPU:** hanya G4/L4/A100 di Colab. Sesi dimatikan otomatis sesudah selesai.
- **Sesi:** satu sesi G4. Sesuai aturan pengguna, G4/A100 memakai satu sesi untuk semua cerita, L4 memakai dua sesi. Diatur oleh `_render_atur.sh`, `_render_lanjut*.sh`.
- **Hasil per video:**

| Video | GPU | Provenance | `qa_render` | `qa_kedip` |
|---|---|---|---|---|
| Benchmark P4-486e18fc49 (860 frame) | G4, ±1,9 dtk/frame | PASS (8 potongan) | 8 PASS, lip-sync NOT_TESTED; `flicker_temporal` PASS (global 1,02, ubin 5,15) | WARN 1,05 di f465, shot 7 (ambang 1,0; 4.1: 1,58; render 4.2 pertama: FAIL 2,37) |
| Generalisasi P4-2d0645d14d (616) | A100, ±3 dtk/frame | PASS (6) | 8 PASS, lip-sync NOT_TESTED | PASS (maks 0,46) |
| Uji ke-3 P4-b1767c3b5e (750) | G4, ±1,4 dtk/frame | PASS (7) | 6 PASS, 2 WARN, lip-sync NOT_TESTED. `flicker_temporal` WARN: ubin 6,8 di f238–239/f288–289, saat Wulan berjalan, global 0,79 (sebelumnya FAIL 5,43). `black_crush` WARN: 1,55% detail bayangan hilang karena grading (batas FAIL 4%) | PASS (maks 0,78; sebelumnya FAIL 5,52) |

- **Klip diagnostik** (`09_klip_*`): cuplikan dari video final dengan label build dan nomor frame. Isinya suapan/tegukan di shot pemakan, kedua serah-terima, kedip meja gerobak (shot 7), dan kedip jendela (shot 2).
- **Sesi Colab:** render generalisasi pertama hilang karena VM dipangkas server Colab (`session_terminated: pruned`) di tengah unggahan. Render diulang di A100. Satu VM G4 yatim (alokasi terlambat tanpa nama sesi) ditemukan dan dilepas dengan izin pengguna. Pemeriksaan VM yatim (`scripts/dev/colab_yatim.py`) kini dijalankan setelah setiap render.

## 7a. Catatan provenance selama Gate E

Build ID dihitung dari hash `engine/*.py`, `engine/sets`, `engine/colab`, dan `make.py`, sehingga perubahan apa pun di mesin membuat semua build lama basi. Selama Gate E ini terjadi tiga kali, dan setiap kali render dengan identitas lama dihentikan atau dibuang, tidak dicampur:

1. Penambahan aturan QA `eat_contact_in_shot` di `engine/qa_rules.py`: tidak mengubah gambar, tetapi mengubah ID. Render yang sedang berjalan dihentikan (`_log_colab_*_batal_buildid_berubah.txt`).
2. Perbaikan meja gerobak di `engine/sets/kit.py`, setelah QA video menemukan kedip. Video benchmark P4-555dd710c7 tidak dipakai. Video generalisasi P4-da5e095e8a, yang sudah selesai dengan provenance PASS, juga tidak dipakai. Gambarnya identik, tetapi source hash-nya berbeda; semua cerita dirender ulang dari source yang sama.
3. Perbaikan `suasana` musik uji ke-3: config hash berubah, sehingga frame uji ke-3 yang sudah selesai (P4-3b9aa5db79) dirender ulang.
4. QA video uji ke-3 (P4-888954b55c) FAIL kedip, lalu pantulan diubah ke `PROBE`. Render benchmark P4-d61be635aa dihentikan di 240/860 frame setelah ditemukan bahwa penyebab sebenarnya z-fighting (temuan 12), dan job Blender di VM ikut dihentikan.
5. Perbaikan gorden dan `ujung_gang`, lalu semua cerita dibangun ulang dan dirender ulang.

Video yang dibuang karena basi, walaupun beberapa provenance-nya PASS: benchmark P4-555dd710c7 dan P4-71837de932, generalisasi P4-da5e095e8a dan P4-92a110fd6f, uji ke-3 P4-3b9aa5db79 (gagal audio) dan P4-888954b55c. Log-nya disimpan di `_log_colab_*`.

Ketiga build final berasal dari satu source hash yang sama. Metrik interaksi dan hasil validator tidak berubah sepanjang pergantian ID ini.

## 8. Daftar file paket

Lihat `00_INDEX.md`. Checksum semua file ada di `99_CHECKSUMS.json`.
