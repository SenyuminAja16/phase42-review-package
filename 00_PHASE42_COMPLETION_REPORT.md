# Phase 4.2 — Laporan Penyelesaian (Completion Report)

**Production Quality Gate & Cross-Story Refinement** pada Blender Hybrid 2D–3D Animation Production Engine.

Laporan ini mendokumentasikan hasil Phase 4.2 **sebagaimana adanya**. Isinya hanya bukti teknis dan angka terukur. **Tidak ada skor penerimaan artistik dari pembuat.** Penerimaan artistik (target ≥ 8,25/10), kesiapan produksi lintas cerita, dan perlu-tidaknya pengembangan lanjutan diputuskan oleh reviewer independen.

Status yang dipakai di seluruh paket:
- **COMPLETE:** dikerjakan dan terverifikasi oleh data.
- **PARTIAL:** sebagian.
- **NOT_IMPLEMENTED:** tidak dikerjakan.
- **NOT_TESTED:** tidak dapat diuji otomatis.
- **FAILED:** dikerjakan tetapi gagal.

Status validator memakai lima nilai mesin: PASS, WARN, FAIL, NOT_TESTED, NOT_APPLICABLE.

---

## 1. Ringkasan eksekutif

- **Render final.** Ketiga cerita dirender final dari **satu source hash yang sama**, `f7ccb35625ca…`, dihitung dari 40 file engine dan `make.py`. Render dilakukan di GPU Colab G4/A100. Provenance per frame: PASS untuk 860, 616, dan 750 frame. Semua frame terverifikasi checksum terhadap metadata potongan.
- **Interaksi fisik (Gate A).** Kategori cacat yang dilaporkan reviewer 4.1 kini terukur nol:
  - genggam terbalik tanpa izin: 0 frame (4.1: 140 sutil, 178 sendok);
  - sendok di dagu: kontak cekung–mulut 0,0 px;
  - residual genggam f245–253: 0,0 px (4.1: 46,5–49,6 px);
  - pergelangan Sri: maks 43,8° (4.1: 74,8°);
  - piring menembus meja: 0 frame;
  - geser presentasi piring: 0,0 m (batas 0,04 m).

  Yang **belum dibuat**: pose penyangga piring dengan jari di bawah piring.
- **Kualitas visual tokoh (Gate B): sebagian.**
  - Selesai: blush dipotong mask kulit per tampak di generator sprite; kaki duduk diperbaiki (pivot lutut, celah dudukan).
  - **Tidak dikerjakan:** kontur bahu/siku/pergelangan, sambungan tangan–lengan bawah, pose tangan per kelas genggam, transisi tampak.
- **Kamera, lingkungan, cahaya (Gate C): sebagian.**
  - Selesai: komposisi per tipe shot di solver kamera; interior `dalam_rumah` dibangun ulang; akar kedip ditemukan dan diperbaiki (pantulan raytraced yang hanya muncul di GPU Colab; z-fighting gorden–kaca).
  - **Tidak dikerjakan:** hero asset benchmark, preset cahaya baru.
- **Generalisasi (Gate D).** Cerita ketiga yang baru (*Kopi Sore di Gang*: lingkungan luar `gang_kampung`, tokoh baru Harjo dan Wulan) berjalan dengan primitif interaksi yang sama, tanpa kondisi khusus cerita atau tokoh di engine. Generalisasi **fungsional** terbukti oleh data. Generalisasi **artistik** belum dinilai.
- **Penerimaan produksi (Gate E).**
  - Validator: 0 FAIL di ketiga cerita.
  - QA video: tidak ada FAIL. WARN tersisa:
    - kedip benchmark 1,05 di f465 (ambang 1,0);
    - ubin kedip 6,8 dan black crush 1,55% di uji ke-3.
  - Lip-sync perseptual: NOT_TESTED.
  - Uji unit: 36/36 OK. Regresi: 89/89 PASS.

## 2. Identitas build final

| Cerita | Folder | Build ID | Frame | Scene `.blend` SHA-256 | Video final (SHA-256) |
|---|---|---|---|---|---|
| Satu Bungkus Lagi (benchmark) | `stories/benchmark_warung` | **P4-486e18fc49** | 860 | `78091a6a…cf27c6` | `01_benchmark_phase42_P4-486e18fc49.mp4` (`99_CHECKSUMS.json`) |
| Teh Sore untuk Ibu (generalisasi) | `stories/_uji_phase4_rumah` | **P4-2d0645d14d** | 616 | `eebd26c6…fca51c` | `02_generalization_phase42_P4-2d0645d14d.mp4` |
| Kopi Sore di Gang (cerita ke-3) | `stories/uji3_kopi_sore` | **P4-b1767c3b5e** | 750 | `b9467133…f61f67` | `03_third_story_phase42_P4-b1767c3b5e.mp4` |

- **Source hash bersama:** `f7ccb35625ca892f68798b6b10541e6810d9a769c139a10ab073e7e045631c8c`. Saat paket dibuat, hash dihitung ulang dan **cocok** dengan ketiga manifest.
- **Basis 4.1:**
  - P4-4b69684991 (benchmark) dan P4-21e3aadc90 (generalisasi);
  - checkpoint `backups/phase41_final_P4-4b69684991_20261127_1031.tar.gz`, SHA-256 `1583201f…f4ac`.
