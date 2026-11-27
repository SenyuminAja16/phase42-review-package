# review_optimized — salinan ramah-akses untuk reviewer

Folder ini **hanya berisi salinan turunan** agar dapat dibuka lewat integrasi GitHub (batas praktis ~1 MB per file). **Semua file di sini < 800 KB.** Artefak asli di root repo dan video di Release `phase42-final` **tidak diubah, diganti, atau dihapus**. Tidak ada render ulang; engine tidak disentuh. Bila ada keraguan kualitas, file asli yang berlaku.

- Jumlah file turunan: 244; file ≥ 800 KB: 0.
- Pemetaan lengkap mesin-baca (file turunan → file asli, SHA-256 asli, frame, shot, build ID, kualitas JPEG, resolusi): `index.json`.
- Skrip pembuat: `_alat/optimasi.py` (dapat dijalankan ulang).

## Isi

| Folder | Isi | Jumlah |
|---|---|---|
| `stills_jpg/benchmark/`, `generalization/`, `third_story/` | Still **graded** (render final Colab + grading video, tanpa subtitle) → JPEG resolusi asli 1080×1920 | 131 |
| `stills_jpg/phase41_reference/` | Still Phase 4.1 yang dipakai lembar before–after (build 4.1, berlabel) | 27 |
| `before_after_jpg/` | Semua lembar before–after; yang sudah < 800 KB disalin apa adanya | 29 |
| `provenance_split/` | `15_build_provenance.json` dipecah per cerita: laporan provenance, video & scene, frame per 150 | 23 |
| `contact_sheets/` | Lembar kontak berurutan video final (tiap 5 frame) dan video diagnostik (tiap 3 frame), dengan nomor frame & timecode | 34 |

Catatan:
- Still **raw** (PNG mentah) tidak dikonversi; aslinya di `0X_stills_*/raw/`. Kolom `asli_raw` di tabel menunjuk ke file raw dengan frame yang sama (kosong untuk 4 frame cerita ke-3 yang hanya dibuat graded untuk lembar 06b/09b).
- `provenance_split/`: menggabungkan kembali semua potongan menghasilkan JSON **identik** dengan `15_build_provenance.json` (diverifikasi skrip).
- Lembar kontak diagnostik: label kuning = frame & timecode **video diagnostik**; label abu = cerita dan **frame asli cerita** (lihat `05_interaction_diagnostic_INDEX.md`).
- File `.blend` di `21_scene_packed/` (17–48 MB) tidak dapat diperkecil tanpa mengubah isinya; tidak disertakan di sini.

## Still graded

