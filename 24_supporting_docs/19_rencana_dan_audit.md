# Phase 4.2 — Production Quality Gate & Cross-Story Refinement: audit dan rencana

## Basis

- Build Phase 4.1: P4-4b69684991 (benchmark) dan P4-21e3aadc90 (generalisasi).
- Checkpoint source: `backups/phase41_final_P4-4b69684991_20261127_1031.tar.gz`.
  - SHA-256 arsip: `1583201f2b67a00443451b6e96e35aa33a6f7c9f14052af7cc4a9b6141d8f4ac`.
  - Source hash build: `87e80bde…`.
- Proyek bukan repo git. `git init` tidak dilakukan tanpa izin, jadi checkpoint = arsip.
- Skor reviewer (statis): benchmark 7,18; generalisasi 5,60. Target ≥ 8,25. Arsitektur dipertahankan.

## Audit temuan reviewer vs kode (akar masalah)

| Temuan | File / fungsi | Akar masalah (terverifikasi di kode) |
|---|---|---|
| P0.1 genggam terbalik | `bl_interact.Director._grip_ik` | Bila `\|th+180−φ0\|+25 < \|th−φ0\|`, target `th` **diganti** `th+180` dan `ori_err` dihitung terhadap target yang sudah dibalik. Skor orientasi jadi ~0° padahal ujung alat keluar di sisi kelingking. Penaltinya hanya 12 di `_solve_dof.cost_sol`. 140 frame sutil dan 178 frame sendok memakai jalur ini. |
| P0.2 piring | `Director._present`, `_plate_c`, `Body.block_shift` | Skala piring dilarang (Phase 4.1, benar). Penggantinya geser sepanjang sinar kamera dengan jarak **tak berbatas** (`p.shift_log` dicatat, tidak dibatasi). Pose piring = genggam jepit di tepi (`dof=("rim", …)`). Sprite tangan `pinch` tidak memperlihatkan jari di bawah piring. |
| P0.3 makan / f240 / f245–253 | `Director.pose("spoon_eat")` | Titik mulut = `body.at(fwd_m, …, mp[1])`, yaitu y kanvas mulut tetap pada bidang badan. Tidak ikut **pose kepala** (angguk/miring/bob kepala dari `_write` dan rig). Kontak dinilai antara tangan dan gagang, bukan cekung sendok dan mulut. Fase makan hanya satu kurva `eat_s` (angkat → mulut → turun), tanpa fase sendok/kunyah/istirahat eksplisit. |
| P0.4 serah-terima | `_solve_handovers`, `_handover_search` | Kandidat dinilai dari residual jangkauan saja, tanpa uji tabrakan dunia (meja/benda) dan tanpa validasi lintasan. 74,8° Sri f500–501 berasal dari pose `drink`, bukan serah-terima: titik gelas berpindah cabang siku di awal minum (cabang IK berganti, pergelangan dikompensasi). |
| Blush meluber (Sri f420/f475) | `chars.face` / `face_profile`, `rig2d` lapisan `wajah*` | Blush digambar elips di posisi tetap pada lapisan wajah **tanpa mask kulit**. Pada kepala hijab (oval wajah lebih kecil), elips melewati batas kulit. |
| Komposisi (generalisasi) | `bl_camsolve.solve` → `comp()`; `plan.camera_shot` | Solver menilai keterlihatan/halangan, pita subtitle, dan ruang depan, tetapi tidak menilai okupansi subjek, headroom, ruang kosong lantai/plafon, atau keterlihatan aksi tangan/benda. Establishing/penutup interior memakai jarak tetap terhadap ukuran ruang → plafon/lantai kosong. |
| Interior lemah | `engine/sets/dalam_rumah.py` (104 baris) | Ruang kotak dengan perabot acak sedikit, palet tidak terarah, tanpa detail arsitektur (kusen, plafon, lis, stop kontak), tanpa zona fokus di sekitar interaksi. |
| Flicker f215 / f466; crush f214 | `bl_rig.held_prop` (sutil), `kit.gerobak_makan` (`B.noise(fl.data,"energy",0,25,2)`), grading per shot | f215: kilap bilah logam. f466: noise energi api kompor 60±25 W setiap ±2 frame (hipotesis; diuji dengan render A/B). f214: grading menekan bayangan (kurva/vignette). |
| Provenance | `provenance.validate` | `config_hash` dicatat tetapi tidak divalidasi terhadap build. `checksum_adegan_sama` = NOT_TESTED bila manifest tanpa hash → status keseluruhan bisa PASS. Potongan tumpang-tindih dipilih "terbaru" tanpa dicatat. Pemulihan manual hanya ada di teks catatan. |

## Rencana per gerbang (urutan pengerjaan)

### Gerbang A — interaksi fisik (P0)

1. **A1 orientasi anatomis bertanda**
   - Profil genggam mendapat `sisi_ujung` (default utensil: `["ibu_jari"]`).
   - Pembalikan hanya boleh bila profil menyatakannya sebagai varian genggam (mis. `kelingking`).
   - `_grip_ik` selalu mengukur galat terhadap orientasi anatomis yang dimaksud. Varian dicatat per frame.
   - Bila tidak ada solusi anatomis dalam batas pergelangan: solver menggeser pose/blocking (arah gagang, jarak badan, sisi tubuh). Bila tetap gagal: WARN/FAIL eksplisit.