- **Format:** semua video 1080×1920, 30 fps, AAC 48 kHz.
- **Engine:** Blender 4.5.16 LTS, EEVEE, 32 sampel.

## 3. Ringkasan perbaikan yang diimplementasikan

| Area | Perbaikan | File / fungsi utama |
|---|---|---|
| Orientasi genggam | Supinasi = tangan **dicerminkan** (`scale.x −1`, overlay ikut). Rotasi lengan hanya bila profil menyatakannya (`rotasi_lengan`). Galat selalu diukur terhadap pronasi desain. Aturan `inversi_genggam` → FAIL. | `engine/bl_interact.py` `Director._grip_ik`, `engine/grip.py` (profil), `engine/qa_rules.py` |
| Primitif makan/minum | Fase eksplisit: sendok → angkat → dekat_mulut → kontak → tarik → kembali → istirahat. Mulut buka/kunyah, teguk dengan kemiringan gelas. Sendok didatarkan sebelum naik. | `engine/actions.py` (baru: `eat`, `drink`, `EAT_PHASES`, `DRINK_PHASES`) |
| Jangkar mulut | Titik mulut mengikuti tampak, anggukan, dan duduk. Kontak diukur antara cekung sendok/bibir gelas dan mulut, relatif terhadap ukuran benda. | `bl_interact.Director._mouth_anchor`, `qa_rules` `kontak_mulut` |
| Jadwal suapan | Satu siklus dijangkarkan agar kontak jatuh di dalam setiap shot yang membingkai pemakan. | `engine/schedule.py` `eat_cycles_visible`, `contact_in`; `engine/plan.py` |
| Piring / presentasi | Sampel cincin tepi untuk benda bulat. Geser presentasi dibatasi `geser_maks` 0,04 m per profil dan dicatat terpisah. | `bl_interact.Director._present`, `_plate_c`; `engine/grip.py` |
| Tabrakan dunia | Proxy OBB objek statis. `_resolve` untuk benda yang dipegang. Kontak sah di titik ambil/letak dicatat terpisah. | `bl_interact.py` (proxy, `_resolve`), `kontak_permukaan_ambil_letak_per_frame` |
| Serah-terima | Kandidat titik dan lintasan diuji terhadap proxy. Cabang siku dan batas pergelangan divalidasi di fase kontak. | `bl_interact.Director._solve_handovers`, `_handover_search`; `qa_rules` |
| Pergelangan | Tekuk minimal di dalam 0,8 × toleransi profil; penalti siku anatomis. | `bl_interact._solve_dof` |
| Mask kulit | `chars.skin_mask` per tampak; blush dikalikan mask (chars VERSION 20). | `engine/chars.py` |
| Duduk | Pivot regangan betis di garis lutut. Celah dudukan dari jejak kotak dudukan. | `engine/bl_rig.py`, `engine/seats.py` (`kotak`, `setengah`) |
| Komposisi kamera | `frame_shots`: pita okupansi, headroom, letak vertikal per tipe shot. Urutan koreksi: dolly → lensa → kemiringan. Semua kepala di dalam tepi aman. Penalti wajah membelakangi kamera. Override deklaratif `komposisi:` di story.yaml. | `engine/bl_camsolve.py` |
| Interior | `dalam_rumah` dibangun ulang dengan palet `hangat`/`sejuk`, detail arsitektur, dan perabot kit baru. | `engine/sets/dalam_rumah.py`, `engine/sets/kit.py` |
| Kedip | Api kompor ±25 W → ±8 W. Meja kerja gerobak menjadi aluminium brushed. Pantulan EEVEE global `SCREEN` → `PROBE`. Gorden 2,5 mm di depan kaca. `ujung_gang` tidak lagi sebidang. | `kit.gerobak_makan`, `kit.house`, `engine/blender_build.py`, `engine/sets/gang_kampung.py` |
| Validasi | Aturan baru di `qa_rules.py` (103 → 302 baris): inversi, kontak mulut, geser presentasi, tabrakan dunia, pergelangan fase kontak, cabang siku, komposisi, wajah, suapan dalam shot. Validator kamera. `cek_sebidang.py` (z-fighting). `qa_kedip.py`. | `engine/qa_rules.py`, `scripts/dev/validasi_*.py`, `cek_sebidang.py`, `qa_kedip.py` |
| Provenance | `config_hash` divalidasi. Identitas kritis yang hilang → FAIL. Potongan tumpang-tindih dan pemulihan manual dicatat. Checksum video asli/distribusi dicatat. | `engine/provenance.py` |
| Bug yang ditemukan uji ke-3 (generik) | `avoid` pada `kit.house`; tangan pemegang piring dicatat sibuk; celah duduk bangku panjang; pivot betis; dolly two-shot; wajah berpaling; dorongan tabrakan di titik ambil/letak; cek jangkauan jangkar bernama. | lihat §6 |

Perubahan ukuran file engine dibanding checkpoint 4.1 (jumlah baris):