| File JPEG | Asli PNG | Cerita | Build | Frame | Shot | Kualitas | Resolusi | KB |
|---|---|---|---|---|---|---|---|---|
| `stills_jpg/benchmark/f0007_s01_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0007_s01_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 7 | 1 | q92 | 1080×1920 | 423 |
| `stills_jpg/benchmark/f0037_s01_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0037_s01_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 37 | 1 | q92 | 1080×1920 | 465 |
| `stills_jpg/benchmark/f0060_s01_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0060_s01_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 60 | 1 | q92 | 1080×1920 | 503 |
| `stills_jpg/benchmark/f0068_s01_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0068_s01_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 68 | 1 | q92 | 1080×1920 | 511 |
| `stills_jpg/benchmark/f0081_s02_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0081_s02_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 81 | 2 | q92 | 1080×1920 | 503 |
| `stills_jpg/benchmark/f0104_s02_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0104_s02_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 104 | 2 | q92 | 1080×1920 | 504 |
| `stills_jpg/benchmark/f0116_s02_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0116_s02_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 116 | 2 | q92 | 1080×1920 | 504 |
| `stills_jpg/benchmark/f0120_s02_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0120_s02_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 120 | 2 | q92 | 1080×1920 | 505 |
| `stills_jpg/benchmark/f0149_s02_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0149_s02_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 149 | 2 | q92 | 1080×1920 | 505 |
| `stills_jpg/benchmark/f0152_s02_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0152_s02_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 152 | 2 | q92 | 1080×1920 | 505 |
| `stills_jpg/benchmark/f0165_s03_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0165_s03_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 165 | 3 | q92 | 1080×1920 | 345 |
| `stills_jpg/benchmark/f0178_s03_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0178_s03_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 178 | 3 | q92 | 1080×1920 | 338 |
| `stills_jpg/benchmark/f0180_s03_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0180_s03_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 180 | 3 | q92 | 1080×1920 | 336 |
| `stills_jpg/benchmark/f0192_s03_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0192_s03_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 192 | 3 | q92 | 1080×1920 | 338 |
| `stills_jpg/benchmark/f0194_s03_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0194_s03_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 194 | 3 | q92 | 1080×1920 | 338 |
| `stills_jpg/benchmark/f0205_s04_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0205_s04_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 205 | 4 | q92 | 1080×1920 | 265 |
| `stills_jpg/benchmark/f0212_s04_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0212_s04_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 212 | 4 | q92 | 1080×1920 | 269 |
| `stills_jpg/benchmark/f0219_s04_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0219_s04_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 219 | 4 | q92 | 1080×1920 | 274 |
| `stills_jpg/benchmark/f0222_s04_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0222_s04_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 222 | 4 | q92 | 1080×1920 | 277 |
| `stills_jpg/benchmark/f0232_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0232_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 232 | 5 | q92 | 1080×1920 | 349 |
| `stills_jpg/benchmark/f0234_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0234_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 234 | 5 | q92 | 1080×1920 | 351 |
| `stills_jpg/benchmark/f0240_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0240_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 240 | 5 | q92 | 1080×1920 | 350 |
| `stills_jpg/benchmark/f0250_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0250_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 250 | 5 | q92 | 1080×1920 | 347 |
| `stills_jpg/benchmark/f0253_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0253_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 253 | 5 | q92 | 1080×1920 | 345 |
| `stills_jpg/benchmark/f0254_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0254_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 254 | 5 | q92 | 1080×1920 | 345 |
| `stills_jpg/benchmark/f0268_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0268_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 268 | 5 | q92 | 1080×1920 | 343 |
| `stills_jpg/benchmark/f0275_s05_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0275_s05_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 275 | 5 | q92 | 1080×1920 | 340 |
| `stills_jpg/benchmark/f0282_s06_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0282_s06_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 282 | 6 | q92 | 1080×1920 | 324 |
| `stills_jpg/benchmark/f0288_s06_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0288_s06_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 288 | 6 | q92 | 1080×1920 | 323 |
| `stills_jpg/benchmark/f0330_s06_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0330_s06_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 330 | 6 | q92 | 1080×1920 | 323 |
| `stills_jpg/benchmark/f0369_s06_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0369_s06_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 369 | 6 | q92 | 1080×1920 | 321 |
| `stills_jpg/benchmark/f0380_s06_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0380_s06_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 380 | 6 | q92 | 1080×1920 | 322 |
| `stills_jpg/benchmark/f0451_s06_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0451_s06_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 451 | 6 | q92 | 1080×1920 | 314 |
| `stills_jpg/benchmark/f0458_s07_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0458_s07_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 458 | 7 | q92 | 1080×1920 | 399 |
| `stills_jpg/benchmark/f0464_s07_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0464_s07_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 464 | 7 | q92 | 1080×1920 | 398 |
| `stills_jpg/benchmark/f0465_s07_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0465_s07_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 465 | 7 | q92 | 1080×1920 | 396 |
| `stills_jpg/benchmark/f0478_s07_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0478_s07_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 478 | 7 | q92 | 1080×1920 | 397 |
| `stills_jpg/benchmark/f0499_s07_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0499_s07_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 499 | 7 | q92 | 1080×1920 | 387 |
| `stills_jpg/benchmark/f0500_s07_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0500_s07_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 500 | 7 | q92 | 1080×1920 | 386 |
| `stills_jpg/benchmark/f0534_s07_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0534_s07_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 534 | 7 | q92 | 1080×1920 | 377 |
| `stills_jpg/benchmark/f0547_s08_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0547_s08_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 547 | 8 | q92 | 1080×1920 | 312 |
| `stills_jpg/benchmark/f0576_s08_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0576_s08_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 576 | 8 | q92 | 1080×1920 | 309 |
| `stills_jpg/benchmark/f0580_s08_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0580_s08_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 580 | 8 | q92 | 1080×1920 | 309 |
| `stills_jpg/benchmark/f0605_s08_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0605_s08_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 605 | 8 | q92 | 1080×1920 | 314 |
| `stills_jpg/benchmark/f0615_s09_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0615_s09_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 615 | 9 | q92 | 1080×1920 | 328 |
| `stills_jpg/benchmark/f0618_s09_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0618_s09_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 618 | 9 | q92 | 1080×1920 | 325 |
| `stills_jpg/benchmark/f0657_s09_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0657_s09_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 657 | 9 | q92 | 1080×1920 | 323 |
| `stills_jpg/benchmark/f0696_s09_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0696_s09_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 696 | 9 | q92 | 1080×1920 | 315 |
| `stills_jpg/benchmark/f0700_s09_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0700_s09_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 700 | 9 | q92 | 1080×1920 | 316 |
| `stills_jpg/benchmark/f0709_s10_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0709_s10_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 709 | 10 | q92 | 1080×1920 | 308 |
| `stills_jpg/benchmark/f0717_s10_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0717_s10_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 717 | 10 | q92 | 1080×1920 | 313 |
| `stills_jpg/benchmark/f0725_s10_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0725_s10_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 725 | 10 | q92 | 1080×1920 | 320 |
| `stills_jpg/benchmark/f0738_s11_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0738_s11_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 738 | 11 | q92 | 1080×1920 | 470 |
| `stills_jpg/benchmark/f0760_s11_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0760_s11_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 760 | 11 | q92 | 1080×1920 | 469 |
| `stills_jpg/benchmark/f0796_s11_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0796_s11_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 796 | 11 | q92 | 1080×1920 | 472 |
| `stills_jpg/benchmark/f0854_s11_P4-486e18fc49_graded.jpg` | `06_stills_benchmark/graded/f0854_s11_P4-486e18fc49_graded.png` | benchmark | P4-486e18fc49 | 854 | 11 | q92 | 1080×1920 | 437 |
| `stills_jpg/generalization/f0007_s01_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0007_s01_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 7 | 1 | q92 | 1080×1920 | 322 |
| `stills_jpg/generalization/f0057_s01_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0057_s01_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 57 | 1 | q92 | 1080×1920 | 318 |
| `stills_jpg/generalization/f0060_s01_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0060_s01_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 60 | 1 | q92 | 1080×1920 | 320 |
| `stills_jpg/generalization/f0108_s01_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0108_s01_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 108 | 1 | q92 | 1080×1920 | 329 |
| `stills_jpg/generalization/f0121_s02_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0121_s02_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 121 | 2 | q92 | 1080×1920 | 320 |
| `stills_jpg/generalization/f0131_s02_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0131_s02_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 131 | 2 | q92 | 1080×1920 | 318 |
| `stills_jpg/generalization/f0135_s02_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0135_s02_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 135 | 2 | q92 | 1080×1920 | 318 |
| `stills_jpg/generalization/f0143_s02_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0143_s02_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 143 | 2 | q92 | 1080×1920 | 317 |
| `stills_jpg/generalization/f0167_s02_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0167_s02_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 167 | 2 | q92 | 1080×1920 | 321 |
| `stills_jpg/generalization/f0200_s02_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0200_s02_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 200 | 2 | q92 | 1080×1920 | 320 |
| `stills_jpg/generalization/f0213_s02_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0213_s02_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 213 | 2 | q92 | 1080×1920 | 320 |
| `stills_jpg/generalization/f0226_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0226_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 226 | 3 | q92 | 1080×1920 | 341 |
| `stills_jpg/generalization/f0292_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0292_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 292 | 3 | q92 | 1080×1920 | 342 |
| `stills_jpg/generalization/f0300_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0300_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 300 | 3 | q92 | 1080×1920 | 342 |
| `stills_jpg/generalization/f0301_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0301_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 301 | 3 | q92 | 1080×1920 | 342 |
| `stills_jpg/generalization/f0310_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0310_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 310 | 3 | q92 | 1080×1920 | 343 |
| `stills_jpg/generalization/f0318_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0318_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 318 | 3 | q92 | 1080×1920 | 346 |
| `stills_jpg/generalization/f0325_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0325_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 325 | 3 | q92 | 1080×1920 | 349 |
| `stills_jpg/generalization/f0330_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0330_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 330 | 3 | q92 | 1080×1920 | 349 |
| `stills_jpg/generalization/f0337_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0337_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 337 | 3 | q92 | 1080×1920 | 350 |
| `stills_jpg/generalization/f0340_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0340_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 340 | 3 | q92 | 1080×1920 | 348 |
| `stills_jpg/generalization/f0359_s03_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0359_s03_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 359 | 3 | q92 | 1080×1920 | 350 |
| `stills_jpg/generalization/f0372_s04_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0372_s04_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 372 | 4 | q92 | 1080×1920 | 254 |
| `stills_jpg/generalization/f0420_s04_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0420_s04_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 420 | 4 | q92 | 1080×1920 | 257 |
| `stills_jpg/generalization/f0424_s04_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0424_s04_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 424 | 4 | q92 | 1080×1920 | 256 |
| `stills_jpg/generalization/f0475_s04_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0475_s04_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 475 | 4 | q92 | 1080×1920 | 251 |
| `stills_jpg/generalization/f0476_s04_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0476_s04_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 476 | 4 | q92 | 1080×1920 | 252 |
| `stills_jpg/generalization/f0489_s05_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0489_s05_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 489 | 5 | q92 | 1080×1920 | 318 |
| `stills_jpg/generalization/f0500_s05_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0500_s05_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 500 | 5 | q92 | 1080×1920 | 317 |
| `stills_jpg/generalization/f0510_s05_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0510_s05_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 510 | 5 | q92 | 1080×1920 | 319 |
| `stills_jpg/generalization/f0513_s05_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0513_s05_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 513 | 5 | q92 | 1080×1920 | 319 |
| `stills_jpg/generalization/f0538_s05_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0538_s05_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 538 | 5 | q92 | 1080×1920 | 324 |
| `stills_jpg/generalization/f0549_s06_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0549_s06_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 549 | 6 | q92 | 1080×1920 | 291 |
| `stills_jpg/generalization/f0551_s06_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0551_s06_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 551 | 6 | q92 | 1080×1920 | 291 |
| `stills_jpg/generalization/f0560_s06_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0560_s06_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 560 | 6 | q92 | 1080×1920 | 290 |
| `stills_jpg/generalization/f0561_s06_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0561_s06_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 561 | 6 | q92 | 1080×1920 | 290 |
| `stills_jpg/generalization/f0580_s06_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0580_s06_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 580 | 6 | q92 | 1080×1920 | 289 |
| `stills_jpg/generalization/f0590_s06_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0590_s06_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 590 | 6 | q92 | 1080×1920 | 288 |
| `stills_jpg/generalization/f0610_s06_P4-2d0645d14d_graded.jpg` | `07_stills_generalization/graded/f0610_s06_P4-2d0645d14d_graded.png` | generalization | P4-2d0645d14d | 610 | 6 | q92 | 1080×1920 | 287 |
| `stills_jpg/third_story/f0007_s01_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0007_s01_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 7 | 1 | q92 | 1080×1920 | 487 |
| `stills_jpg/third_story/f0030_s01_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0030_s01_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 30 | 1 | q92 | 1080×1920 | 459 |
| `stills_jpg/third_story/f0054_s01_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0054_s01_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 54 | 1 | q92 | 1080×1920 | 424 |
| `stills_jpg/third_story/f0067_s02_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0067_s02_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 67 | 2 | q92 | 1080×1920 | 308 |
| `stills_jpg/third_story/f0088_s02_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0088_s02_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 88 | 2 | q92 | 1080×1920 | 307 |
| `stills_jpg/third_story/f0103_s02_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0103_s02_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 103 | 2 | q92 | 1080×1920 | 305 |
| `stills_jpg/third_story/f0118_s02_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0118_s02_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 118 | 2 | q92 | 1080×1920 | 302 |
| `stills_jpg/third_story/f0132_s02_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0132_s02_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 132 | 2 | q92 | 1080×1920 | 300 |
| `stills_jpg/third_story/f0139_s02_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0139_s02_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 139 | 2 | q92 | 1080×1920 | 298 |
| `stills_jpg/third_story/f0141_s02_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0141_s02_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 141 | 2 | q92 | 1080×1920 | 299 |
| `stills_jpg/third_story/f0152_s03_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0152_s03_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 152 | 3 | q92 | 1080×1920 | 374 |
| `stills_jpg/third_story/f0162_s03_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0162_s03_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 162 | 3 | q92 | 1080×1920 | 373 |
| `stills_jpg/third_story/f0165_s03_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0165_s03_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 165 | 3 | q92 | 1080×1920 | 374 |
| `stills_jpg/third_story/f0174_s03_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0174_s03_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 174 | 3 | q92 | 1080×1920 | 374 |
| `stills_jpg/third_story/f0224_s03_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0224_s03_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 224 | 3 | q92 | 1080×1920 | 379 |
| `stills_jpg/third_story/f0250_s03_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0250_s03_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 250 | 3 | q92 | 1080×1920 | 392 |
| `stills_jpg/third_story/f0296_s03_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0296_s03_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 296 | 3 | q92 | 1080×1920 | 397 |
| `stills_jpg/third_story/f0309_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0309_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 309 | 4 | q92 | 1080×1920 | 370 |
| `stills_jpg/third_story/f0372_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0372_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 372 | 4 | q92 | 1080×1920 | 369 |
| `stills_jpg/third_story/f0383_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0383_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 383 | 4 | q92 | 1080×1920 | 369 |
| `stills_jpg/third_story/f0384_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0384_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 384 | 4 | q92 | 1080×1920 | 369 |
| `stills_jpg/third_story/f0398_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0398_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 398 | 4 | q92 | 1080×1920 | 367 |
| `stills_jpg/third_story/f0410_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0410_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 410 | 4 | q92 | 1080×1920 | 367 |
| `stills_jpg/third_story/f0413_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0413_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 413 | 4 | q92 | 1080×1920 | 368 |
| `stills_jpg/third_story/f0435_s04_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0435_s04_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 435 | 4 | q92 | 1080×1920 | 365 |
| `stills_jpg/third_story/f0448_s05_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0448_s05_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 448 | 5 | q92 | 1080×1920 | 273 |
| `stills_jpg/third_story/f0500_s05_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0500_s05_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 500 | 5 | q92 | 1080×1920 | 271 |
| `stills_jpg/third_story/f0523_s05_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0523_s05_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 523 | 5 | q92 | 1080×1920 | 269 |
| `stills_jpg/third_story/f0598_s05_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0598_s05_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 598 | 5 | q92 | 1080×1920 | 262 |
| `stills_jpg/third_story/f0611_s06_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0611_s06_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 611 | 6 | q92 | 1080×1920 | 309 |
| `stills_jpg/third_story/f0640_s06_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0640_s06_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 640 | 6 | q92 | 1080×1920 | 312 |
| `stills_jpg/third_story/f0669_s06_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0669_s06_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 669 | 6 | q92 | 1080×1920 | 316 |
| `stills_jpg/third_story/f0682_s07_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0682_s07_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 682 | 7 | q92 | 1080×1920 | 383 |
| `stills_jpg/third_story/f0700_s07_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0700_s07_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 700 | 7 | q92 | 1080×1920 | 387 |
| `stills_jpg/third_story/f0713_s07_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0713_s07_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 713 | 7 | q92 | 1080×1920 | 389 |
| `stills_jpg/third_story/f0744_s07_P4-b1767c3b5e_graded.jpg` | `08_stills_third_story/graded/f0744_s07_P4-b1767c3b5e_graded.png` | third_story | P4-b1767c3b5e | 744 | 7 | q92 | 1080×1920 | 468 |

