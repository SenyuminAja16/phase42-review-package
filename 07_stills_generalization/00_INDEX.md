# Still Teh Sore untuk Ibu — build P4-2d0645d14d

Semua frame berasal dari **render final Colab** (`build/frames_penuh`, checksum per potongan terverifikasi di `frames.json`), bukan render terpisah.

- `raw/`: PNG render mentah (EEVEE, 1080×1920), tautan keras ke file render asli.
- `graded/`: grading video yang sama (koreksi per shot dari `grade_auto.json`) diterapkan pada PNG mentah. Subtitle, grain film, dan fade yang ditambahkan saat perakitan video **tidak** ada di sini. Metadata PNG memuat build ID, shot, filter grading, dan SHA-256 file mentah.

**Pemetaan frame 4.1 → 4.2:** batas shot identik (f115, 220, 366, 483, 545). Waktu aksi bergeser sedikit: `jadwal` mencatat 'dimas ambil teh +4 f' dan 'sri taruh teh +4 f' (menjauhi frame potongan).

| Frame | Shot | Kamera | Alasan | Fase mulut | File |
|---|---|---|---|---|---|
| 7 | 1 | establishing (sri) | shot 1 awal | — | `f0007_s01_P4-2d0645d14d_*.png` |
| 57 | 1 | establishing (sri) | shot 1 tengah | — | `f0057_s01_P4-2d0645d14d_*.png` |
| 60 | 1 | establishing (sri) | frame acuan review 4.1 | — | `f0060_s01_P4-2d0645d14d_*.png` |
| 108 | 1 | establishing (sri) | shot 1 akhir | — | `f0108_s01_P4-2d0645d14d_*.png` |
| 121 | 2 | medium (dimas) | shot 2 awal | — | `f0121_s02_P4-2d0645d14d_*.png` |
| 131 | 2 | medium (dimas) | teh: world:None -> carry:dimas | — | `f0131_s02_P4-2d0645d14d_*.png` |
| 135 | 2 | medium (dimas) | frame acuan review 4.1 | — | `f0135_s02_P4-2d0645d14d_*.png` |
| 143 | 2 | medium (dimas) | teh: carry:dimas -> hand:dimas | — | `f0143_s02_P4-2d0645d14d_*.png` |
| 167 | 2 | medium (dimas) | shot 2 tengah | — | `f0167_s02_P4-2d0645d14d_*.png` |
| 200 | 2 | medium (dimas) | frame acuan review 4.1 | — | `f0200_s02_P4-2d0645d14d_*.png` |
| 213 | 2 | medium (dimas) | shot 2 akhir | — | `f0213_s02_P4-2d0645d14d_*.png` |
| 226 | 3 | full (dimas) | shot 3 awal | — | `f0226_s03_P4-2d0645d14d_*.png` |
| 292 | 3 | full (dimas) | shot 3 tengah | — | `f0292_s03_P4-2d0645d14d_*.png` |
| 300 | 3 | full (dimas) | frame acuan review 4.1 | — | `f0300_s03_P4-2d0645d14d_*.png` |
| 301 | 3 | full (dimas) | teh: hand:dimas -> carry:dimas | — | `f0301_s03_P4-2d0645d14d_*.png` |
| 310 | 3 | full (dimas) | serah-terima f325 (-15) | — | `f0310_s03_P4-2d0645d14d_*.png` |
| 318 | 3 | full (dimas) | frame acuan review 4.1 | — | `f0318_s03_P4-2d0645d14d_*.png` |
| 325 | 3 | full (dimas) | frame acuan review 4.1; teh: carry:dimas -> carry:sri; serah-terima f325 (+0) | — | `f0325_s03_P4-2d0645d14d_*.png` |
| 330 | 3 | full (dimas) | frame acuan review 4.1 | — | `f0330_s03_P4-2d0645d14d_*.png` |
| 337 | 3 | full (dimas) | teh: carry:sri -> hand:sri | — | `f0337_s03_P4-2d0645d14d_*.png` |
| 340 | 3 | full (dimas) | serah-terima f325 (+15) | — | `f0340_s03_P4-2d0645d14d_*.png` |
| 359 | 3 | full (dimas) | shot 3 akhir | — | `f0359_s03_P4-2d0645d14d_*.png` |
| 372 | 4 | closeup (sri) | shot 4 awal | — | `f0372_s04_P4-2d0645d14d_*.png` |
| 420 | 4 | closeup (sri) | frame acuan review 4.1 | — | `f0420_s04_P4-2d0645d14d_*.png` |
| 424 | 4 | closeup (sri) | shot 4 tengah | — | `f0424_s04_P4-2d0645d14d_*.png` |
| 475 | 4 | closeup (sri) | frame acuan review 4.1 | — | `f0475_s04_P4-2d0645d14d_*.png` |
| 476 | 4 | closeup (sri) | shot 4 akhir | — | `f0476_s04_P4-2d0645d14d_*.png` |
| 489 | 5 | medium (sri) | shot 5 awal | teh:angkat | `f0489_s05_P4-2d0645d14d_*.png` |
| 500 | 5 | medium (sri) | frame acuan review 4.1 | teh:dekat_mulut | `f0500_s05_P4-2d0645d14d_*.png` |
| 510 | 5 | medium (sri) | teh: kontak mulut f503-516 | teh:kontak | `f0510_s05_P4-2d0645d14d_*.png` |
| 513 | 5 | medium (sri) | shot 5 tengah | teh:kontak | `f0513_s05_P4-2d0645d14d_*.png` |
| 538 | 5 | medium (sri) | shot 5 akhir | — | `f0538_s05_P4-2d0645d14d_*.png` |
| 549 | 6 | wide (sri) | teh: hand:sri -> carry:sri | — | `f0549_s06_P4-2d0645d14d_*.png` |
| 551 | 6 | wide (sri) | shot 6 awal | — | `f0551_s06_P4-2d0645d14d_*.png` |
| 560 | 6 | wide (sri) | frame acuan review 4.1 | — | `f0560_s06_P4-2d0645d14d_*.png` |
| 561 | 6 | wide (sri) | teh: carry:sri -> world:None | — | `f0561_s06_P4-2d0645d14d_*.png` |
| 580 | 6 | wide (sri) | shot 6 tengah | — | `f0580_s06_P4-2d0645d14d_*.png` |
| 590 | 6 | wide (sri) | frame acuan review 4.1 | — | `f0590_s06_P4-2d0645d14d_*.png` |
| 610 | 6 | wide (sri) | shot 6 akhir | — | `f0610_s06_P4-2d0645d14d_*.png` |