| File | 4.1 → 4.2 | File | 4.1 → 4.2 |
|---|---|---|---|
| `actions.py` (baru) | 0 → 108 | `bl_camsolve.py` | 246 → 439 |
| `bl_interact.py` | 1400 → 1733 | `qa_rules.py` | 103 → 302 |
| `provenance.py` | 180 → 238 | `sets/dalam_rumah.py` | 104 → 218 |
| `chars.py` | 788 → 820 | `sets/kit.py` | 1364 → 1431 |
| `schedule.py` | 84 → 130 | `grip.py` | 144 → 160 |
| `bl_rig.py` | 706 → 721 | `plan.py` | 659 → 669 |
| `seats.py` | 46 → 52 | `blender_build.py` | 349 → 356 |
| `sets/gang_kampung.py` | 97 → 98 | `make.py` | 446 → 448 |

## 4. Matriks kepatuhan (setiap persyaratan Phase 4.2)

| § | Persyaratan | Status | Bukti / catatan |
|---|---|---|---|
| 3 P0.1 | Batasan orientasi anatomis bertanda | COMPLETE | `inversi_genggam` PASS (0 frame) di 3 cerita; `test_grip_inversion_rule`, `test_phase41_flip_without_mirror_is_inversion` |
| | Sisi ibu jari / sisi jari benar | COMPLETE | `test_thumb_side_matches_tip_for_both_variants`; supinasi = cermin, bukan putar 180° |
| | Galat diukur terhadap genggam yang dimaksud | COMPLETE | Galat terhadap pronasi desain: sutil maks 8,3°, sendok 8,2° (tol 10°). 4.1 melaporkan ~0,2° terhadap target yang sudah dibalik. |
| | Penyesuaian pose/blocking bila tak ada solusi anatomis | PARTIAL | Solusi lewat varian supinasi yang diizinkan profil. Penyesuaian blocking otomatis tidak dibuat; di 3 cerita tidak ada frame tanpa solusi anatomis. |
| | FAIL/WARN eksplisit untuk inversi tidak sah | COMPLETE | aturan `inversi_genggam` (FAIL bila > 0) |
| | Evaluasi 140 / 178 frame terbalik | COMPLETE | 0 / 0 tanpa izin. 356 frame sutil dan 140 frame sendok memakai supinasi sah; perlu dinilai visual. |
| 3 P0.2 | Dimensi fisik piring konstan | COMPLETE | `skala_fisik_benda` piring 1,0 (benchmark, uji ke-3) |
| | Tidak ada translasi tak terbatas bergantung kamera | COMPLETE | `geser_presentasi` piring maks 0,0 m (batas 0,04 m; 4.1: 0,076 m) |
| | Pose penyangga piring (jari di bawah, ibu jari di tepi) | **NOT_IMPLEMENTED** | Piring tetap genggam jepit tepi (`rim`). Lapisan tangan `support` tidak dibuat. |
| | Kontak konsisten antar-potongan kamera | PARTIAL | Kontak tangan–benda 0 px di setiap frame. **Posisi dunia benda melompat di potongan kamera** hingga 0,46 m (benchmark piring) dan 1,22 m (uji ke-3 piring, f61). Dicatat, tanpa ambang (lihat §11). |
| | Translasi fisik→presentasi dicatat terpisah, dengan toleransi | COMPLETE | `20_presentation_transform/*.json` |
| 3 P0.3 | Fase sendok/angkat/dekati/kontak/kunyah-teguk/kembali/istirahat | COMPLETE | `engine/actions.py`; fase per frame di `interaksi.json`; lembar `09_before_after/05_*` |
| | Jangkar semantik melalui pose kepala & tampak | COMPLETE | `Director._mouth_anchor` |
| | Kontak cekung sendok ↔ mulut | COMPLETE | rasio maks / lebar cekung: benchmark 0,0; uji ke-3 0,0; gelas 0,003 / 0,019 (batas 0,25) |
| | Orientasi makanan/alat selama gerak | COMPLETE | `test_spoon_levelled_before_it_rises` |
| | Tanpa koreksi khusus Jali | COMPLETE | Primitif yang sama dipakai Harjo (uji ke-3); `grep` engine: nama tokoh hanya muncul di komentar |
| 3 P0.4 | Kandidat & lintasan sadar-tabrakan; proxy sederhana | COMPLETE | Proxy OBB: 56 (generalisasi), 49 (uji ke-3); `serah_terima_tabrakan` |
| | Jangkauan pemberi/penerima | COMPLETE | residual 0/0 px di kedua serah-terima |
| | Orientasi anatomis, jarak bebas dunia | COMPLETE / **WARN** | Generalisasi: titik 6,2 cm, lintasan 0,39 cm dari `daun_meja` → `mepet` (WARN). Uji ke-3: 0,49 m (ok). |
| | Tumpang tindih genggam saat pindah kepemilikan; transform kontinu | COMPLETE | `transisi_kepemilikan` PASS, lompatan maks 0,0106 m (tol 0,02) |
| | Kontinuitas cabang siku; batas pergelangan | COMPLETE | `cabang_siku` 0 kejadian; `pergelangan_fase_kontak` PASS (maks 43,8°, batas 45/60) |
| | Investigasi Sri 74,8° f500–501 | COMPLETE | Akar masalah: cabang siku berganti di awal minum. 4.2: f500 29,7°, f501 39,2°, maks 43,8°. |
| | Serah-terima di > 1 layout tanpa modifikasi khusus | COMPLETE | Generalisasi f325 dan uji ke-3 f398, dari source yang sama |
| 4 | Kontur bahu, siku, pergelangan | **NOT_IMPLEMENTED** | lembar `09_before_after/02_*` menunjukkan keadaan saat ini |
| | Sambungan tangan–lengan bawah | **NOT_IMPLEMENTED** | |
| | Pose tangan per kelas genggam | **NOT_IMPLEMENTED** | Hanya pose yang sudah ada (kepal/jepit); `support` tidak dibuat |
| | Siluet kaki duduk | PARTIAL | Pivot lutut dan celah dudukan diperbaiki; bentuk kaki masih sederhana |
| | Postur tubuh | NOT_IMPLEMENTED | |
| | Keberagaman siluet tokoh | PARTIAL | Tokoh baru dari parameter yang sudah ada (peci, kumis, tua, rambut panjang) |
| | Konsistensi tampak depan/3-4/profil/belakang; kontinuitas transisi | NOT_IMPLEMENTED | Tidak ada pekerjaan baru |
| | Mask kulit per tampak (blush Sri f420/f475) | COMPLETE | `test_blush_never_outside_skin`; lembar `08_*` |
| | Perbaikan di generator sprite, bukan gambar | COMPLETE | `chars.skin_mask` |
| | Pertahankan dialog, mata, kedip, gestur, gerak kepala | COMPLETE | regresi 89/89 PASS; `rencana_mulut`, `kedip` PASS |
| 5 | Okupansi subjek, headroom | COMPLETE dengan WARN | `komposisi_pita` WARN di 3 cerita (two-shot 9:16 "dibatasi lebar kelompok"; 2 kunci mata 0,179 vs pita 0,18) |
| | Ruang depan (lead room) | dipertahankan dari 4.1 | Tidak diubah |
| | Keterlihatan multi-tokoh | COMPLETE | Semua kepala di dalam tepi aman 0,86 NDC |
| | Keterlihatan aksi tangan/benda | PARTIAL | `aksi_dalam_shot` = heuristik daftar shot, bukan proyeksi |
| | Hierarki fokus | PARTIAL | Penalti wajah membelakangi kamera (`arah_wajah_thd_kamera`) dan subjek per shot |
| | Jarak fokus sesuai aksi utama | dipertahankan dari 4.1 | DOF ke titik bidik (`blender_build.py`); tidak dikhususkan ke aksi |
| | Ruang negatif bermakna | PARTIAL | Wide/establishing generalisasi masih menyisakan ~44–51% ruang atas (kamera.json) |
| | Establishing & penutup | COMPLETE dengan WARN | Generalisasi establishing: tinggi subjek 0,10 → 0,22–0,35; ruang bawah 0,38 → 0,27 |
| | Konsistensi arah layar | NOT_IMPLEMENTED | Tidak ada aturan garis 180° |
| | Override deklaratif | COMPLETE | `komposisi: {tinggi: [a,b]}` / `komposisi: false` per shot; tidak dipakai di 3 cerita final |
| 6 | Interior: denah, proporsi perabot, palet, detail arsitektur, penempatan | PARTIAL | `dalam_rumah.py` 104 → 218 baris; palet `sejuk` tidak dirender; dinding polos, perabot tanpa jejak pakai |
| | Hero asset benchmark (nasi goreng, sutil, piring, gelas, alat masak, gerobak) | **NOT_IMPLEMENTED** | Hanya material meja kerja gerobak (untuk kedip) |
| | Tier kualitas aset | NOT_IMPLEMENTED | |
| 7 | Preset cahaya interior/eksterior baru | NOT_IMPLEMENTED | Preset `atmosfer.py` yang ada; interior mendapat sinar jendela |
| | DOF yang sesuai | dipertahankan | |
| | Detail bayangan | COMPLETE untuk metrik | `black_crush` PASS benchmark/generalisasi (4.1 generalisasi WARN 1,12%); uji ke-3 WARN 1,55% |
| | Investigasi kedip f215 / f466, crush f214 | COMPLETE | f215: `qa_kedip` shot 4 maks 0,35 di f215 (PASS). f466: akar masalah pantulan meja (lihat §5); sisa WARN 1,05 f465. f214: crush ada di video generalisasi 4.1, bukan benchmark. |
| 8 | Regresi: inversi bertanda, kontak sendok–mulut, kontak penyangga piring, translasi presentasi, tabrakan dunia, pergelangan fase kontak, cabang siku, overflow lapisan wajah, okupansi, oklusi aksi | COMPLETE kecuali penyangga piring | 36 tes `tests/test_phase42*.py` (daftar di `13_regression_tests.json`). Kontak penyangga piring tidak diuji karena pose `support` tidak ada. |
| | Toleransi relatif-ukuran & kontak semantik | COMPLETE | rasio thd lebar cekung/diameter gelas |
| | Bedakan kebenaran matematis/teknis/visual/artistik | COMPLETE (dokumentasi) | `kategori` per aturan; daftar masalah visual yang lolos validator (§10) |
| | Lima status validasi | COMPLETE | |
| | Uji integrasi dengan scene nyata & render | COMPLETE | Validator berjalan di `scene.blend` final; QA berjalan di video final |
| | Lip-sync perseptual tidak diklaim dari timestamp | COMPLETE | `lip_sync_perseptual` = NOT_TESTED |
| 9 | config_hash divalidasi; identitas kritis hilang ≠ PASS | COMPLETE | `test_config_hash_change_fails`, `test_missing_scene_identity_is_fail_not_pass` |
| | Catat potongan, tumpang tindih, pemulihan manual, checksum video, scene/source/config hash, setelan render | COMPLETE | `15_build_provenance.json` (uji ke-3: 3 kandidat potongan per rentang, dipilih berdasarkan checksum; pemulihan manual 0) |
| 10 | Pertahankan 2 cerita; tambah 1 cerita kecil di lingkungan luar yang ada | COMPLETE | `uji3_kopi_sore` di `gang_kampung` |
| | Source sama untuk semua build final; tanpa kondisi ID cerita/nama tokoh | COMPLETE | source hash identik; `grep` engine → nama cerita/tokoh hanya di 2 komentar |
| | Aset/override baru didokumentasikan | COMPLETE | `22_generalization_evidence.md` |
| 11 | Gerbang A–E; still & klip murah saat iterasi | COMPLETE | Lihat §5 dan §12 (render penuh yang dibuang tercatat) |
| | Before/after dengan kondisi identik bila mungkin, berlabel bila berbeda | PARTIAL | Lembar berlabel; **tidak ada A/B satu-variabel** (build 4.1 dan 4.2 berbeda di banyak variabel) |
| 12 | Bukti yang diminta | COMPLETE | Paket ini; solid view 4.2 **tidak tersedia** |

