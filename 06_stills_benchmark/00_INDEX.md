# Still Satu Bungkus Lagi — build P4-486e18fc49

Semua frame berasal dari **render final Colab** (`build/frames_penuh`, checksum per potongan terverifikasi di `frames.json`), bukan render terpisah.

- `raw/`: PNG render mentah (EEVEE, 1080×1920), tautan keras ke file render asli.
- `graded/`: grading video yang sama (koreksi per shot dari `grade_auto.json`) diterapkan pada PNG mentah. Subtitle, grain film, dan fade yang ditambahkan saat perakitan video **tidak** ada di sini. Metadata PNG memuat build ID, shot, filter grading, dan SHA-256 file mentah.

**Pemetaan frame 4.1 → 4.2:** batas shot identik di kedua versi (deteksi potongan pada video 4.1 dan 4.2 memberi f75, 159, 199, 226, 282, 458, 541, 612, 732; potongan f703 ke shot 10 tidak terdeteksi otomatis di kedua versi karena subjek dan latar sama, tetapi ada di `plan.json`). Jadi nomor frame acuan 4.1 menunjuk ke shot yang sama di 4.2. **Isi aksi di dalam shot berubah:** jadwal suapan dijangkarkan ulang (`schedule.eat_cycles_visible`), sehingga kontak sendok–mulut di shot 5 kini f233–235 (4.1: hanya di f226, frame potongan). Frame f240 di 4.2 berada di fase `kembali`, bukan kontak; frame setara fase kontak adalah f234.

Shot 10 (f703–731, closeup Jali) yang belum diuji di review 4.1 diwakili oleh frame awal/tengah/akhir shot 10 di bawah.

