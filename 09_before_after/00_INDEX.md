# Bukti visual sebelum/sesudah (Phase 4.1 → 4.2)

Setiap lembar memuat label kondisi. **Build 4.1 dan 4.2 berbeda di banyak variabel sekaligus** (kamera/komposisi, interior, interaksi, material). Tidak ada lembar A/B satu-variabel; perbandingan ini bukan bukti kausal satu perubahan.

- Lembar `NN_*.jpg` (baru): kolom/baris memakai still lokal ter-grading (pipeline `make.py --frame` yang sama untuk 4.1 dan 4.2) atau frame dari video final kedua versi; sumbernya tertulis di setiap lembar.
- `NN_lembar_lama__04x_*.jpg`: lembar yang sudah dibuat selama Phase 4.2 (judul/label di dalam lembar).
- Still full-resolution 4.2 ada di `06/07/08_stills_*` (raw + graded). Still full-resolution 4.1 yang dipakai: `_sumber_phase41/`.
- **Solid/debug view 4.2: TIDAK TERSEDIA** (tidak dirender di 4.2; tidak diganti dengan solid view 4.1). Solid view 4.1 disertakan hanya sebagai `14_phase41_03_solid_view.jpg` berlabel 4.1.

| # | Topik | Status 4.2 | File |
|---|---|---|---|
| 1 | Genggam sutil anatomis & pergelangan | COMPLETE (numerik); visual: reviewer | `01_lembar_lama__04a_sutil_genggam_sebelum_sesudah.jpg`, `01_sutil_genggam_pergelangan.jpg` |
| 2 | Bahu–siku–pergelangan–lengan bawah | NOT_IMPLEMENTED (tidak ada perubahan di 4.2) | `02_bahu_siku_pergelangan_lengan.jpg` |
| 3 | Penyangga piring alami | PARTIAL (pose 'support' belum dibuat) | `03_penyangga_piring.jpg` |
| 4 | Kontak sendok–mulut | COMPLETE (numerik); visual: tangan menutupi cekung | `04_lembar_lama__04b_sendok_mulut_sebelum_sesudah.jpg`, `04_sendok_ke_mulut.jpg` |
| 5 | Fase makan & minum | COMPLETE | `05_fase_makan.jpg`, `05_fase_minum.jpg` |
| 6 | Serah-terima gelas sadar-tabrakan | COMPLETE dengan WARN (titik 'mepet' 6,2 cm dari meja) | `06_serah_terima_gelas.jpg`, `06b_serah_terima_uji3.jpg` |
| 7 | Anatomi duduk | PARTIAL (pivot lutut + celah dudukan; bentuk kaki belum diperhalus) | `07_anatomi_duduk.jpg`, `07_lembar_lama__04d_kaki_duduk_bangku_sebelum_sesudah.jpg` |
| 8 | Mask wajah (blush Sri) | COMPLETE | `08_lembar_lama__04c_blush_mask_kulit_sebelum_sesudah.jpg`, `08_mask_wajah_blush_sri.jpg` |
| 9 | Siluet & transisi profil | NOT_IMPLEMENTED (tidak ada pekerjaan baru di 4.2) | `09_siluet_transisi_profil.jpg`, `09b_tokoh_cerita_ketiga.jpg` |
| 10 | Establishing & penutup | COMPLETE dengan WARN (komposisi_pita) | `10_establishing_penutup_benchmark.jpg`, `10_establishing_penutup_generalisasi.jpg` |
| 11 | Interior | PARTIAL (art direction sebagian) | `11_interior.jpg` |
| 12 | Hero asset | NOT_IMPLEMENTED (aset 4.1 dipakai) | `12_hero_asset_makanan_alat_masak.jpg` |
| 13 | Cahaya & kedalaman atmosfer | PARTIAL; PARTIAL (preset lama; tidak ada preset baru) | `13_cahaya_kedalaman_benchmark.jpg`, `13_cahaya_kedalaman_generalisasi.jpg` |
| 14 | Raw vs graded | bukti (tidak ada perubahan grading di 4.2) | `14_phase41_01_final_render.jpg`, `14_phase41_02_raw_render.jpg`, `14_phase41_03_solid_view.jpg`, `14_raw_vs_graded.jpg` |
| 15 | Kedip & black crush | lihat 14_post_render_QA.json | `15_kedip_f463-467_benchmark.jpg`, `15_lembar_lama__04f_kedip_meja_gerobak_sebelum_sesudah.jpg`, `15_lembar_lama__04g_kedip_jendela_zfighting_sebelum_sesudah.jpg` |