## 5. Hasil Quality Gate A–E

| Gerbang | Hasil | Ringkasan |
|---|---|---|
| **A — interaksi fisik** | Lolos kriteria numerik; PARTIAL terhadap spesifikasi | 0 FAIL validator. Inversi 0. Kontak mulut ≤ 0,019 × ukuran. Pergelangan fase kontak ≤ 43,8°. Tabrakan dunia 0. Serah-terima generalisasi WARN `mepet`. Pergelangan piring uji ke-3 59,7° pada 1 frame (f40, WARN). IK meleset 7 frame uji ke-3 (f619–625, 8–15 px). Pose penyangga piring tidak dibuat. |
| **B — visual tokoh** | PARTIAL | Blush dan kaki duduk diperbaiki. Lengan, pose tangan, siluet, dan transisi tampak tidak dikerjakan. |
| **C — kamera/lingkungan/cahaya** | PARTIAL | Komposisi (WARN beralasan) dan interior dibangun ulang. Kedip diselidiki dan diperbaiki. Hero asset dan preset cahaya tidak dikerjakan. |
| **D — generalisasi** | Fungsional: lolos | Cerita ke-3 dibangun dari source dan primitif yang sama. Artistik: belum dinilai. |
| **E — penerimaan produksi** | Teknis: lolos dengan WARN | 3/3 video provenance PASS; QA 0 FAIL; lip-sync NOT_TESTED. |