## Still Phase 4.1 (referensi)

| File JPEG | Asli PNG | Build | Frame | KB |
|---|---|---|---|---|
| `stills_jpg/phase41_reference/benchmark_f0060_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0060_P4-4b69684991.png` | P4-4b69684991 | 60 | 433 |
| `stills_jpg/phase41_reference/benchmark_f0120_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0120_P4-4b69684991.png` | P4-4b69684991 | 120 | 460 |
| `stills_jpg/phase41_reference/benchmark_f0180_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0180_P4-4b69684991.png` | P4-4b69684991 | 180 | 332 |
| `stills_jpg/phase41_reference/benchmark_f0212_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0212_P4-4b69684991.png` | P4-4b69684991 | 212 | 261 |
| `stills_jpg/phase41_reference/benchmark_f0222_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0222_P4-4b69684991.png` | P4-4b69684991 | 222 | 269 |
| `stills_jpg/phase41_reference/benchmark_f0240_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0240_P4-4b69684991.png` | P4-4b69684991 | 240 | 330 |
| `stills_jpg/phase41_reference/benchmark_f0250_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0250_P4-4b69684991.png` | P4-4b69684991 | 250 | 320 |
| `stills_jpg/phase41_reference/benchmark_f0282_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0282_P4-4b69684991.png` | P4-4b69684991 | 282 | 277 |
| `stills_jpg/phase41_reference/benchmark_f0330_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0330_P4-4b69684991.png` | P4-4b69684991 | 330 | 272 |
| `stills_jpg/phase41_reference/benchmark_f0380_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0380_P4-4b69684991.png` | P4-4b69684991 | 380 | 261 |
| `stills_jpg/phase41_reference/benchmark_f0500_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0500_P4-4b69684991.png` | P4-4b69684991 | 500 | 369 |
| `stills_jpg/phase41_reference/benchmark_f0580_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0580_P4-4b69684991.png` | P4-4b69684991 | 580 | 296 |
| `stills_jpg/phase41_reference/benchmark_f0615_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0615_P4-4b69684991.png` | P4-4b69684991 | 615 | 281 |
| `stills_jpg/phase41_reference/benchmark_f0700_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0700_P4-4b69684991.png` | P4-4b69684991 | 700 | 250 |
| `stills_jpg/phase41_reference/benchmark_f0760_P4-4b69684991.jpg` | `09_before_after/_sumber_phase41/benchmark_f0760_P4-4b69684991.png` | P4-4b69684991 | 760 | 450 |
| `stills_jpg/phase41_reference/generalization_f0060_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0060_P4-21e3aadc90.png` | P4-21e3aadc90 | 60 | 278 |
| `stills_jpg/phase41_reference/generalization_f0135_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0135_P4-21e3aadc90.png` | P4-21e3aadc90 | 135 | 272 |
| `stills_jpg/phase41_reference/generalization_f0200_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0200_P4-21e3aadc90.png` | P4-21e3aadc90 | 200 | 269 |
| `stills_jpg/phase41_reference/generalization_f0300_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0300_P4-21e3aadc90.png` | P4-21e3aadc90 | 300 | 316 |
| `stills_jpg/phase41_reference/generalization_f0318_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0318_P4-21e3aadc90.png` | P4-21e3aadc90 | 318 | 319 |
| `stills_jpg/phase41_reference/generalization_f0325_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0325_P4-21e3aadc90.png` | P4-21e3aadc90 | 325 | 320 |
| `stills_jpg/phase41_reference/generalization_f0330_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0330_P4-21e3aadc90.png` | P4-21e3aadc90 | 330 | 319 |
| `stills_jpg/phase41_reference/generalization_f0420_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0420_P4-21e3aadc90.png` | P4-21e3aadc90 | 420 | 217 |
| `stills_jpg/phase41_reference/generalization_f0475_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0475_P4-21e3aadc90.png` | P4-21e3aadc90 | 475 | 203 |
| `stills_jpg/phase41_reference/generalization_f0500_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0500_P4-21e3aadc90.png` | P4-21e3aadc90 | 500 | 269 |
| `stills_jpg/phase41_reference/generalization_f0560_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0560_P4-21e3aadc90.png` | P4-21e3aadc90 | 560 | 227 |
| `stills_jpg/phase41_reference/generalization_f0590_P4-21e3aadc90.jpg` | `09_before_after/_sumber_phase41/generalization_f0590_P4-21e3aadc90.png` | P4-21e3aadc90 | 590 | 227 |

