# Phase 4.2 — Masalah visual yang LOLOS validator

Validator mengukur geometri dan waktu, bukan kualitas gambar. Di bawah ini masalah yang saya lihat langsung di still atau render, tetapi tidak ditandai FAIL oleh validator. Daftar ini tidak lengkap: penilaian artistik tetap ada di tangan reviewer.

| # | Cerita / frame | Masalah | Status validator | Catatan |
|---|---|---|---|---|
| 1 | Uji ke-3 f330–420 (two-shot serah-terima) | Kepala Wulan menutupi sebagian wajah Harjo. Kepala chibi berdiameter ~0,5 m, jarak serah-terima ~0,45 m. | `wajah_subjek` PASS (subjek = Wulan, wajahnya terlihat); validator interaksi `wajah_terhalang` hanya mengukur subjek | Belum ada condong badan/offset kepala |
| 2 | Uji ke-3 f165 | Wulan mengambil cangkir sambil membelakangi kamera, sehingga tangan dan cangkir tidak terbaca. | PASS | Pilihan blocking; aksi ambil kurang terbaca |
| 3 | Uji ke-3 shot duduk | Kaki duduk Harjo (tampak 3/4) berbentuk sederhana: paha horizontal lalu betis yang diregang ×2,2. Paha menempel di tepi depan bangku. | PASS | Bentuk kaki duduk Gate B belum diperhalus |
| 4 | Uji ke-3 (rambut panjang) | Rambut panjang Wulan tampak sebagai massa hitam besar dari belakang/samping; dalam cahaya senja terbaca seperti helm. | — | Gaya rambut yang sudah ada; tidak diubah di 4.2 |
| 5 | Generalisasi shot medium/full | Kepala Sri sangat dekat dengan tepi kiri. Masih di dalam tepi aman 0,86 NDC, tetapi ketat. Okupansi subjek turun karena tokoh lain ikut dibingkai. | `komposisi_pita` WARN (beralasan) | Pilihan solver: semua kepala utuh vs okupansi |
| 6 | Semua cerita, two-shot 9:16 | Okupansi di bawah pita karena lebar kelompok. | WARN | Batas format potret |
| 7 | Benchmark f234 | Pada fase kontak, cekung sendok tertutup tangan di depan mulut; suapan terbaca dari tangan dan mulut, bukan dari sendok. | `kontak_mulut` PASS (0,0 px) | Urutan lapisan tangan di depan sendok |
| 8 | Benchmark shot makan | Siklus suapan terakhir dipendekkan (35 frame) agar terlihat di shot makan, sehingga suapan ini lebih cepat dari yang lain. | PASS | Efek penjadwal sadar-shot |
| 9 | Piring (benchmark/uji ke-3) | Piring dipegang dengan jepit tepi; tidak ada jari di bawah piring. | PASS | Spesifikasi P0.2 support belum dibuat (lihat 17) |
| 10 | Interior generalisasi | Dinding polos tanpa variasi tekstur; furnitur tampak baru, tanpa jejak pemakaian. | — | Art direction sebagian |
| 11 | Generalisasi closeup f420/f475 | Meja di latar depan besar dan kabur, memakan sepertiga bawah bingkai. | PASS | Sudut closeup |
| 12 | Uji ke-3 f40 (1 frame) | Pergelangan tangan pemegang piring 59,7° pada frame pertama segmen genggam; mungkin terlihat sebagai pop. | WARN | Lihat 17 #11 |
| 13 | Benchmark, meja gerobak | Sesudah perbaikan kedip, permukaan kerja tampak stainless kusam (brushed), tidak berkilau lagi. Masih ada sisa bintik halus pantulan di dekat tumpukan piring. | `flicker_temporal` (lihat `00_STATUS_RENDER.md`) | Kompromi: stabil antar-frame vs kilap logam |
| 14 | Semua cerita (render lokal vs Colab) | Pantulan raytraced berbeda antara GPU lokal dan GPU Colab; still lokal yang PASS tidak menjamin video Colab bebas kedip. Pantulan kini `PROBE`, sehingga kilap logam/kaca sedikit kurang tajam. | still PASS | Lihat 17 #18 |
| 15 | Semua cerita | Kemungkinan kedip kecil dari sisa pasangan sebidang (jendela jauh, bayangan kontak dua tokoh saat berdekatan). | QA video PASS/WARN | Lihat 17 #19 |
