# Paket Review Independen — Phase 4.2

Blender Hybrid 2D–3D Animation Production Engine: **Production Quality Gate & Cross-Story Refinement**.

- **Isi:** hasil Phase 4.2 yang **sudah selesai**. Tidak ada pengembangan Phase 4.3, tidak ada perbaikan tambahan, dan tidak ada render ulang adegan untuk paket ini.
- **Pembuat tidak memberi skor artistik.** Target penerimaan independen tetap ≥ 8,25/10.
- **Tidak ada ZIP:** semua file bisa diakses langsung satu per satu.
- **Ukuran file:** beberapa file adalah *hard link* ke artefak build asli, jadi isinya identik byte-per-byte dengan file sumbernya (SHA-256 di `99_CHECKSUMS.json`).

## Identitas artefak

| Cerita | Build ID | Frame | Video final |
|---|---|---|---|
| Satu Bungkus Lagi (benchmark) | **P4-486e18fc49** | 860 | `01_benchmark_phase42_P4-486e18fc49.mp4` |
| Teh Sore untuk Ibu (generalisasi) | **P4-2d0645d14d** | 616 | `02_generalization_phase42_P4-2d0645d14d.mp4` |
| Kopi Sore di Gang (cerita ke-3, baru) | **P4-b1767c3b5e** | 750 | `03_third_story_phase42_P4-b1767c3b5e.mp4` |

- **Source hash bersama:** `f7ccb35625ca892f68798b6b10541e6810d9a769c139a10ab073e7e045631c8c`. Dihitung ulang saat paket dibuat dan cocok dengan ketiga manifest.
- **Pembanding Phase 4.1:** P4-4b69684991 (benchmark) dan P4-21e3aadc90 (generalisasi).
- **Video:** 1080×1920, 30 fps, AAC 48 kHz. Build ID juga tertulis di metadata `comment` setiap video.
- **Render:** EEVEE (Blender 4.5.16) di GPU Colab G4/A100. Provenance per frame PASS (checksum setiap frame terverifikasi terhadap metadata potongan render).

## Urutan review yang disarankan

1. `00_PHASE42_COMPLETION_REPORT.md`: ringkasan, matriks kepatuhan, gerbang A–E, peringatan yang tersisa.
2. `23_reviewer_findings_matrix.md`: setiap temuan review 4.1, dengan status akhir dan bukti.
3. Video final `01`, `02`, `03` (dengan audio).
4. `04_comparison_phase41_vs_phase42_*.mp4`: 4.1 (kiri) vs 4.2 (kanan), sinkron per frame, audio 4.2.
5. `05_interaction_diagnostic_*.mp4` + `05_interaction_diagnostic_INDEX.md`: cuplikan interaksi kritis dengan nomor frame dan anotasi fase per frame.
6. `09_before_after/00_INDEX.md` + lembar `*.jpg`: 15 topik sebelum/sesudah.
7. Still full-resolution: `06_stills_benchmark/`, `07_stills_generalization/`, `08_stills_third_story/` (masing-masing punya `00_INDEX.md`).
8. `22_generalization_evidence.md`.
9. Bukti teknis `10`–`21`, lalu dokumen pendukung `24_supporting_docs/`.

## Struktur folder