| Frame | Shot | Kamera | Alasan | Fase mulut | File |
|---|---|---|---|---|---|
| 7 | 1 | establishing (gerobak) | shot 1 awal | — | `f0007_s01_P4-486e18fc49_*.png` |
| 37 | 1 | establishing (gerobak) | shot 1 tengah | — | `f0037_s01_P4-486e18fc49_*.png` |
| 60 | 1 | establishing (gerobak) | frame acuan review 4.1 | — | `f0060_s01_P4-486e18fc49_*.png` |
| 68 | 1 | establishing (gerobak) | shot 1 akhir | — | `f0068_s01_P4-486e18fc49_*.png` |
| 81 | 2 | full (darto) | shot 2 awal | sendok:istirahat | `f0081_s02_P4-486e18fc49_*.png` |
| 104 | 2 | full (darto) | sendok: kontak mulut f102-106 | sendok:kontak | `f0104_s02_P4-486e18fc49_*.png` |
| 116 | 2 | full (darto) | shot 2 tengah | sendok:kembali | `f0116_s02_P4-486e18fc49_*.png` |
| 120 | 2 | full (darto) | frame acuan review 4.1 | sendok:istirahat | `f0120_s02_P4-486e18fc49_*.png` |
| 149 | 2 | full (darto) | sendok: kontak mulut f147-151 | sendok:kontak | `f0149_s02_P4-486e18fc49_*.png` |
| 152 | 2 | full (darto) | shot 2 akhir | sendok:tarik | `f0152_s02_P4-486e18fc49_*.png` |
| 165 | 3 | medium (darto) | shot 3 awal | sendok:istirahat | `f0165_s03_P4-486e18fc49_*.png` |
| 178 | 3 | medium (darto) | shot 3 tengah | sendok:sendok | `f0178_s03_P4-486e18fc49_*.png` |
| 180 | 3 | medium (darto) | frame acuan review 4.1 | sendok:sendok | `f0180_s03_P4-486e18fc49_*.png` |
| 192 | 3 | medium (darto) | shot 3 akhir | sendok:kontak | `f0192_s03_P4-486e18fc49_*.png` |
| 194 | 3 | medium (darto) | sendok: kontak mulut f192-196 | sendok:kontak | `f0194_s03_P4-486e18fc49_*.png` |
| 205 | 4 | insert (gerobak.wajan) | shot 4 awal | sendok:kembali | `f0205_s04_P4-486e18fc49_*.png` |
| 212 | 4 | insert (gerobak.wajan) | frame acuan review 4.1; shot 4 tengah | sendok:istirahat | `f0212_s04_P4-486e18fc49_*.png` |
| 219 | 4 | insert (gerobak.wajan) | shot 4 akhir | sendok:sendok | `f0219_s04_P4-486e18fc49_*.png` |
| 222 | 4 | insert (gerobak.wajan) | frame acuan review 4.1 | sendok:sendok | `f0222_s04_P4-486e18fc49_*.png` |
| 232 | 5 | medium (jali) | shot 5 awal | sendok:dekat_mulut | `f0232_s05_P4-486e18fc49_*.png` |
| 234 | 5 | medium (jali) | frame bukti tambahan 4.2; sendok: kontak mulut f233-235 | sendok:kontak | `f0234_s05_P4-486e18fc49_*.png` |
| 240 | 5 | medium (jali) | frame acuan review 4.1 | sendok:kembali | `f0240_s05_P4-486e18fc49_*.png` |
| 250 | 5 | medium (jali) | frame acuan review 4.1 | sendok:istirahat | `f0250_s05_P4-486e18fc49_*.png` |
| 253 | 5 | medium (jali) | shot 5 tengah | sendok:istirahat | `f0253_s05_P4-486e18fc49_*.png` |
| 254 | 5 | medium (jali) | sendok: hand:jali -> place:jali | — | `f0254_s05_P4-486e18fc49_*.png` |
| 268 | 5 | medium (jali) | sendok: place:jali -> on:None | — | `f0268_s05_P4-486e18fc49_*.png` |
| 275 | 5 | medium (jali) | shot 5 akhir | — | `f0275_s05_P4-486e18fc49_*.png` |
| 282 | 6 | mcu (jali) | frame acuan review 4.1 | — | `f0282_s06_P4-486e18fc49_*.png` |
| 288 | 6 | mcu (jali) | shot 6 awal | — | `f0288_s06_P4-486e18fc49_*.png` |
| 330 | 6 | mcu (jali) | frame acuan review 4.1 | — | `f0330_s06_P4-486e18fc49_*.png` |
| 369 | 6 | mcu (jali) | shot 6 tengah | — | `f0369_s06_P4-486e18fc49_*.png` |
| 380 | 6 | mcu (jali) | frame acuan review 4.1 | — | `f0380_s06_P4-486e18fc49_*.png` |
| 451 | 6 | mcu (jali) | shot 6 akhir | — | `f0451_s06_P4-486e18fc49_*.png` |
| 458 | 7 | ots (jali) | sutil: hand:darto -> world:None | — | `f0458_s07_P4-486e18fc49_*.png` |
| 464 | 7 | ots (jali) | shot 7 awal | — | `f0464_s07_P4-486e18fc49_*.png` |
| 465 | 7 | ots (jali) | frame bukti tambahan 4.2 | — | `f0465_s07_P4-486e18fc49_*.png` |
| 478 | 7 | ots (jali) | frame bukti tambahan 4.2 | — | `f0478_s07_P4-486e18fc49_*.png` |
| 499 | 7 | ots (jali) | shot 7 tengah | — | `f0499_s07_P4-486e18fc49_*.png` |
| 500 | 7 | ots (jali) | frame acuan review 4.1 | — | `f0500_s07_P4-486e18fc49_*.png` |
| 534 | 7 | ots (jali) | shot 7 akhir | — | `f0534_s07_P4-486e18fc49_*.png` |
| 547 | 8 | mcu (darto) | shot 8 awal | — | `f0547_s08_P4-486e18fc49_*.png` |
| 576 | 8 | mcu (darto) | shot 8 tengah | — | `f0576_s08_P4-486e18fc49_*.png` |
| 580 | 8 | mcu (darto) | frame acuan review 4.1 | — | `f0580_s08_P4-486e18fc49_*.png` |
| 605 | 8 | mcu (darto) | shot 8 akhir | — | `f0605_s08_P4-486e18fc49_*.png` |
| 615 | 9 | mcu (jali) | frame acuan review 4.1 | — | `f0615_s09_P4-486e18fc49_*.png` |
| 618 | 9 | mcu (jali) | shot 9 awal | — | `f0618_s09_P4-486e18fc49_*.png` |
| 657 | 9 | mcu (jali) | shot 9 tengah | — | `f0657_s09_P4-486e18fc49_*.png` |
| 696 | 9 | mcu (jali) | shot 9 akhir | — | `f0696_s09_P4-486e18fc49_*.png` |
| 700 | 9 | mcu (jali) | frame acuan review 4.1 | — | `f0700_s09_P4-486e18fc49_*.png` |
| 709 | 10 | closeup (jali) | shot 10 awal | — | `f0709_s10_P4-486e18fc49_*.png` |
| 717 | 10 | closeup (jali) | shot 10 tengah | — | `f0717_s10_P4-486e18fc49_*.png` |
| 725 | 10 | closeup (jali) | shot 10 akhir | — | `f0725_s10_P4-486e18fc49_*.png` |
| 738 | 11 | ending (darto) | shot 11 awal | — | `f0738_s11_P4-486e18fc49_*.png` |
| 760 | 11 | ending (darto) | frame acuan review 4.1 | — | `f0760_s11_P4-486e18fc49_*.png` |
| 796 | 11 | ending (darto) | shot 11 tengah | — | `f0796_s11_P4-486e18fc49_*.png` |
| 854 | 11 | ending (darto) | shot 11 akhir | — | `f0854_s11_P4-486e18fc49_*.png` |
