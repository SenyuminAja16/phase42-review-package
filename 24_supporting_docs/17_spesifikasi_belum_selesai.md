# Phase 4.2 — Spesifikasi yang belum selesai / hanya sebagian

Daftar jujur item spesifikasi Phase 4.2 yang **tidak** atau **belum sepenuhnya** dikerjakan.

| # | Item spesifikasi | Status | Keterangan |
|---|---|---|---|
| 1 | P0.2 pose penyangga piring (jari di bawah, ibu jari di tepi) | **Belum** | Piring masih memakai genggam jepit tepi (`rim`). Lapisan tangan `support` direncanakan di `PHASE42_PLAN.md` tetapi tidak dibuat. Ukuran piring sudah konstan dan geser presentasi dibatasi/terukur. |
| 2 | Gate B: kontur bahu/siku/pergelangan, sambungan tangan–lengan bawah, pose tangan per kelas | **Belum** | Yang dikerjakan di Gate B hanya mask kulit blush dan kaki duduk (pivot lutut + celah dudukan). |
| 3 | Gate B: keberagaman siluet tokoh | **Sebagian** | Tokoh uji ke-3 memakai parameter yang sudah ada (peci/kumis/tua, rambut panjang). Tidak ada generator siluet baru. |
| 4 | P1 hero asset (nasi goreng, sutil, piring, gelas, alat masak, gerobak) dengan tier kualitas | **Belum di 4.2** | Masih aset 4.1. Yang ditingkatkan di 4.2 adalah perabot interior (meja, kursi, kursi tamu, bufet, dll.). |
| 5 | P1 preset pencahayaan baru | **Sebagian** | Preset atmosfer yang ada (`atmosfer.py`: pagi/siang/senja/malam) dipakai; tidak ada preset baru. Interior mendapat sinar matahari jendela. Kedip api diperbaiki. |
| 6 | Arah hadap tokoh duduk dibatasi oleh orientasi dudukan | **Belum** | `bangku` punya `maju: None`, sehingga tokoh bisa menghadap sepanjang bangku. Di uji ke-3 hal ini dihindari lewat blocking. |
| 7 | Jalan otomatis menghadap tujuan | **Belum** | Tanpa aksi `hadap` eksplisit, tokoh berjalan dengan arah hadap terakhir; di uji ke-3 terjadi jalan mundur sambil membawa. Diatasi di `story.yaml`. |
| 8 | Keterlihatan aksi (proyeksi) | **Sebagian** | `aksi_dalam_shot` adalah heuristik daftar shot, bukan uji proyeksi tangan/benda di layar. |
| 9 | Kepala tumpang-tindih pada serah-terima dekat (rig chibi) | **Belum** | Diameter kepala sekitar 0,5 m, jarak serah ~0,45 m. Belum ada condong badan atau offset kepala. |
| 10 | Jangkauan IK 2D tidak bergantung kamera | **Belum** | Residual bergantung pada sudut pandang; titik taruh generalisasi harus digeser 14 cm setelah kamera berubah. |
| 11 | Lonjakan pergelangan di frame pertama segmen genggam (uji3 f40, 59,7°) | **Belum** | Satu frame. |
| 12 | IK meleset saat mengangkat cangkir (uji3 f619–625, 8–15 px) | **Belum** | Fase angkat; kontak bibir sendiri ≤ 1,3 px. |
| 13 | Before/after A/B satu variabel | **Tidak tersedia** | Lembar sebelum/sesudah membandingkan build 4.1 vs 4.2 yang berbeda di banyak variabel (kamera, interior, interaksi). Diberi label. |
| 14 | Lip-sync perseptual | NOT_TESTED | Butuh penilaian manusia. |
| 15 | Palet interior `sejuk` | Tidak dirender | Hanya `hangat` yang dipakai di cerita. |
| 16 | Klip diagnostik terpisah dari render khusus | **Sebagian** | Klip diagnostik di paket adalah cuplikan dari video final (rentang frame dicatat), bukan render terpisah. |
| 17 | Validasi `musik.suasana` di tahap rencana | **Belum** | Nilai tidak dikenal baru gagal di langkah audio, setelah render. Di uji ke-3 ini menyebabkan satu render Colab terbuang. |
| 18 | Uji kedip yang dapat dijalankan sebelum render penuh | **Sebagian** | Pantulan kini memakai `PROBE`, sehingga sumber kedip yang hanya muncul di Colab dihilangkan, dan `cek_sebidang.py` menangkap z-fighting sebelum render. QA kedip tetap hanya pasti dari video. Klip uji pendek di Colab sebelum render penuh belum menjadi langkah wajib. |
| 19 | Sisa pasangan sebidang (`build/sebidang.json`) | **Belum** | Jendela jauh (benchmark), jari roda, bayangan kontak dua tokoh saat berdekatan, poster di balik kaca, plafon turun (generalisasi). Tidak memicu FAIL kedip di QA video; tidak diperbaiki. |