| Path | Isi |
|---|---|
| `00_PHASE42_COMPLETION_REPORT.md` | Laporan penyelesaian (A) |
| `01_benchmark_phase42_<build>.mp4` / `02_generalization_…` / `03_third_story_…` | Video final (B) |
| `04_comparison_phase41_vs_phase42_<build>_<build>.mp4` | 2160×1920 berdampingan (sisi kiri/kanan masing-masing 1080×1920 asli). Bagian 1: benchmark (860 frame), bagian 2: generalisasi (616 frame). Cerita ke-3 tidak punya versi 4.1. |
| `05_interaction_diagnostic_<builds>.mp4` + `_INDEX.md` | 11 segmen, 723 frame, audio segmen asli (B) |
| `06/07/08_stills_*/raw/` | PNG mentah dari render final Colab (frame yang sama dengan video) |
| `06/07/08_stills_*/graded/` | Grading video yang sama diterapkan ke PNG mentah. Tanpa subtitle, grain, dan fade. Metadata PNG: build ID, shot, filter, SHA-256 mentah. |
| `06/07/08_stills_*/00_INDEX.md` | Daftar frame, shot, alasan pemilihan, fase mulut, dan pemetaan frame 4.1 → 4.2 (C) |
| `09_before_after/` | Lembar sebelum/sesudah 15 topik, termasuk lembar lama yang dibuat selama 4.2, still 4.1 sumber (`_sumber_phase41/`), dan raw/graded/solid 4.1 (`14_phase41_*`) (D) |
| `10_source_code.txt` | Source lengkap dengan batas file, SHA-256 per file, source hash, dan tools hash (E) |
| `11_configuration.txt` | `story.yaml` ketiga cerita, manifest inputs, setelan render, daftar shot, koreksi grading per shot, diff `story.yaml` 4.1 → 4.2 |
| `12_validation_results.json` | Validator interaksi + kamera + z-fighting per cerita (build final); validator 4.1 sebagai pembanding |
| `13_regression_tests.json` | Hasil regresi 89/89 + log uji unit 36 tes |
| `14_post_render_QA.json` | `qa_render` + `qa_kedip` pada video final; QA 4.1 sebagai pembanding |
| `15_build_provenance.json` | Provenance per frame/potongan, checksum video, scene build, daftar build yang dibuang |
| `16_build_manifests/` | Manifest build final per cerita |
| `17_interaction_reports/` | `interaksi.json` lengkap (per frame: residual, orientasi, pergelangan, fase, kontak, transisi) + validator interaksi |
| `18_camera_composition/` | `kamera.json` (komposisi awal/akhir per kunci kamera, koreksi lensa/dolly/bidik) + validator kamera |
| `19_collision_semantic_contact/` | Tabrakan dunia (proxy OBB), kontak permukaan ambil/letak, kontak cekung/bibir ↔ mulut, serah-terima, pasangan sebidang |
| `20_presentation_transform/` | Skala, geser presentasi, lompatan posisi benda di potongan kamera (4.1 vs 4.2), transisi kepemilikan |
| `21_scene_packed/` | `scene.blend` final dengan semua gambar eksternal di-*pack* (salinan; file build asli tidak diubah, SHA-256 diverifikasi sebelum dan sesudah) |
| `22_generalization_evidence.md` | Bukti generalisasi (F) |
| `23_reviewer_findings_matrix.md` | Matriks temuan reviewer (G) |
| `24_supporting_docs/` | Laporan teknis rinci, daftar spesifikasi belum selesai (19), masalah visual yang lolos validator (15), rencana & audit, log uji unit, log render Colab |
| `_alat/bangun_paket_review.py` | Skrip yang merakit paket ini (dapat dijalankan ulang; tidak mengubah build) |
| `99_CHECKSUMS.json` | SHA-256 dan ukuran setiap file |

## Bukti yang TIDAK tersedia

Bukti yang tidak ada ditandai, bukan diganti dengan bukti build lama.

- **Solid/debug view Phase 4.2:** tidak dirender di 4.2. Solid view 4.1 hanya disertakan dengan label 4.1.
- **Before/after A/B satu-variabel:** build 4.1 dan 4.2 berbeda di banyak variabel sekaligus. Setiap lembar diberi label kondisi.
- **Pembanding 4.1 untuk cerita ke-3:** cerita baru, jadi tidak ada versinya di 4.1.
- **Lip-sync perseptual:** NOT_TESTED (butuh penilaian manusia).
- **Fase `sendok` (menyendok) pada siklus suapan yang terlihat di shot makan benchmark:** jatuh di shot 4 (insert wajan), sehingga tidak terlihat di layar.

## Catatan pembacaan

- **Pemetaan frame benchmark:** batas shot 4.1 dan 4.2 identik, jadi frame acuan review 4.1 (60…760) menunjuk ke shot yang sama. Waktu aksi di dalam shot bisa berbeda: kontak suapan di shot 5 kini f233–235, dan f240 berada di fase `kembali`. Detailnya di `06_stills_benchmark/00_INDEX.md`.
- **Frame potongan kamera:** di video perbandingan, posisi benda yang dipegang dapat melompat di frame potongan. Ini keterbatasan arsitektur yang dicatat di `20_presentation_transform/` dan laporan §11.
- **Path lokal:** log dan JSON memuat path lokal mesin pembuat (`/home/…`). Path ini tidak memengaruhi isi bukti.