Validator per cerita (build final):

| Cerita | Interaksi `validasi_p42.json` | Kamera `validasi_kamera.json` |
|---|---|---|
| Benchmark | 33 PASS · 0 WARN · 0 FAIL · 3 NOT_TESTED · 8 NOT_APPLICABLE | `komposisi_pita` WARN; `wajah_subjek` PASS; `aksi_dalam_shot` NOT_APPLICABLE; `suapan_dalam_shot` PASS |
| Generalisasi | 21 PASS · 1 WARN (`serah_terima_tabrakan` mepet) · 0 FAIL · 3 NT · 3 NA | WARN / PASS / PASS / PASS |
| Uji ke-3 | 33 PASS · 2 WARN (`tembus_tubuh` 1 pelanggaran; `tekuk_pergelangan` piring 59,7° 1 frame) · 0 FAIL · 3 NT · 6 NA | WARN / PASS / PASS / PASS |

Ketiga NOT_TESTED di validator interaksi (`render_crush`, `render_alpha`, `audio_sinkron`) diuji di luar Blender oleh `qa_render.py` pada video final (§9).

## 6. Analisis akar masalah (file, kelas, fungsi aktual)

| Masalah | Akar masalah | Perbaikan |
|---|---|---|
| Genggam terbalik (140 sutil / 178 sendok) | `bl_interact.Director._grip_ik`: bila `\|th+180−φ0\|+25 < \|th−φ0\|`, target `th` diganti `th+180`. `ori_err` lalu diukur terhadap target yang sudah dibalik, sehingga skor ~0°. Penaltinya hanya 12 di `_solve_dof.cost_sol`. | Supinasi = cermin tangan. Rotasi lengan hanya bila `rotasi_lengan` di profil `grip.py`. Galat selalu diukur terhadap pronasi desain. Aturan `inversi_genggam`. |
| Sendok di dagu f240; residual f245–253 | `Director.pose("spoon_eat")`: titik mulut = `body.at(fwd_m, …, mp[1])`, tetap pada bidang badan dan tidak ikut pose kepala. Tangan mendahului cekung karena lerp vektor. Kontak diukur antara tangan dan gagang. | `actions.eat` (level sebelum naik, pendekatan lurus dari depan), `_mouth_anchor`, kontak cekung–mulut |
| Suapan tidak terlihat di shot makan (temuan baru 4.2) | Siklus terjadwal tanpa mengetahui shot; kontak shot 5 hanya di f226 (frame potongan). | `schedule.eat_cycles_visible`; aturan `qa_rules.eat_contact_in_shot` |
| Piring geser 7,6 cm / menembus meja | `_present`: pengganti skala = geser sepanjang sinar kamera tanpa batas (`p.shift_log` tidak dibatasi). Benda bulat diukur dari sudut bbox. Tidak ada uji tabrakan dunia. | Sampel cincin tepi, `geser_maks`, proxy OBB + `_resolve` |
| Pergelangan Sri 74,8° | Cabang IK siku berganti di awal pose `drink`; pergelangan mengompensasi penuh (bukan dari serah-terima). | Tekuk pergelangan minimal (0,8 × toleransi), penalti siku anatomis, aturan `cabang_siku` |
| Blush meluber ke hijab | `chars.face`/`face_profile` menggambar elips blush pada posisi tetap tanpa mask kulit; oval wajah berhijab lebih kecil. | `chars.skin_mask` per tampak |
| Plafon/lantai kosong | `bl_camsolve.solve` → `comp()` hanya menilai keterlihatan/halangan; establishing interior memakai jarak tetap terhadap ukuran ruang. | `bl_camsolve.frame_shots` (pita per tipe shot) |
| Kedip benchmark f466 (4.1) / f478 (4.2) | **Hipotesis 4.1 (noise api) hanya sebagian benar.** Penyebab utama: meja kerja gerobak aluminium kasar 0,25 di bawah batas raytracing EEVEE 0,5, dengan pantulan ruang-layar dari etalase/piring. Di GPU Colab sesekali satu frame "menyala"; di GPU lokal hanya berbintik, sehingga still lokal tidak bisa menangkapnya. | `kit.gerobak_makan` meja aluminium brushed (0,32 / kasar 0,6); `blender_build.py` `ray_tracing_method = "PROBE"` untuk semua adegan; api ±8 W |
| Kedip jendela uji ke-3 (FAIL 5,52) | `kit.house`: muka depan `gorden` dan `kaca` sebidang (fx 0,07 m) → z-fighting. **Diagnosis awal saya (pantulan) salah**; dibuktikan dengan raycast f140–142. | Gorden 2,5 mm di depan kaca; `ujung_gang` tidak lagi sebidang; detektor `scripts/dev/cek_sebidang.py` |
| Provenance lemah | `provenance.validate`: `config_hash` dicatat tetapi tidak divalidasi; `checksum_adegan_sama` NOT_TESTED → status bisa PASS. | Lihat §4 baris 9 |
| Bug yang ditemukan uji ke-3 | (1) `kit.house` tanpa `avoid` → pot di bangku. (2) Tangan pemegang piring tidak tercatat sibuk. (3) Celah duduk dari "jari-jari" untuk bangku panjang. (4) Pivot betis di dasar kanvas → kaki hilang (juga Sri). (5) Dolly two-shot memotong tokoh. (6) Wajah berpaling tidak dinilai. (7) Dorongan tabrakan di titik ambil/letak → gelas melompat 6 cm (f131) dan 19,7 cm (f561). (8) Cek jangkauan hanya untuk `tempat` berupa koordinat. | Semua diperbaiki secara generik (`kit.py`, `bl_interact.py`, `seats.py`, `bl_rig.py`, `bl_camsolve.py`, `plan.py`) |
| Validasi `musik.suasana` | Nilai tidak dikenal baru gagal di langkah audio, setelah render. | **Tidak diperbaiki di engine**; `story.yaml` uji ke-3 dikoreksi (`ceria`) |