2. **A2 piring**
   - Geser presentasi dibatasi (`presentasi.geser_maks`), dicatat terpisah dan divalidasi.
   - Pose penyangga piring: telapak/jari di bawah piring, ibu jari di tepi atas. Ini butuh lapisan tangan baru `support` di rig2d (umum untuk benda datar/piring/nampan).
   - Kontak konsisten antar-potongan kamera.
3. **A3 primitif makan/minum**
   - Fase eksplisit: sendok/ambil → angkat → dekati mulut → kontak → kunyah/teguk → kembali → istirahat.
   - Target mulut = titik semantik yang ditransformasikan melalui pose kepala (pivot kepala, angguk, tampak).
   - Validasi cekung sendok/bibir gelas ↔ mulut (relatif ukuran benda).
4. **A4 serah-terima sadar-tabrakan**
   - Proxy tabrakan sederhana (kotak bbox objek dunia statis).
   - Kandidat titik dan lintasan raih diuji terhadap proxy.
   - Validasi kontinuitas cabang siku dan batas pergelangan di fase kontak.
   - Diuji pada ≥ 2 tata letak tanpa kode khusus cerita.

### Gerbang B — kualitas visual tokoh (P0)

- **Mask kulit per tampak:** blush dan lapisan khusus kulit dipotong oleh area kulit kepala tampak yang sama (di generator sprite).
- **Kontur lengan:** bahu/siku/pergelangan dan sambungan tangan–lengan bawah; pose tangan per kelas genggam.
- **Siluet kaki duduk** dan postur.
- **Variasi siluet tokoh** lewat parameter spesifikasi tokoh yang sudah ada.

### Gerbang C — kamera, lingkungan, cahaya (P1)

- **Kamera:** komposisi di `bl_camsolve` (okupansi, headroom, ruang depan, keterlihatan aksi, kesatuan multi-tokoh, ruang kosong bermakna). Fokus pada aksi utama. Establishing/penutup interior dihitung dari isi aksi, bukan ukuran ruang. Override deklaratif di story.yaml.
- **Interior rumah Indonesia:** denah ruang tamu yang masuk akal, proporsi perabot, palet terarah, detail arsitektur, zona fokus interaksi. Hero asset benchmark: nasi goreng, sutil, piring, gelas, alat masak, gerobak (tier kualitas sesuai ukuran layar).
- **Cahaya:** preset interior/eksterior (key/fill/rim, hangat/dingin, kedalaman) dan detail bayangan. Investigasi flicker f215/f466 dan crush f214.

### Gerbang D — generalisasi lintas cerita

- Cerita ketiga kecil di lingkungan luar yang sudah ada (mis. `gang_kampung`), dengan tokoh berbeda dan primitif interaksi yang sama.
- Ketiga cerita dibangun dari source yang sama, tanpa kondisi berdasarkan ID cerita/nama tokoh.

### Gerbang E — penerimaan produksi

- Render final hanya setelah A–D lolos.
- QA render, provenance (dengan config hash dan peristiwa pemulihan), dan paket review berupa file individual.

## Kriteria penerimaan teknis (bukan skor artistik)

| Aspek | Kriteria |
|---|---|
| Genggam terbalik tanpa izin profil | 0 frame (FAIL bila > 0) |
| Galat orientasi anatomis utensil | ≤ 10° p95 |
| Pergelangan di fase kontak | ≤ 45°; maks ≤ 60° |
| Cekung sendok ↔ mulut saat kontak | ≤ 0,25 × lebar cekung (relatif ukuran benda) |
| Geser presentasi piring | ≤ `geser_maks` profil (awal 0,06 m) |
| Benda dipegang vs proxy dunia | tembus ≤ 0,5 cm; titik serah bebas tabrakan |
| Lapisan khusus kulit di luar kulit | 0 piksel (uji generator) |
| Komposisi | okupansi subjek, headroom, dan ruang kosong dalam rentang per tipe shot (WARN di luar) |
| Provenance | config hash cocok; metadata identitas kritis hilang → FAIL, bukan PASS |

## Risiko

- Lapisan tangan `support` baru menuntut versi karakter naik (cache `chars.VERSION`), sehingga semua tokoh dibangun ulang.
- Larangan pembalikan bisa membuat sebagian frame sutil/sendok tanpa solusi anatomis. Solver harus mengubah pose (arah gagang/jarak), dan sisanya dilaporkan.
- Interior dan cerita ketiga menambah waktu render. Iterasi memakai still dan klip pendek. Video penuh hanya di akhir (Colab, GPU G4/L4/A100).

## Rekomendasi reviewer yang disesuaikan

- **"Fingers beneath the plate":** pada sprite 2D satu lapis tangan, jari di bawah piring hanya terlihat dari sudut kamera di bawah tepi piring. Solusinya lapisan tangan `support` (telapak di bawah, ibu jari di atas tepi) yang dipilih saat kamera melihat dari atas/sejajar. Bukan deformasi bebas.
- **"Proxy tabrakan":** dipakai kotak terarah (OBB) per objek dunia statis yang dekat interaksi, bukan mesh penuh. Cukup untuk meja/gerobak/kursi dan murah.