## Lembar before–after

| File | Asli | Kualitas | Resolusi | KB (asli → turunan) |
|---|---|---|---|---|
| `before_after_jpg/01_lembar_lama__04a_sutil_genggam_sebelum_sesudah.jpg` | `09_before_after/01_lembar_lama__04a_sutil_genggam_sebelum_sesudah.jpg` | asli (disalin) | 1292×466 | 124 → 124 |
| `before_after_jpg/01_sutil_genggam_pergelangan.jpg` | `09_before_after/01_sutil_genggam_pergelangan.jpg` | asli (disalin) | 1818×2122 | 629 → 629 |
| `before_after_jpg/02_bahu_siku_pergelangan_lengan.jpg` | `09_before_after/02_bahu_siku_pergelangan_lengan.jpg` | asli (disalin) | 1818×2122 | 622 → 622 |
| `before_after_jpg/03_penyangga_piring.jpg` | `09_before_after/03_penyangga_piring.jpg` | asli (disalin) | 1818×2122 | 552 → 552 |
| `before_after_jpg/04_lembar_lama__04b_sendok_mulut_sebelum_sesudah.jpg` | `09_before_after/04_lembar_lama__04b_sendok_mulut_sebelum_sesudah.jpg` | asli (disalin) | 976×466 | 110 → 110 |
| `before_after_jpg/04_sendok_ke_mulut.jpg` | `09_before_after/04_sendok_ke_mulut.jpg` | 88 | 2324×2122 | 850 → 717 |
| `before_after_jpg/05_fase_makan.jpg` | `09_before_after/05_fase_makan.jpg` | 82 | 3289×1842 | 1136 → 709 |
| `before_after_jpg/05_fase_minum.jpg` | `09_before_after/05_fase_minum.jpg` | 88 | 2862×1842 | 915 → 764 |
| `before_after_jpg/06_serah_terima_gelas.jpg` | `09_before_after/06_serah_terima_gelas.jpg` | asli (disalin) | 2324×2122 | 792 → 792 |
| `before_after_jpg/06b_serah_terima_uji3.jpg` | `09_before_after/06b_serah_terima_uji3.jpg` | asli (disalin) | 1818×1144 | 344 → 344 |
| `before_after_jpg/07_anatomi_duduk.jpg` | `09_before_after/07_anatomi_duduk.jpg` | asli (disalin) | 1818×2122 | 502 → 502 |
| `before_after_jpg/07_lembar_lama__04d_kaki_duduk_bangku_sebelum_sesudah.jpg` | `09_before_after/07_lembar_lama__04d_kaki_duduk_bangku_sebelum_sesudah.jpg` | asli (disalin) | 1321×426 | 133 → 133 |
| `before_after_jpg/08_lembar_lama__04c_blush_mask_kulit_sebelum_sesudah.jpg` | `09_before_after/08_lembar_lama__04c_blush_mask_kulit_sebelum_sesudah.jpg` | asli (disalin) | 1920×466 | 126 → 126 |
| `before_after_jpg/08_mask_wajah_blush_sri.jpg` | `09_before_after/08_mask_wajah_blush_sri.jpg` | asli (disalin) | 1424×2322 | 374 → 374 |
| `before_after_jpg/09_siluet_transisi_profil.jpg` | `09_before_after/09_siluet_transisi_profil.jpg` | asli (disalin) | 1818×2122 | 589 → 589 |
| `before_after_jpg/09b_tokoh_cerita_ketiga.jpg` | `09_before_after/09b_tokoh_cerita_ketiga.jpg` | asli (disalin) | 2830×1144 | 503 → 503 |
| `before_after_jpg/10_establishing_penutup_benchmark.jpg` | `09_before_after/10_establishing_penutup_benchmark.jpg` | asli (disalin) | 1312×2088 | 484 → 484 |
| `before_after_jpg/10_establishing_penutup_generalisasi.jpg` | `09_before_after/10_establishing_penutup_generalisasi.jpg` | asli (disalin) | 1312×2122 | 371 → 371 |
| `before_after_jpg/11_interior.jpg` | `09_before_after/11_interior.jpg` | asli (disalin) | 2324×2122 | 708 → 708 |
| `before_after_jpg/12_hero_asset_makanan_alat_masak.jpg` | `09_before_after/12_hero_asset_makanan_alat_masak.jpg` | asli (disalin) | 1818×2122 | 520 → 520 |
| `before_after_jpg/13_cahaya_kedalaman_benchmark.jpg` | `09_before_after/13_cahaya_kedalaman_benchmark.jpg` | asli (disalin) | 1818×2088 | 556 → 556 |
| `before_after_jpg/13_cahaya_kedalaman_generalisasi.jpg` | `09_before_after/13_cahaya_kedalaman_generalisasi.jpg` | asli (disalin) | 1312×2088 | 315 → 315 |
| `before_after_jpg/14_phase41_01_final_render.jpg` | `09_before_after/14_phase41_01_final_render.jpg` | asli (disalin) | 3270×960 | 544 → 544 |
| `before_after_jpg/14_phase41_02_raw_render.jpg` | `09_before_after/14_phase41_02_raw_render.jpg` | asli (disalin) | 2178×960 | 357 → 357 |
| `before_after_jpg/14_phase41_03_solid_view.jpg` | `09_before_after/14_phase41_03_solid_view.jpg` | asli (disalin) | 1506×960 | 149 → 149 |
| `before_after_jpg/14_raw_vs_graded.jpg` | `09_before_after/14_raw_vs_graded.jpg` | asli (disalin) | 1818×2088 | 502 → 502 |
| `before_after_jpg/15_kedip_f463-467_benchmark.jpg` | `09_before_after/15_kedip_f463-467_benchmark.jpg` | asli (disalin) | 3000×1048 | 647 → 647 |
| `before_after_jpg/15_lembar_lama__04f_kedip_meja_gerobak_sebelum_sesudah.jpg` | `09_before_after/15_lembar_lama__04f_kedip_meja_gerobak_sebelum_sesudah.jpg` | asli (disalin) | 1740×1010 | 277 → 277 |
| `before_after_jpg/15_lembar_lama__04g_kedip_jendela_zfighting_sebelum_sesudah.jpg` | `09_before_after/15_lembar_lama__04g_kedip_jendela_zfighting_sebelum_sesudah.jpg` | asli (disalin) | 1758×426 | 139 → 139 |