## 7. Keputusan teknis & perubahan arsitektur

- **Arsitektur dipertahankan:** rig 2D berlapis di Blender, set prosedural modular, konfigurasi `story.yaml`. Tidak ada percabangan berdasarkan ID cerita atau nama tokoh.
- **Modul baru `engine/actions.py`** (murni Python, tanpa `bpy`): primitif makan/minum dapat diuji unit tanpa Blender.
- **Supinasi = cermin** dipilih alih-alih rotasi lengan bebas. Sprite 2D satu lapis tidak bisa memutar lengan bawah secara 3D; mencerminkan tangan menjaga sisi ibu jari yang benar.
- **Proxy OBB** alih-alih mesh penuh: cukup untuk meja, gerobak, dan kursi, dan murah.
- **Pantulan `PROBE` global:** kompromi antara stabilitas antar-frame (hasil sama di GPU lokal dan Colab) dan ketajaman kilap logam/kaca. Diputuskan pengguna (perbaikan global) setelah QA video.
- **Build ID = hash source:** perubahan engine sekecil apa pun membuat semua build basi. Konsekuensinya, setiap perbaikan di Gate E memaksa render ulang ketiga cerita (§12).
- **Pemeriksaan pra-render baru:** `cek_sebidang.py` untuk z-fighting. QA kedip tetap hanya pasti dari video GPU Colab.

## 8. Perbedaan rencana (`docs/PHASE42_PLAN.md`) vs implementasi

| Rencana | Implementasi |
|---|---|
| A2: lapisan tangan `support` di rig2d (telapak di bawah, ibu jari di tepi) | **Tidak dibuat.** Geser presentasi dibatasi dan tabrakan diselesaikan, tetapi pose piring tetap jepit tepi. |
| A1: solver menggeser pose/blocking bila tak ada solusi anatomis | Diganti dengan varian supinasi yang diizinkan profil. Tidak ada penggeser blocking otomatis. |
| Gate B: kontur lengan, pose tangan per kelas genggam | Tidak dikerjakan. |
| Gate C: hero asset benchmark (tier kualitas), preset cahaya interior/eksterior baru | Tidak dikerjakan. |
| Gate C: investigasi kedip f466 dengan hipotesis noise api | Hipotesis hanya sebagian benar. Penyebab utama ditemukan di QA video final (pantulan meja), ditambah z-fighting di uji ke-3. |
| Gate D: cerita ke-3 kecil | Sesuai rencana. Sekaligus menemukan 8 bug generik (§6). |
| Gate E: render final sekali sesudah A–D | Render final diulang beberapa kali karena perbaikan engine di Gate E (§12). |
| Tidak direncanakan | Penjadwal suapan sadar-shot (`eat_cycles_visible`), pemeriksa z-fighting, pemeriksa VM Colab yatim. |

## 9. Hasil uji regresi & QA pasca-render

- **Uji unit Phase 4.2:** 36 tes, OK. Daftar nama tes ada di `13_regression_tests.json`.
- **Suite regresi:** 89/89 PASS, 0 FAIL, 0 ERROR, 0 NOT_TESTED.
- Keduanya dijalankan **sesudah** render final. `plan.json` ketiga cerita diverifikasi tidak berubah (byte-identik).

QA video final (`14_post_render_QA.json`):

| Video | `qa_render` | `flicker_temporal` | `black_crush` | `qa_kedip` (per shot, ambang WARN 1,0 / FAIL 2,0) |
|---|---|---|---|---|
| Benchmark | 8 PASS, 1 NOT_TESTED (lip-sync) | PASS (global 1,02, ubin 5,15) | PASS (p95 0,14%) | **WARN 1,05 di f465** (shot 7); shot 4 (f215) 0,35 PASS |
| Generalisasi | 8 PASS, 1 NOT_TESTED | PASS | PASS (4.1: WARN 1,12%) | PASS (maks 0,46) |
| Uji ke-3 | 6 PASS, 2 WARN, 1 NOT_TESTED | **WARN**: ubin 6,8 di f238–239/f288–289 (Wulan berjalan), global 0,79 | **WARN** 1,55% (FAIL > 4%) | PASS (maks 0,78; sebelum perbaikan FAIL 5,52) |

## 10. Peringatan & kegagalan yang belum terselesaikan

- **FAIL:** tidak ada, baik di validator maupun QA video final.
- **WARN:**
  - `komposisi_pita` (3 cerita);
  - `serah_terima_tabrakan` mepet (generalisasi);
  - `tembus_tubuh` 1 pelanggaran (uji ke-3);
  - pergelangan piring 59,7° f40 (uji ke-3);
  - `qa_kedip` benchmark 1,05 f465;
  - `flicker_temporal` ubin dan `black_crush` (uji ke-3).
- **NOT_TESTED:** lip-sync perseptual (3 video).
- **Tidak divalidasi dengan ambang:** lompatan posisi dunia benda di potongan kamera (§11).
- **IK meleset:** 7 frame di uji ke-3 (f619–625, 8–15 px) saat cangkir diangkat.

Daftar lengkap spesifikasi yang belum/sebagian selesai (19 butir): `24_supporting_docs/17_spesifikasi_belum_selesai.md`. Butir besarnya:
- pose penyangga piring;
- kontur lengan;
- hero asset;
- preset cahaya;
- arah hadap tokoh duduk mengikuti dudukan;
- jalan otomatis menghadap tujuan;
- keterlihatan aksi berbasis proyeksi;
- kepala tumpang-tindih pada serah-terima dekat;
- jangkauan IK 2D yang bergantung kamera;
- validasi `musik.suasana`;
- uji kedip pra-render;
- sisa pasangan sebidang.

**Masalah visual yang lolos validator** (15 butir): `24_supporting_docs/18_masalah_visual_lolos_validator.md`. Contoh:
- kepala Wulan menutupi wajah Harjo di two-shot serah-terima;
- cekung sendok tertutup tangan saat kontak (f234);
- piring tanpa jari di bawahnya;
- dinding interior polos;
- meja gerobak kini tampak stainless kusam;
- kaki duduk Harjo sederhana;
- rambut panjang Wulan terbaca sebagai massa gelap;
- siklus suapan terakhir benchmark lebih cepat (35 frame).