## Provenance terpecah

| File | KB |
|---|---|
| `provenance_split/00_ringkasan.json` | 2 |
| `provenance_split/benchmark_01_provenance_laporan.json` | 310 |
| `provenance_split/benchmark_02_video_dan_scene.json` | 1 |
| `provenance_split/benchmark_03_frame_0001-0150.json` | 32 |
| `provenance_split/benchmark_03_frame_0151-0300.json` | 32 |
| `provenance_split/benchmark_03_frame_0301-0450.json` | 32 |
| `provenance_split/benchmark_03_frame_0451-0600.json` | 32 |
| `provenance_split/benchmark_03_frame_0601-0750.json` | 32 |
| `provenance_split/benchmark_03_frame_0751-0860.json` | 24 |
| `provenance_split/generalization_01_provenance_laporan.json` | 246 |
| `provenance_split/generalization_02_video_dan_scene.json` | 1 |
| `provenance_split/generalization_03_frame_0001-0150.json` | 32 |
| `provenance_split/generalization_03_frame_0151-0300.json` | 32 |
| `provenance_split/generalization_03_frame_0301-0450.json` | 32 |
| `provenance_split/generalization_03_frame_0451-0600.json` | 32 |
| `provenance_split/generalization_03_frame_0601-0616.json` | 3 |
| `provenance_split/third_story_01_provenance_laporan.json` | 211 |
| `provenance_split/third_story_02_video_dan_scene.json` | 1 |
| `provenance_split/third_story_03_frame_0001-0150.json` | 32 |
| `provenance_split/third_story_03_frame_0151-0300.json` | 32 |
| `provenance_split/third_story_03_frame_0301-0450.json` | 32 |
| `provenance_split/third_story_03_frame_0451-0600.json` | 32 |
| `provenance_split/third_story_03_frame_0601-0750.json` | 32 |

## Lembar kontak video

| File | Video asli (Release) | Build | Frame video | Timecode | Langkah | KB |
|---|---|---|---|---|---|---|
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar01_f0001-0116.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 1–116 | 00:00.00–00:03.83 | 5 | 742 |
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar02_f0121-0236.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 121–236 | 00:04.00–00:07.83 | 5 | 756 |
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar03_f0241-0356.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 241–356 | 00:08.00–00:11.83 | 5 | 679 |
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar04_f0361-0476.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 361–476 | 00:12.00–00:15.83 | 5 | 686 |
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar05_f0481-0596.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 481–596 | 00:16.00–00:19.83 | 5 | 769 |
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar06_f0601-0716.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 601–716 | 00:20.00–00:23.83 | 5 | 670 |
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar07_f0721-0836.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 721–836 | 00:24.00–00:27.83 | 5 | 771 |
| `contact_sheets/benchmark/01_benchmark_phase42_P4-486e18fc49_lembar08_f0841-0856.jpg` | [01_benchmark_phase42_P4-486e18fc49.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/01_benchmark_phase42_P4-486e18fc49.mp4) | P4-486e18fc49 | 841–856 | 00:28.00–00:28.50 | 5 | 116 |
| `contact_sheets/generalization/02_generalization_phase42_P4-2d0645d14d_lembar01_f0001-0116.jpg` | [02_generalization_phase42_P4-2d0645d14d.…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/02_generalization_phase42_P4-2d0645d14d.mp4) | P4-2d0645d14d | 1–116 | 00:00.00–00:03.83 | 5 | 580 |
| `contact_sheets/generalization/02_generalization_phase42_P4-2d0645d14d_lembar02_f0121-0236.jpg` | [02_generalization_phase42_P4-2d0645d14d.…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/02_generalization_phase42_P4-2d0645d14d.mp4) | P4-2d0645d14d | 121–236 | 00:04.00–00:07.83 | 5 | 754 |
| `contact_sheets/generalization/02_generalization_phase42_P4-2d0645d14d_lembar03_f0241-0356.jpg` | [02_generalization_phase42_P4-2d0645d14d.…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/02_generalization_phase42_P4-2d0645d14d.mp4) | P4-2d0645d14d | 241–356 | 00:08.00–00:11.83 | 5 | 774 |
| `contact_sheets/generalization/02_generalization_phase42_P4-2d0645d14d_lembar04_f0361-0476.jpg` | [02_generalization_phase42_P4-2d0645d14d.…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/02_generalization_phase42_P4-2d0645d14d.mp4) | P4-2d0645d14d | 361–476 | 00:12.00–00:15.83 | 5 | 661 |
| `contact_sheets/generalization/02_generalization_phase42_P4-2d0645d14d_lembar05_f0481-0596.jpg` | [02_generalization_phase42_P4-2d0645d14d.…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/02_generalization_phase42_P4-2d0645d14d.mp4) | P4-2d0645d14d | 481–596 | 00:16.00–00:19.83 | 5 | 657 |
| `contact_sheets/generalization/02_generalization_phase42_P4-2d0645d14d_lembar06_f0601-0616.jpg` | [02_generalization_phase42_P4-2d0645d14d.…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/02_generalization_phase42_P4-2d0645d14d.mp4) | P4-2d0645d14d | 601–616 | 00:20.00–00:20.50 | 5 | 92 |
| `contact_sheets/third_story/03_third_story_phase42_P4-b1767c3b5e_lembar01_f0001-0116.jpg` | [03_third_story_phase42_P4-b1767c3b5e.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/03_third_story_phase42_P4-b1767c3b5e.mp4) | P4-b1767c3b5e | 1–116 | 00:00.00–00:03.83 | 5 | 672 |
| `contact_sheets/third_story/03_third_story_phase42_P4-b1767c3b5e_lembar02_f0121-0236.jpg` | [03_third_story_phase42_P4-b1767c3b5e.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/03_third_story_phase42_P4-b1767c3b5e.mp4) | P4-b1767c3b5e | 121–236 | 00:04.00–00:07.83 | 5 | 714 |
| `contact_sheets/third_story/03_third_story_phase42_P4-b1767c3b5e_lembar03_f0241-0356.jpg` | [03_third_story_phase42_P4-b1767c3b5e.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/03_third_story_phase42_P4-b1767c3b5e.mp4) | P4-b1767c3b5e | 241–356 | 00:08.00–00:11.83 | 5 | 760 |
| `contact_sheets/third_story/03_third_story_phase42_P4-b1767c3b5e_lembar04_f0361-0476.jpg` | [03_third_story_phase42_P4-b1767c3b5e.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/03_third_story_phase42_P4-b1767c3b5e.mp4) | P4-b1767c3b5e | 361–476 | 00:12.00–00:15.83 | 5 | 705 |
| `contact_sheets/third_story/03_third_story_phase42_P4-b1767c3b5e_lembar05_f0481-0596.jpg` | [03_third_story_phase42_P4-b1767c3b5e.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/03_third_story_phase42_P4-b1767c3b5e.mp4) | P4-b1767c3b5e | 481–596 | 00:16.00–00:19.83 | 5 | 600 |
| `contact_sheets/third_story/03_third_story_phase42_P4-b1767c3b5e_lembar06_f0601-0716.jpg` | [03_third_story_phase42_P4-b1767c3b5e.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/03_third_story_phase42_P4-b1767c3b5e.mp4) | P4-b1767c3b5e | 601–716 | 00:20.00–00:23.83 | 5 | 700 |
| `contact_sheets/third_story/03_third_story_phase42_P4-b1767c3b5e_lembar07_f0721-0746.jpg` | [03_third_story_phase42_P4-b1767c3b5e.mp4…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/03_third_story_phase42_P4-b1767c3b5e.mp4) | P4-b1767c3b5e | 721–746 | 00:24.00–00:24.83 | 5 | 171 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar01_f0001-0058.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 1–58 | 00:00.00–00:01.90 | 3 | 769 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar02_f0061-0118.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 61–118 | 00:02.00–00:03.90 | 3 | 747 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar03_f0121-0178.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 121–178 | 00:04.00–00:05.90 | 3 | 778 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar04_f0181-0238.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 181–238 | 00:06.00–00:07.90 | 3 | 791 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar05_f0241-0298.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 241–298 | 00:08.00–00:09.90 | 3 | 784 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar06_f0301-0358.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 301–358 | 00:10.00–00:11.90 | 3 | 776 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar07_f0361-0418.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 361–418 | 00:12.00–00:13.90 | 3 | 761 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar08_f0421-0478.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 421–478 | 00:14.00–00:15.90 | 3 | 753 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar09_f0481-0538.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 481–538 | 00:16.00–00:17.90 | 3 | 771 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar10_f0541-0598.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 541–598 | 00:18.00–00:19.90 | 3 | 759 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar11_f0601-0658.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 601–658 | 00:20.00–00:21.90 | 3 | 776 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar12_f0661-0718.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 661–718 | 00:22.00–00:23.90 | 3 | 789 |
| `contact_sheets/diagnostic/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e_lembar13_f0721-0721.jpg` | [05_interaction_diagnostic_P4-486e18fc49_…](https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4) | 3 build | 721–721 | 00:24.00–00:24.00 | 3 | 97 |