## 11. Keterbatasan arsitektur yang tersisa

1. **Presentasi bergantung kamera.** Tokoh 2D adalah billboard yang menghadap kamera tiap shot, dan benda yang dipegang mengikuti tangan 2D. Akibatnya posisi dunia benda **berubah di setiap potongan kamera**:
   - benchmark piring: 0,0017–0,46 m;
   - uji ke-3 piring: 1,22 m di f61;
   - generalisasi gelas: ≤ 0,20 m.

   Di dalam satu shot posisinya kontinu (`temporal:lompatan_benda` PASS) dan kontak tangan 0 px. Lompatan antar-shot hanya **dicatat**, tanpa ambang lolos/gagal. Angka 4.1 dan 4.2 hampir sama, karena sifat arsitektur ini tidak diubah di 4.2.
2. **Jangkauan IK 2D bergantung sudut kamera.** Titik taruh generalisasi harus digeser 14 cm setelah kamera berubah.
3. **Rig chibi:** kepala ~0,5 m dengan jarak serah-terima ~0,45 m, sehingga kepala tumpang-tindih di two-shot dekat.
4. **Format 9:16:** two-shot dengan semua kepala di dalam tepi aman tidak bisa mencapai okupansi minimum, sehingga WARN `komposisi_pita` bersifat struktural.
5. **Perbedaan GPU:** hasil pantulan dan kedip berbeda antara GPU lokal dan Colab. QA kedip yang pasti hanya dari video Colab penuh; tidak ada klip uji pra-render wajib.
6. **Build ID = source hash:** benar untuk provenance, tetapi membuat setiap perbaikan kecil di akhir fase mahal (render ulang semua cerita).

## 12. Kinerja render & penggunaan sumber daya aktual

| Render final | GPU | Kecepatan | Waktu dinding (log) |
|---|---|---|---|
| Benchmark P4-486e18fc49, 860 frame | Colab G4 | ±1,9 dtk/frame | 28,5 menit (termasuk unggah, audio, perakitan) |
| Uji ke-3 P4-b1767c3b5e, 750 frame | Colab G4 | ±1,4 dtk/frame | 18,5 menit |
| Generalisasi P4-2d0645d14d, 616 frame | Colab A100 | ±3 dtk/frame stabil (rata-rata 4,3 termasuk potongan pertama yang timeout 240 dtk) | 47,4 menit (termasuk menunggu GPU) |

- **Bangun adegan lokal:** benchmark 175,9 dtk, generalisasi 23,2 dtk, uji ke-3 106,8 dtk.
- **Still lokal:** ±24 dtk/frame (GPU laptop).
- **Compute unit Colab pada hari Gate E:** 131,64 → 80,42 CU, total **±51,2 CU**. Jumlah ini termasuk:
  - render ulang yang dibuang (§7a laporan teknis): benchmark P4-555dd710c7, P4-71837de932, P4-d61be635aa (240/860); generalisasi P4-da5e095e8a, P4-92a110fd6f; uji ke-3 P4-3b9aa5db79, P4-888954b55c;
  - satu VM G4 yatim (alokasi terlambat tanpa nama sesi) yang dilepas;
  - satu sesi G4 yang dipangkas server Colab di tengah unggahan.
- **Tarif G4:** ±11,2 CU/jam.
- **Video yang dibuang:** satu render ulang penuh ketiga cerita terjadi karena perbaikan kedip (pantulan, z-fighting), dan satu karena validasi musik yang belum ada di engine.

## 13. Hasil generalisasi ketiga cerita

Rincian: `22_generalization_evidence.md`.

| | Benchmark | Generalisasi | Cerita ke-3 |
|---|---|---|---|
| Lingkungan | `jalan_kota` malam, habis hujan | `dalam_rumah` siang | `gang_kampung` senja |
| Tokoh | Darto, Jali | Sri (hijab, duduk), Dimas (anak) | Harjo (tua, peci, kumis, kulit gelap), Wulan (rambut panjang) — **baru** |
| Primitif | masak (sutil), pegang piring, makan (sendok), taruh | ambil, bawa, serah-terima, duduk, minum, taruh | makan, pegang piring, taruh sendok, ambil, jalan sambil membawa, serah-terima, minum |
| Validator | 0 FAIL | 0 FAIL, 1 WARN | 0 FAIL, 2 WARN |
| Video QA | 0 FAIL, kedip WARN | 0 FAIL | 0 FAIL, 2 WARN |

- **Fungsional:** satu source hash, tanpa kondisi khusus cerita, primitif interaksi yang sama, dan 0 FAIL di ketiga cerita.
- **Artistik:**
  - konsistensi kualitas antar-cerita **tidak dinilai oleh pembuat**;
  - interior generalisasi sudah dibangun ulang, tetapi masih lebih polos daripada benchmark;
  - cerita ke-3 memakai set luar yang ada tanpa art direction khusus.

## 14. Isi paket & cara membaca

Lihat `00_README.md`.
