"""Perakit paket review independen Phase 4.2 -> output/phase42/review_package/

TIDAK merender ulang adegan dan TIDAK mengubah engine/story/build. Semua bukti diambil dari artefak build final:
  - video final  : stories/<s>/output/<s>.mp4 (build ID di metadata 'comment' dicek terhadap manifest)
  - frame mentah : stories/<s>/build/frames_penuh/f_NNNN.png (render Colab final, checksum per potongan di frames.json)
  - frame graded : grading video yang SAMA (make.grade_filters + koreksi shot dari build/grade_auto.json) diterapkan
                   ke frame mentah; tanpa subtitle, grain, dan fade (yang ditambahkan saat perakitan video)
  - Phase 4.1    : output/phase41/ (video & still 4.1, diberi label build 4.1; bukan pengganti bukti 4.2)
Dijalankan:  .venv/bin/python output/phase42/review_package/_alat/bangun_paket_review.py [langkah ...]
Langkah: verifikasi video still lembar banding diagnostik teknis blend checksum (default: semua)"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import difflib
import tempfile
from itertools import groupby
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin  # noqa: E402

import make  # noqa: E402
from engine import grade as G, manifest as M  # noqa: E402
from engine.common import Story  # noqa: E402

PKG = ROOT / "output" / "phase42" / "review_package"
P41 = ROOT / "output" / "phase41"
P42 = ROOT / "output" / "phase42"
FONT = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FPS = 30

S = [  # kunci, folder cerita, judul, folder still, nama video, build 4.1 (bila ada)
    {"k": "benchmark", "dir": "benchmark_warung", "judul": "Satu Bungkus Lagi", "still": "06_stills_benchmark",
     "vid": "01_benchmark_phase42", "v41": P41 / "08_animation_P4-4b69684991.mp4", "b41": "P4-4b69684991",
     "s41": P41 / "01_stills_benchmark", "s42": P42 / "01_stills_benchmark",
     "wajib": [60, 120, 180, 212, 222, 240, 250, 282, 330, 380, 500, 580, 615, 700, 760], "tambah": [234, 465, 478]},
    {"k": "generalization", "dir": "_uji_phase4_rumah", "judul": "Teh Sore untuk Ibu", "still": "07_stills_generalization",
     "vid": "02_generalization_phase42", "v41": P41 / "15_generalization_test_P4-21e3aadc90.mp4", "b41": "P4-21e3aadc90",
     "s41": P41 / "01_stills_generalisasi", "s42": P42 / "01_stills_generalisasi",
     "wajib": [60, 135, 200, 300, 318, 325, 330, 420, 475, 500, 560, 590], "tambah": []},
    {"k": "third_story", "dir": "uji3_kopi_sore", "judul": "Kopi Sore (cerita ke-3, baru)", "still": "08_stills_third_story",
     "vid": "03_third_story_phase42", "v41": None, "b41": None, "s41": None, "s42": P42 / "01_stills_uji3",
     "wajib": [], "tambah": [141]},
]
for s in S:
    s["story"] = Story(f"stories/{s['dir']}")
    s["b"] = ROOT / "stories" / s["dir"] / "build"
    s["man"] = json.loads((s["b"] / "manifest.json").read_text())
    s["bid"] = s["man"]["build_id"]
    s["plan"] = json.loads((s["b"] / "plan.json").read_text())
    s["inter"] = json.loads((s["b"] / "interaksi.json").read_text())
    s["v42"] = ROOT / "stories" / s["dir"] / "output" / f"{s['dir']}.mp4"


def sha(p):
    return M.sha256_file(p)


def log(*a):
    print(*a, flush=True)


def link(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)                    # tautan keras: file individual, tanpa salinan ganda di disk
    except OSError:
        shutil.copy2(src, dst)


def shot_of(s, f):
    return next(x for x in s["plan"]["shots"] if x["f0"] <= f <= x["f1"])


def font(n, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, n)


# ---------------------------------------------------------------- verifikasi
def verifikasi():
    rep = {}
    src_now = M.source_hash()[0]
    for s in S:
        meta = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format_tags=comment", "-of",
                               "default=nw=1:nk=1", str(s["v42"])], capture_output=True, text=True).stdout.strip()
        fj = json.loads((s["b"] / "frames_penuh" / "frames.json").read_text())["frame"]
        prov = json.loads((s["b"] / f"provenance_1_{s['plan']['end']}.json").read_text())
        r = {"build_id": s["bid"], "video_comment": meta,
             "video_build_cocok": f"build_id={s['bid']}" in meta,
             "frame_terverifikasi": sum(1 for v in fj.values() if v.get("status") == "terverifikasi_chunk" and v.get("build_id") == s["bid"]),
             "frame_total": s["plan"]["end"],
             "provenance": prov["status"], "provenance_build": prov["build_id"],
             "scene_blend_sha256_manifest": s["man"]["scene_build"]["scene_blend_sha256"],
             "scene_blend_sha256_disk": sha(s["b"] / "scene.blend"),
             "source_hash_manifest": s["man"]["inputs"]["source_hash"], "source_hash_sekarang": src_now}
        r["ok"] = (r["video_build_cocok"] and r["frame_terverifikasi"] == r["frame_total"] and r["provenance"] == "PASS"
                   and r["provenance_build"] == s["bid"] and r["scene_blend_sha256_manifest"] == r["scene_blend_sha256_disk"]
                   and r["source_hash_manifest"] == src_now)
        rep[s["k"]] = r
        log("verifikasi", s["k"], s["bid"], "OK" if r["ok"] else "GAGAL", {k: v for k, v in r.items() if k != "video_comment"})
    if not all(r["ok"] for r in rep.values()):
        sys.exit("verifikasi gagal: paket TIDAK dirakit")
    return rep


# ---------------------------------------------------------------- video final
def video():
    for s in S:
        link(s["v42"], PKG / f"{s['vid']}_{s['bid']}.mp4")
        log("video", s["vid"], s["bid"])


# ---------------------------------------------------------------- still
def graded_png(s, f, dst, raw):
    sh = shot_of(s, f)
    ov = make.shot_override(s["story"], s["plan"], shot=sh)       # cache build/grade_auto.json (build ini)
    flt = make.grade_filters(s["story"], ov)
    im = G.apply(raw, flt)
    info = PngImagePlugin.PngInfo()
    for k, v in {"build_id": s["bid"], "kind": "graded_dari_frame_render_final", "frame": str(f),
                 "shot": f"shot{sh['n']:02d}_{sh['kamera']}_{sh.get('subjek')}", "raw_sha256": sha(raw),
                 "grading": ",".join(flt), "catatan": "grading video yang sama; tanpa subtitle/grain/fade"}.items():
        info.add_text(k, v)
    im.save(dst, pnginfo=info)


def pilih_frame(s):
    """-> {frame: [alasan]}"""
    out = {}

    def add(f, why):
        f = max(1, min(s["plan"]["end"], int(f)))
        out.setdefault(f, [])
        if why not in out[f]:
            out[f].append(why)
    for f in s["wajib"]:
        add(f, "frame acuan review 4.1")
    for f in s["tambah"]:
        add(f, "frame bukti tambahan 4.2")
    for x in s["plan"]["shots"]:
        n = x["f1"] - x["f0"]
        add(x["f0"] + min(6, n // 4), f"shot {x['n']} awal")
        add((x["f0"] + x["f1"]) // 2, f"shot {x['n']} tengah")
        add(x["f1"] - min(6, n // 4), f"shot {x['n']} akhir")
    for n, p in s["inter"]["props"].items():
        km = p.get("kontak_mulut_per_frame", {})
        fr = sorted(int(f) for f in km)
        for ph, g in groupby(fr, key=lambda f: km[str(f)][0]):
            g = list(g)
            if ph == "kontak":
                add(g[len(g) // 2], f"{n.rsplit('_', 2)[0]}: kontak mulut f{g[0]}-{g[-1]}")
    for t in s["inter"].get("transisi_kepemilikan", []):
        add(t["frame"], f"{t['benda'].rsplit('_', 2)[0]}: {t['dari']} -> {t['ke']}")
    for h in s["inter"].get("serah_terima", []):
        for d in (-15, 0, 15):
            add(h["frame"] + d, f"serah-terima f{h['frame']} ({d:+d})")
    return dict(sorted(out.items()))


def still():
    for s in S:
        d = PKG / s["still"]
        (d / "graded").mkdir(parents=True, exist_ok=True)
        (d / "raw").mkdir(parents=True, exist_ok=True)
        fr = pilih_frame(s)
        rows = []
        for f, why in fr.items():
            raw = s["b"] / "frames_penuh" / f"f_{f:04d}.png"
            sh = shot_of(s, f)
            tag = f"f{f:04d}_s{sh['n']:02d}_{s['bid']}"
            link(raw, d / "raw" / f"{tag}_raw.png")
            g = d / "graded" / f"{tag}_graded.png"
            if not g.exists():
                graded_png(s, f, g, raw)
            ph = []
            for n, p in s["inter"]["props"].items():
                v = p.get("kontak_mulut_per_frame", {}).get(str(f))
                if v:
                    ph.append(f"{n.rsplit('_', 2)[0]}:{v[0]}")
            rows.append((f, sh, why, ph, tag))
        lines = [f"# Still {s['judul']} — build {s['bid']}", "",
                 "Semua frame berasal dari **render final Colab** (`build/frames_penuh`, checksum per potongan "
                 "terverifikasi di `frames.json`), bukan render terpisah.", "",
                 "- `raw/`: PNG render mentah (EEVEE, 1080×1920), tautan keras ke file render asli.",
                 "- `graded/`: grading video yang sama (koreksi per shot dari `grade_auto.json`) diterapkan pada PNG mentah. "
                 "Subtitle, grain film, dan fade yang ditambahkan saat perakitan video **tidak** ada di sini. "
                 "Metadata PNG memuat build ID, shot, filter grading, dan SHA-256 file mentah.", ""]
        if s["k"] == "benchmark":
            lines += ["**Pemetaan frame 4.1 → 4.2:** batas shot identik di kedua versi (deteksi potongan pada video 4.1 dan 4.2 "
                      "memberi f75, 159, 199, 226, 282, 458, 541, 612, 732; potongan f703 ke shot 10 tidak terdeteksi otomatis di "
                      "kedua versi karena subjek dan latar sama, tetapi ada di `plan.json`). Jadi nomor frame acuan 4.1 menunjuk ke "
                      "shot yang sama di 4.2. **Isi aksi di dalam shot berubah:** jadwal suapan dijangkarkan ulang "
                      "(`schedule.eat_cycles_visible`), sehingga kontak sendok–mulut di shot 5 kini f233–235 (4.1: hanya di f226, "
                      "frame potongan). Frame f240 di 4.2 berada di fase `kembali`, bukan kontak; frame setara fase kontak adalah f234.", "",
                      "Shot 10 (f703–731, closeup Jali) yang belum diuji di review 4.1 diwakili oleh frame awal/tengah/akhir shot 10 di bawah.", ""]
        if s["k"] == "generalization":
            lines += ["**Pemetaan frame 4.1 → 4.2:** batas shot identik (f115, 220, 366, 483, 545). Waktu aksi bergeser sedikit: "
                      "`jadwal` mencatat 'dimas ambil teh +4 f' dan 'sri taruh teh +4 f' (menjauhi frame potongan).", ""]
        lines += ["| Frame | Shot | Kamera | Alasan | Fase mulut | File |", "|---|---|---|---|---|---|"]
        for f, sh, why, ph, tag in rows:
            lines.append(f"| {f} | {sh['n']} | {sh['kamera']} ({sh.get('subjek')}) | {'; '.join(why)} | {', '.join(ph) or '—'} | `{tag}_*.png` |")
        (d / "00_INDEX.md").write_text("\n".join(lines) + "\n")
        log("still", s["k"], len(rows), "frame")


# ---------------------------------------------------------------- ekstrak frame video
def frames_from_video(video, frames, out_dir):
    """ekstrak beberapa frame (1-based) dari video dalam satu lintasan -> {f: path}"""
    out_dir.mkdir(parents=True, exist_ok=True)
    want = sorted(set(frames))
    todo = [f for f in want if not (out_dir / f"v_{f:04d}.png").exists()]
    if todo:
        expr = "+".join(f"eq(n\\,{f - 1})" for f in todo)
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf", f"select='{expr}'", "-vsync", "0",
                            str(Path(td) / "o_%04d.png")], check=True)
            for i, f in enumerate(todo, 1):
                shutil.move(str(Path(td) / f"o_{i:04d}.png"), out_dir / f"v_{f:04d}.png")
    return {f: out_dir / f"v_{f:04d}.png" for f in want}


# ---------------------------------------------------------------- lembar sebelum/sesudah
def sheet(path, title, sub, cols, rows, cell_h=900, notes=(), aspect=9 / 16):
    """cols: label kolom (frame); rows: [(label baris, [path|None])]"""
    fx = lambda t: t.replace("→", "->")              # NotoSans tidak punya glyph panah
    title, sub, notes, cols = fx(title), fx(sub), [fx(n) for n in notes], [fx(c) for c in cols]
    cw = int(cell_h * aspect)
    lab_w = 300
    head = 150 + 34 * len(notes)
    W = lab_w + cw * len(cols)
    H = head + 50 + (cell_h + 10) * len(rows)
    im = Image.new("RGB", (W, H), (24, 24, 26))
    d = ImageDraw.Draw(im)
    d.text((20, 16), title, font=font(44, True), fill=(255, 255, 255))
    d.text((20, 74), sub, font=font(26), fill=(230, 200, 120))
    for i, n in enumerate(notes):
        d.text((20, 116 + 34 * i), n, font=font(24), fill=(200, 200, 200))
    for j, c in enumerate(cols):
        d.text((lab_w + j * cw + 10, head + 8), c, font=font(28, True), fill=(255, 230, 120))
    for i, (lab, imgs) in enumerate(rows):
        y = head + 50 + i * (cell_h + 10)
        yy = y + 10
        for line in lab.split("\n"):
            d.text((14, yy), line, font=font(26, True if yy == y + 10 else False), fill=(255, 255, 255))
            yy += 34
        for j, p in enumerate(imgs):
            x = lab_w + j * cw
            if p is None or not Path(p).exists():
                d.rectangle([x + 4, y, x + cw - 4, y + cell_h], outline=(120, 60, 60), width=3)
                d.text((x + 20, y + cell_h // 2), "TIDAK TERSEDIA", font=font(30, True), fill=(220, 90, 90))
                continue
            t = Image.open(p).convert("RGB").resize((cw - 8, cell_h), Image.LANCZOS)
            im.paste(t, (x + 4, y))
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, quality=92)


def banding():
    out = PKG / "09_before_after"
    tmp = PKG / "_tmp_frames"
    B, Gn, U = S
    vf = {}                                       # (cerita, versi) -> {f: path} (frame dari video final)

    def vframes(s, ver, frames):
        v = s["v41"] if ver == "41" else s["v42"]
        return frames_from_video(v, frames, tmp / f"{s['k']}_{ver}")

    def st41(s, f):
        p = s["s41"] / f"f{f:04d}_{s['b41']}.png"
        return p if p.exists() else None

    def st42(s, f):
        p = s["s42"] / f"f{f:04d}_{s['bid']}.png"
        return p if p.exists() else None

    def raw42(s, f):
        return s["b"] / "frames_penuh" / f"f_{f:04d}.png"

    def graded42(s, f):
        sh = shot_of(s, f)
        p = PKG / s["still"] / "graded" / f"f{f:04d}_s{sh['n']:02d}_{s['bid']}_graded.png"
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            graded_png(s, f, p, raw42(s, f))
        return p

    KOND_STILL = ("Kondisi: KEDUA kolom = still lokal ter-grading dari pipeline yang sama (make.py --frame), frame sama. "
                  "BUILD BERBEDA (4.1 vs 4.2): kamera/komposisi, interior, dan interaksi dapat berbeda sekaligus.")
    KOND_VIDEO = ("Kondisi: KEDUA baris = frame dari video final (h264, subtitle+grain ikut), nomor frame sama. "
                  "BUILD BERBEDA: kamera/komposisi/waktu aksi dapat berbeda.")

    def pair_still(s, frames):
        return [(f"Phase 4.1\n{s['b41']}", [st41(s, f) for f in frames]),
                (f"Phase 4.2\n{s['bid']}", [st42(s, f) for f in frames])]

    def pair_video(s, frames):
        a, b = vframes(s, "41", frames), vframes(s, "42", frames)
        return [(f"Phase 4.1\n{s['b41']}", [a[f] for f in frames]), (f"Phase 4.2\n{s['bid']}", [b[f] for f in frames])]

    T = []      # (nomor, nama, status, file lembar, catatan)

    def mk(no, slug, title, status, cols, rows, notes, cell_h=900):
        p = out / f"{no:02d}_{slug}.jpg"
        sheet(p, f"{no:02d}. {title}", f"Status implementasi 4.2: {status}", cols, rows, cell_h, notes)
        T.append((no, title, status, p.name, notes))
        log("lembar", p.name)

    def old(no, name, label):
        src = P42 / name
        if src.exists():
            link(src, out / f"{no:02d}_{label}__{name}")
            return f"{no:02d}_{label}__{name}"

    # 1 sutil
    fr = [120, 180, 212]
    mk(1, "sutil_genggam_pergelangan", "Genggam sutil anatomis & orientasi pergelangan", "COMPLETE (numerik); visual: reviewer",
       [f"f{f} (shot {shot_of(B, f)['n']})" for f in fr], pair_still(B, fr),
       [KOND_STILL, "4.1: 140 frame sutil memakai target orientasi yang DIBALIK diam-diam (galat dilaporkan ~0,2°). "
        "4.2: 0 frame terbalik tanpa izin profil; galat thd pronasi desain maks 8,3° (tol 10°).",
        "4.2 memakai supinasi sah (tangan dicerminkan) di 356 frame sutil — diizinkan profil `rotasi_lengan`; perlu dinilai visual."])
    old(1, "04a_sutil_genggam_sebelum_sesudah.jpg", "lembar_lama")
    # 2 lengan
    fr = [180, 250, 500]
    mk(2, "bahu_siku_pergelangan_lengan", "Sambungan bahu–siku–pergelangan–lengan bawah", "NOT_IMPLEMENTED (tidak ada perubahan di 4.2)",
       [f"f{f}" for f in fr], pair_still(B, fr),
       [KOND_STILL, "Kontur lengan / sambungan tangan–lengan bawah TIDAK dikerjakan di 4.2 (lihat daftar belum selesai #2).",
        "Lembar ini hanya menunjukkan keadaan saat ini; perbedaan yang terlihat berasal dari pose/IK, bukan sprite lengan baru."])
    # 3 piring
    fr = [250, 282, 580]
    mk(3, "penyangga_piring", "Penyangga piring alami", "PARTIAL (pose 'support' belum dibuat)",
       [f"f{f}" for f in fr], pair_still(B, fr),
       [KOND_STILL, "Pose jari di bawah piring + ibu jari di tepi BELUM dibuat; piring masih genggam jepit tepi (rim).",
        "Yang diperbaiki: geser presentasi 0,076 m → 0,0 m (batas 0,04); tembus meja ~225 frame → 0 (proxy OBB)."])
    # 4 sendok-mulut (fase-setara: 4.1 f240 vs 4.2 f234)
    fr = [222, 234, 240, 250]
    mk(4, "sendok_ke_mulut", "Kontak sendok ke mulut", "COMPLETE (numerik); visual: tangan menutupi cekung",
       [f"f{f}" for f in fr], pair_video(B, fr),
       [KOND_VIDEO, "4.1 f240: sendok di dagu. 4.2: kontak cekung–mulut f233–235 (0,0 px / lebar cekung 35,2 px); f240 di 4.2 = fase 'kembali'.",
        "4.1 residual genggam f245–253 = 46,5–49,6 px; 4.2 = 0,0 px di setiap frame f245–253 (interaksi.json per_frame)."])
    old(4, "04b_sendok_mulut_sebelum_sesudah.jpg", "lembar_lama")
    # 5 fase makan & minum
    km = B["inter"]["props"]["sendok_jali_2"]["kontak_mulut_per_frame"]
    fr = [227, 230, 234, 236, 240, 246, 252]   # semua di shot 5 (f226-281); fase 'sendok' siklus ini jatuh di shot 4 (insert wajan)
    rows = pair_video(B, fr)
    mk(5, "fase_makan", "Fase aksi makan (benchmark, satu siklus suapan shot 5)", "COMPLETE",
       [f"f{f} {km.get(str(f), ['?'])[0]}" for f in fr], rows,
       [KOND_VIDEO, "Label kolom = fase 4.2 dari interaksi.json (sendok->angkat->dekat_mulut->kontak->tarik->kembali->istirahat; mulut kunyah k23-38). Fase 'sendok' siklus ini ada di shot 4 (insert), tidak terlihat.",
        "Baris 4.1 TIDAK sefase: 4.1 memakai satu kurva angkat–turun tanpa fase eksplisit dan jadwal berbeda."], cell_h=760)
    kt = Gn["inter"]["props"]["teh_dimas_0"]["kontak_mulut_per_frame"]
    fr = [486, 497, 503, 510, 517, 530]
    mk(5, "fase_minum", "Fase aksi minum (generalisasi, Sri shot 5)", "COMPLETE",
       [f"f{f} {kt.get(str(f), ['?'])[0]}" for f in fr], pair_video(Gn, fr),
       [KOND_VIDEO, "Fase 4.2: angkat->dekat_mulut->kontak (teguk, gelas dimiringkan)->kembali->istirahat. Bibir gelas–mulut maks 0,2 px / 64 px.",
        "Pergelangan Sri: 4.1 maks 74,8° (f500–501); 4.2 maks 43,8° (f500 = 29,7°, f501 = 39,2°)."], cell_h=760)
    # 6 serah-terima
    fr = [300, 318, 325, 330]
    mk(6, "serah_terima_gelas", "Serah-terima gelas sadar-tabrakan (generalisasi)", "COMPLETE dengan WARN (titik 'mepet' 6,2 cm dari meja)",
       [f"f{f}" for f in fr], pair_still(Gn, fr),
       [KOND_STILL, "4.2: proxy OBB 56 objek; jarak bebas titik 6,2 cm, lintasan 0,39 cm (status mepet → WARN), residual 0/0 px.",
        "Layout kedua tanpa kode khusus: uji ke-3 f398 (jarak bebas 0,49 m, status ok) — lihat lembar 06b."])
    fr = [383, 398, 413]
    sheet(out / "06b_serah_terima_uji3.jpg", "06b. Serah-terima di layout kedua (cerita ke-3, tidak ada versi 4.1)",
          "Status: COMPLETE (serah_terima PASS, serah_terima_tabrakan PASS)", [f"f{f}" for f in fr],
          [(f"Phase 4.2\n{U['bid']}\ngraded", [graded42(U, f) for f in fr])], 900,
          ["Sumber: frame render final + grading video (tanpa subtitle). Tidak ada pembanding 4.1 (cerita baru)."])
    # 7 duduk
    fr = [500, 560, 590]
    mk(7, "anatomi_duduk", "Anatomi tokoh duduk (Sri)", "PARTIAL (pivot lutut + celah dudukan; bentuk kaki belum diperhalus)",
       [f"f{f}" for f in fr], pair_still(Gn, fr),
       [KOND_STILL, "4.2: regangan betis memakai pivot di garis lutut (sebelumnya dasar kanvas → kaki hilang di dudukan tinggi).",
        "Celah dudukan dari jejak kotak dudukan. Bentuk kaki duduk masih sederhana (lihat masalah visual #3)."])
    old(7, "04d_kaki_duduk_bangku_sebelum_sesudah.jpg", "lembar_lama")
    # 8 blush
    fr = [420, 475]
    mk(8, "mask_wajah_blush_sri", "Mask wajah: blush Sri meluber ke hijab", "COMPLETE",
       [f"f{f} closeup" for f in fr], pair_still(Gn, fr),
       [KOND_STILL, "4.2: chars.skin_mask per tampak; blush dikalikan mask kulit di generator sprite (chars VERSION 20), bukan koreksi gambar.",
        "Uji generator: 0 piksel lapisan khusus-kulit di luar kulit (tests/test_phase42*.py)."], cell_h=1000)
    old(8, "04c_blush_mask_kulit_sebelum_sesudah.jpg", "lembar_lama")
    # 9 siluet & transisi tampak
    fr = [282, 615, 760]
    mk(9, "siluet_transisi_profil", "Siluet tokoh & transisi tampak/profil", "NOT_IMPLEMENTED (tidak ada pekerjaan baru di 4.2)",
       [f"f{f}" for f in fr], pair_still(B, fr),
       [KOND_STILL, "Tidak ada generator siluet atau perubahan transisi tampak di 4.2; tokoh baru uji ke-3 memakai parameter yang sudah ada.",
        "Bukti tampak tokoh baru (Harjo, Wulan): lembar 09b."])
    fr = [30, 165, 250, 500, 700]
    sheet(out / "09b_tokoh_cerita_ketiga.jpg", "09b. Tokoh cerita ke-3 (Harjo, Wulan) — tampak depan/3/4/belakang",
          "Tidak ada versi 4.1", [f"f{f}" for f in fr], [(f"Phase 4.2\n{U['bid']}\ngraded", [graded42(U, f) for f in fr])], 900,
          ["Sumber: frame render final + grading video (tanpa subtitle)."])
    # 10 establishing & penutup
    mk(10, "establishing_penutup_benchmark", "Komposisi establishing & penutup (benchmark)", "COMPLETE dengan WARN (komposisi_pita)",
       ["f60 establishing", "f760 penutup"], pair_still(B, [60, 760]),
       [KOND_STILL, "KAMERA BERBEDA: bl_camsolve.frame_shots (okupansi, headroom, letak vertikal per tipe shot) mengubah kamera 4.2."])
    mk(10, "establishing_penutup_generalisasi", "Komposisi establishing & penutup (generalisasi interior)", "COMPLETE dengan WARN (komposisi_pita)",
       ["f60 establishing", "f590 penutup"], pair_still(Gn, [60, 590]),
       [KOND_STILL, "KAMERA + INTERIOR BERBEDA. Okupansi establishing 0,10 → 0,24; plafon kosong medium 40% → 20% (kamera.json).",
        "WARN tersisa: two-shot 9:16 'dibatasi lebar kelompok' — alasan per kunci kamera di 18_camera_composition/."])
    # 11 interior
    fr = [135, 200, 300, 560]
    mk(11, "interior", "Kualitas lingkungan interior (dalam_rumah)", "PARTIAL (art direction sebagian)",
       [f"f{f}" for f in fr], pair_still(Gn, fr),
       [KOND_STILL, "4.2: dalam_rumah dibangun ulang (wainscot, lis, plint, drop ceiling, kusen jati, teralis, gorden, roster, bufet, kipas plafon, sinar jendela).",
        "Belum: variasi tekstur dinding, jejak pemakaian perabot (masalah visual #10). Kamera juga berubah."])
    # 12 hero asset
    fr = [212, 222, 250]
    mk(12, "hero_asset_makanan_alat_masak", "Hero asset: nasi goreng, sutil, wajan, piring, gerobak", "NOT_IMPLEMENTED (aset 4.1 dipakai)",
       [f"f{f}" for f in fr], pair_still(B, fr),
       [KOND_STILL, "Aset hero benchmark TIDAK ditingkatkan di 4.2. Satu-satunya perubahan: permukaan kerja gerobak aluminium brushed",
        "(warna 0,32, kasar 0,6) untuk menghilangkan kedip pantulan; pantulan EEVEE global SCREEN → PROBE."])
    # 13 cahaya
    mk(13, "cahaya_kedalaman_benchmark", "Cahaya sinematik & kedalaman atmosfer (benchmark)", "PARTIAL (preset lama; tidak ada preset baru)",
       ["f330", "f500", "f700"], pair_still(B, [330, 500, 700]),
       [KOND_STILL, "Preset atmosfer yang ada (atmosfer.py) dipakai; api kompor ±25 W → ±8 W; pantulan PROBE (kilap logam/kaca sedikit kurang tajam)."])
    mk(13, "cahaya_kedalaman_generalisasi", "Cahaya interior (generalisasi)", "PARTIAL",
       ["f420", "f560"], pair_still(Gn, [420, 560]),
       [KOND_STILL, "Interior mendapat sinar matahari jendela; palet 'hangat'. Palet 'sejuk' tidak dirender."])
    # 14 raw vs graded (4.2, frame render final yang sama)
    rows = []
    cols = []
    for s, f in ((B, 330), (Gn, 420), (U, 500)):
        cols.append(f"{s['k']} f{f}")
    rows = [("RAW\nframe render\nfinal Colab", [raw42(B, 330), raw42(Gn, 420), raw42(U, 500)]),
            ("GRADED\ngrading video\n(tanpa subtitle)", [graded42(B, 330), graded42(Gn, 420), graded42(U, 500)])]
    mk(14, "raw_vs_graded", "Raw vs graded (Phase 4.2, frame yang sama)", "bukti (tidak ada perubahan grading di 4.2)",
       cols, rows, ["Kondisi IDENTIK: render dan kamera sama; hanya grading berbeda. Build: " + ", ".join(s["bid"] for s in S),
                    "Raw/graded 4.1 (build 4.1) disalin terpisah sebagai referensi: 14_phase41_*."])
    for n in ("01_final_render.jpg", "02_raw_render.jpg", "03_solid_view.jpg"):
        if (P41 / n).exists():
            link(P41 / n, out / f"14_phase41_{n}")
    # 15 kedip & crush
    old(15, "04f_kedip_meja_gerobak_sebelum_sesudah.jpg", "lembar_lama")
    old(15, "04g_kedip_jendela_zfighting_sebelum_sesudah.jpg", "lembar_lama")
    fr = [463, 464, 465, 466, 467]
    a, b = vframes(B, "41", fr), vframes(B, "42", fr)
    crop = (0, 760, 1080, 1520)

    def cropped(p, tag):
        q = tmp / "crop" / f"{tag}_{Path(p).name}"
        q.parent.mkdir(parents=True, exist_ok=True)
        if not q.exists():
            Image.open(p).crop(crop).save(q)
        return q
    sheet(out / "15_kedip_f463-467_benchmark.jpg", "15. Kedip & black crush: benchmark f463–467 (area gerobak, potongan y 760–1520)",
          "Status: flicker_temporal PASS (global 1,02); qa_kedip WARN 1,05 di f465 (ambang 1,0; 4.1: 1,58)",
          [f"f{f}" for f in fr],
          [(f"Phase 4.1\n{B['b41']}", [cropped(a[f], "41") for f in fr]), (f"Phase 4.2\n{B['bid']}", [cropped(b[f], "42") for f in fr])],
          380,
          [KOND_VIDEO + " Potongan area yang sama.",
           "Akar masalah 4.2: pantulan ruang-layar meja aluminium (kasar 0,25) berbintik/menyala hanya di GPU Colab; z-fighting gorden–kaca (uji ke-3)."],
          aspect=1080 / 760)
    T.append((15, "Kedip f463–467 benchmark", "lihat 14_post_render_QA.json", "15_kedip_f463-467_benchmark.jpg", ()))
    # index
    L = ["# Bukti visual sebelum/sesudah (Phase 4.1 → 4.2)", "",
         "Setiap lembar memuat label kondisi. **Build 4.1 dan 4.2 berbeda di banyak variabel sekaligus** (kamera/komposisi, interior, "
         "interaksi, material). Tidak ada lembar A/B satu-variabel; perbandingan ini bukan bukti kausal satu perubahan.", "",
         "- Lembar `NN_*.jpg` (baru): kolom/baris memakai still lokal ter-grading (pipeline `make.py --frame` yang sama untuk 4.1 dan 4.2) "
         "atau frame dari video final kedua versi; sumbernya tertulis di setiap lembar.",
         "- `NN_lembar_lama__04x_*.jpg`: lembar yang sudah dibuat selama Phase 4.2 (judul/label di dalam lembar).",
         "- Still full-resolution 4.2 ada di `06/07/08_stills_*` (raw + graded). Still full-resolution 4.1 yang dipakai: `_sumber_phase41/`.",
         "- **Solid/debug view 4.2: TIDAK TERSEDIA** (tidak dirender di 4.2; tidak diganti dengan solid view 4.1). "
         "Solid view 4.1 disertakan hanya sebagai `14_phase41_03_solid_view.jpg` berlabel 4.1.", "",
         "| # | Topik | Status 4.2 | File |", "|---|---|---|---|"]
    topics = {1: "Genggam sutil anatomis & pergelangan", 2: "Bahu–siku–pergelangan–lengan bawah", 3: "Penyangga piring alami",
              4: "Kontak sendok–mulut", 5: "Fase makan & minum", 6: "Serah-terima gelas sadar-tabrakan", 7: "Anatomi duduk",
              8: "Mask wajah (blush Sri)", 9: "Siluet & transisi profil", 10: "Establishing & penutup", 11: "Interior",
              12: "Hero asset", 13: "Cahaya & kedalaman atmosfer", 14: "Raw vs graded", 15: "Kedip & black crush"}
    files = sorted(p.name for p in out.glob("*.jpg"))
    for no, nm in topics.items():
        st = "; ".join(sorted({t[2] for t in T if t[0] == no})) or "lihat lembar lama"
        fl = ", ".join(f"`{f}`" for f in files if f.startswith(f"{no:02d}_") or f.startswith(f"{no:02d}b_"))
        L.append(f"| {no} | {nm} | {st} | {fl} |")
    (out / "00_INDEX.md").write_text("\n".join(L) + "\n")
    src = out / "_sumber_phase41"
    for s in (B, Gn):
        for p in sorted(s["s41"].glob("*.png")):
            link(p, src / f"{s['k']}_{p.name}")


# ---------------------------------------------------------------- video perbandingan & diagnostik
def ass_time(f):
    t = (f - 1) / FPS
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def komparasi():
    """04: 4.1 | 4.2 berdampingan, resolusi asli tiap sisi (2160×1920), sinkron per frame, audio 4.2"""
    B, Gn, _ = S
    parts = []
    for s in (B, Gn):
        dst = PKG / "_tmp_frames" / f"kompar_{s['k']}.mp4"
        lab41 = f"PHASE 4.1  {s['b41']}".replace(":", r"\:")
        lab42 = f"PHASE 4.2  {s['bid']}".replace(":", r"\:")
        fc = (f"[0:v]drawtext=fontfile={FONTB}:text='{lab41}':x=24:y=24:fontsize=44:fontcolor=white:box=1:boxcolor=black@0.6[a];"
              f"[1:v]drawtext=fontfile={FONTB}:text='{lab42}':x=24:y=24:fontsize=44:fontcolor=white:box=1:boxcolor=black@0.6[b];"
              f"[a][b]hstack=inputs=2,drawtext=fontfile={FONT}:text='{s['judul'].replace(':', '')}  f%{{eif\\:n+1\\:d}}':"
              f"x=(w-tw)/2:y=h-80:fontsize=40:fontcolor=yellow:box=1:boxcolor=black@0.6[v]")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(s["v41"]), "-i", str(s["v42"]), "-filter_complex", fc,
                        "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(dst)], check=True)
        parts.append(dst)
        log("komparasi", s["k"])
    lst = PKG / "_tmp_frames" / "kompar.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    out = PKG / f"04_comparison_phase41_vs_phase42_{B['bid']}_{Gn['bid']}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", "-metadata",
                    f"comment=kiri=4.1 ({B['b41']},{Gn['b41']}) kanan=4.2 ({B['bid']},{Gn['bid']}); audio=4.2", str(out)], check=True)
    log("komparasi ->", out.name)


DIAG = {  # (nama, f0, f1) dari data build (fase/transisi), rentang tertulis di label
    "benchmark": [("sutil_aduk_shot3_insert4", 159, 225), ("sendok_suap_kontak_f233-235_taruh_f254_shot5", 226, 281),
                  ("sutil_taruh_f458_kedip_meja_shot7", 458, 540)],
    "generalization": [("ambil_teh_f131-143_shot2", 115, 165), ("serah_terima_f325_shot3", 280, 355),
                       ("minum_kontak_f503-516_shot5", 483, 544), ("taruh_teh_f549-561_shot6", 545, 585)],
    "third_story": [("sendok_suap_kontak_f85-90_taruh_f118_kedip_jendela_shot2", 61, 145), ("ambil_kopi_f162-174_shot3", 146, 200),
                    ("serah_terima_f398_shot4", 353, 428), ("minum_kontak_f631-649_shot6", 605, 675)],
}


def diagnostik():
    segs = []
    for s in S:
        for nm, a, b in DIAG[s["k"]]:
            # anotasi fase per frame (ASS) dari interaksi.json
            ev = []
            for x in s["inter"]["fase"]:
                lo, hi = max(a, x["f0"]), min(b, x["f1"])
                if lo <= hi:
                    ev.append((lo, hi, f"{x['benda'].rsplit('_', 2)[0]}/{x['tokoh']}: {x['fase']}"))
            for n, p in s["inter"]["props"].items():
                km = p.get("kontak_mulut_per_frame", {})
                fr = [f for f in sorted(int(k) for k in km) if a <= f <= b]
                for ph, g in groupby(fr, key=lambda f: km[str(f)][0]):
                    g = list(g)
                    ev.append((g[0], g[-1], f"{n.rsplit('_', 2)[0]} mulut: {ph}"))
            for h in s["inter"].get("serah_terima", []):
                if a <= h["frame"] <= b:
                    ev.append((h["frame"] - 3, h["frame"] + 3, f"SERAH-TERIMA f{h['frame']} {h['pemberi']} -> {h['penerima']}"))
            ass = PKG / "_tmp_frames" / f"diag_{s['k']}_{a}.ass"
            hdr = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
                   "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, "
                   "StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                   "Style: F,Noto Sans,34,&H0000FFFF,&H000000FF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,3,2,0,7,20,20,150,1\n\n"
                   "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
            lines = []
            for i, (lo, hi, t) in enumerate(sorted(ev)):
                lines.append(f"Dialogue: 0,{ass_time(lo - a + 1)},{ass_time(hi - a + 2)},F,,20,20,{150 + 44 * (i % 6)},,{t}")
            ass.write_text(hdr + "\n".join(lines) + "\n")
            lab = f"{s['k']} {s['bid']}  f{a}-{b}  {nm}".replace(":", r"\:")
            dst = PKG / "_tmp_frames" / f"diag_{s['k']}_{a}.mp4"
            fc = (f"[0:v]trim=start_frame={a - 1}:end_frame={b},setpts=PTS-STARTPTS,"
                  f"subtitles={ass}:fontsdir=/usr/share/fonts/truetype/noto,"
                  f"drawtext=fontfile={FONT}:text='{lab}':x=20:y=20:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.7,"
                  f"drawtext=fontfile={FONTB}:text='f%{{eif\\:n+{a}\\:d}}':x=20:y=70:fontsize=48:fontcolor=yellow:box=1:boxcolor=black@0.7[v];"
                  f"[0:a]atrim=start={(a - 1) / FPS}:end={b / FPS},asetpts=PTS-STARTPTS[au]")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(s["v42"]), "-filter_complex", fc, "-map", "[v]", "-map", "[au]",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
                            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(dst)], check=True)
            segs.append((s, nm, a, b, dst))
            log("diag", s["k"], nm)
    lst = PKG / "_tmp_frames" / "diag.txt"
    lst.write_text("".join(f"file '{x[4]}'\n" for x in segs))
    out = PKG / f"05_interaction_diagnostic_{'_'.join(s['bid'] for s in S)}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart",
                    "-metadata", "comment=cuplikan video final 4.2; " + "; ".join(f"{x[0]['bid']} f{x[2]}-{x[3]} {x[1]}" for x in segs),
                    str(out)], check=True)
    L = ["# 05 — Video diagnostik interaksi", "",
         f"File: `{out.name}` (1080×1920, 30 fps, audio asli segmen). Isinya **cuplikan dari video final 4.2** "
         "(bukan render terpisah). Setiap segmen menampilkan cerita, build ID, rentang frame, nomor frame asli (kuning), dan "
         "anotasi fase per frame dari `interaksi.json` (fase aksi, fase mulut, serah-terima).", "",
         "| # | Cerita | Build | Frame | Isi | Mulai di detik |", "|---|---|---|---|---|---|"]
    t = 0.0
    for i, (s, nm, a, b, _) in enumerate(segs, 1):
        L.append(f"| {i} | {s['judul']} | {s['bid']} | f{a}–{b} | {nm} | {t:.1f} |")
        t += (b - a + 1) / FPS
    (PKG / "05_interaction_diagnostic_INDEX.md").write_text("\n".join(L) + "\n")
    log("diagnostik ->", out.name)


# ---------------------------------------------------------------- bukti teknis
def teknis(ver):
    files_b = sorted({p for g in M.SOURCE_GLOBS for p in ROOT.glob(g) if p.is_file()})
    files_t = sorted({p for g in M.TOOL_GLOBS for p in ROOT.glob(g) if p.is_file()})
    src_h, n = M.source_hash()
    tool_h = M._hash_files(files_t, ROOT)
    build_t = min(os.path.getmtime(s["b"] / "manifest.json") for s in S)
    with open(PKG / "10_source_code.txt", "w") as f:
        f.write("# Source code lengkap Phase 4.2 (keadaan saat paket dibuat; tidak diubah sesudah build final)\n")
        f.write(f"# source_hash (engine/*.py, engine/sets/*.py, engine/colab/*.py, make.py; {n} file) = {src_h}\n")
        for s in S:
            f.write(f"#   manifest {s['k']:15s} {s['bid']}  source_hash = {s['man']['inputs']['source_hash']}  "
                    f"{'COCOK' if s['man']['inputs']['source_hash'] == src_h else 'BERBEDA'}\n")
        f.write(f"# tools_hash sekarang (scripts/dev/*.py, tests/*.py; TIDAK menentukan build ID) = {tool_h}\n")
        for s in S:
            th = s["man"]["inputs"].get("tools_hash")
            f.write(f"#   manifest {s['k']:15s} tools_hash = {th}  {'COCOK' if th == tool_h else 'BERBEDA'}\n")
        later = [p for p in files_t if os.path.getmtime(p) > build_t]
        f.write("#   alat yang diubah SESUDAH build final (hanya alat paket/klip, bukan render): "
                + (", ".join(str(p.relative_to(ROOT)) for p in later) or "tidak ada") + "\n")
        f.write("#\n# Daftar file: [BUILD]=masuk source_hash, [ALAT]=validator/paket/uji. sha256 lengkap, jumlah baris\n")
        for grp, fl in (("BUILD", files_b), ("ALAT", files_t)):
            for p in fl:
                t = p.read_text()
                f.write(f"#   [{grp}] {p.relative_to(ROOT)}  {sha(p)}  {t.count(chr(10))} baris\n")
        for grp, fl in (("BUILD", files_b), ("ALAT", files_t)):
            for p in fl:
                f.write(f"\n\n{'=' * 110}\n# FILE [{grp}]: {p.relative_to(ROOT)}\n# sha256: {sha(p)}\n{'=' * 110}\n")
                f.write(p.read_text())
    # 11 konfigurasi
    arc = ROOT / "backups" / "phase41_final_P4-4b69684991_20261127_1031.tar.gz"
    old = {}
    with tarfile.open(arc) as tf:
        for s in S:
            try:
                old[s["k"]] = tf.extractfile(f"stories/{s['dir']}/story.yaml").read().decode()
            except KeyError:
                old[s["k"]] = None
    with open(PKG / "11_configuration.txt", "w") as f:
        f.write("# Konfigurasi ketiga cerita final Phase 4.2\n")
        for s in S:
            m = s["man"]
            f.write(f"\n\n{'#' * 110}\n# {s['judul']}  —  stories/{s['dir']}  —  build {s['bid']}\n{'#' * 110}\n")
            f.write(f"\n## story.yaml (sha256 {sha(s['story'].dir / 'story.yaml')})\n")
            f.write((s["story"].dir / "story.yaml").read_text())
            f.write("\n\n## manifest.inputs\n" + json.dumps(m["inputs"], indent=1, ensure_ascii=False))
            f.write("\n\n## pengaturan render & keluaran (manifest.outputs, unik)\n")
            seen = set()
            for o in m.get("outputs", []):
                key = json.dumps(o.get("settings"), sort_keys=True, ensure_ascii=False)
                if (o["kind"], key) not in seen:
                    seen.add((o["kind"], key))
                    f.write(f"- {o['kind']}: {key}\n")
            f.write("\n## daftar shot (plan.json)\n")
            for x in s["plan"]["shots"]:
                f.write(f"- shot {x['n']}: f{x['f0']}-{x['f1']} {x['kamera']} subjek={x.get('subjek')} ke_arah={x.get('ke_arah')}\n")
            f.write("\n## koreksi grading per shot (grade_auto.json, build ini)\n")
            ga = json.loads((s["b"] / "grade_auto.json").read_text())
            for k, v in sorted(ga["shots"].items(), key=lambda kv: int(kv[0])):
                f.write(f"- shot {k}: override {v['override']}  hitam raw {v['laporan']['raw']['hitam']} -> graded {v['laporan']['akhir']['hitam']}\n")
            f.write("\n## diff story.yaml Phase 4.1 (backup) -> Phase 4.2\n")
            if old.get(s["k"]) is None:
                f.write("(cerita baru di 4.2 — tidak ada versi 4.1)\n")
            else:
                f.write("".join(difflib.unified_diff(old[s["k"]].splitlines(True), (s["story"].dir / "story.yaml").read_text().splitlines(True),
                                                     "phase41/story.yaml", "phase42/story.yaml")) or "(tidak ada perubahan)\n")
    # 12 validasi
    val = {"catatan": "status validator final per cerita. File validasi.json / validasi_interaksi.json di build/ berasal dari build LAMA "
                      "(4.1 atau perantara) dan tidak dipakai; hanya validasi_p42.json (build final) dan validasi_kamera.json.",
           "status_yang_dipakai": ["PASS", "WARN", "FAIL", "NOT_TESTED", "NOT_APPLICABLE"]}
    for s in S:
        vi = json.loads((s["b"] / "validasi_p42.json").read_text())
        vk = json.loads((s["b"] / "validasi_kamera.json").read_text())
        sb = json.loads((s["b"] / "sebidang.json").read_text())
        assert vi["build_id"] == s["bid"] and vk["build_id"] == s["bid"]
        val[s["k"]] = {"build_id": s["bid"], "interaksi": vi, "kamera": vk,
                       "sebidang_zfighting": {"tol_m": sb["tol_m"], "jumlah_pasangan": sb["jumlah"], "pasangan": sb["pasangan"],
                                              "catatan": "diukur pada scene.blend build final (scripts/dev/cek_sebidang.py); sisa pasangan tidak diperbaiki"}}
    pv41 = {}
    for s in S[:2]:
        p = s["b"] / "validasi_interaksi.json"
        d = json.loads(p.read_text())
        if d.get("build_id") == s["b41"]:
            pv41[s["k"]] = {"build_id": d["build_id"], "status_ringkas": d["status_ringkas"], "status": d["status"],
                            "lompatan_benda_di_potongan_kamera_m": d.get("lompatan_benda_di_potongan_kamera_m")}
    val["pembanding_phase41_validator_lama"] = pv41
    (PKG / "12_validation_results.json").write_text(json.dumps(val, indent=1, ensure_ascii=False))
    # 13 regresi
    reg = json.loads((P42 / "14_regression_tests.json").read_text())
    (PKG / "13_regression_tests.json").write_text(json.dumps(
        {"catatan": "dijalankan SESUDAH render final; plan.json ketiga cerita diverifikasi tidak berubah (cmp)",
         "regresi": reg, "unittest_phase42_log": (P42 / "14_unittest_phase42.log").read_text().splitlines()}, indent=1, ensure_ascii=False))
    # 14 QA pasca-render
    qa = {"catatan": "qa_render.py (frame lengkap/kembar, alpha, durasi A/V, black crush, clipping, flicker temporal, sinkron dialog) dan "
                     "qa_kedip.py (kedip per shot) pada video final; lip-sync perseptual NOT_TESTED (butuh penilaian manusia)"}
    for s in S:
        kk = {"benchmark": "benchmark", "generalization": "generalisasi", "third_story": "uji3"}[s["k"]]
        qa[s["k"]] = {"build_id": s["bid"], "video": f"{s['vid']}_{s['bid']}.mp4", "video_sha256": sha(s["v42"]),
                      "qa_render": json.loads((P42 / f"_qa_render_{kk}_{s['bid']}.json").read_text()),
                      "qa_kedip": json.loads((P42 / f"_qa_kedip_{kk}_{s['bid']}.json").read_text())}
    q41 = {}
    for nm in ("benchmark_P4-4b69684991", "generalisasi_P4-21e3aadc90"):
        p = P41 / f"_qa_render_{nm}.json"
        if p.exists():
            q41[nm] = json.loads(p.read_text())
    qa["pembanding_phase41"] = q41
    (PKG / "14_post_render_QA.json").write_text(json.dumps(qa, indent=1, ensure_ascii=False))
    # 15 provenance
    pv = {"catatan": "provenance per frame/potongan render final + checksum video + identitas scene/source/config",
          "verifikasi_paket": ver,
          "build_dibuang_selama_gate_E": {
              "benchmark": ["P4-555dd710c7 (kedip meja; source berubah)", "P4-71837de932 (source berubah: PROBE)", "P4-d61be635aa (dihentikan 240/860; z-fighting)"],
              "generalization": ["P4-da5e095e8a (provenance PASS, source berubah)", "P4-92a110fd6f (source berubah)",
                                 "P4-2d0645d14d percobaan pertama: sesi Colab dipangkas server saat unggah (tidak ada frame)"],
              "third_story": ["P4-3b9aa5db79 (gagal audio: suasana tidak dikenal)", "P4-888954b55c (QA kedip FAIL 5,52: z-fighting)"]}}
    for s in S:
        fj = json.loads((s["b"] / "frames_penuh" / "frames.json").read_text())
        vc = json.loads((s["b"] / "video_checksum.json").read_text())["video"]
        vsha = sha(s["v42"])
        pv[s["k"]] = {"build_id": s["bid"], "provenance": json.loads((s["b"] / f"provenance_1_{s['plan']['end']}.json").read_text()),
                      "frames_json_skema": fj.get("skema"), "frames_json_catatan": fj.get("catatan"),
                      "frame": fj["frame"],
                      "video_checksum_final": [v for v in vc if v.get("sha256") == vsha],
                      "video_checksum_riwayat_build_lama": [{k: v.get(k) for k in ("jenis", "build_id", "sha256", "dibuat")} for v in vc if v.get("sha256") != vsha],
                      "video_sha256_disk": vsha,
                      "scene_build": s["man"]["scene_build"]}
    (PKG / "15_build_provenance.json").write_text(json.dumps(pv, indent=1, ensure_ascii=False))
    # 16-20
    for s in S:
        link(s["b"] / "manifest.json", PKG / "16_build_manifests" / f"manifest_{s['k']}_{s['bid']}.json")
        link(s["b"] / "interaksi.json", PKG / "17_interaction_reports" / f"interaksi_{s['k']}_{s['bid']}.json")
        link(s["b"] / "validasi_p42.json", PKG / "17_interaction_reports" / f"validasi_interaksi_{s['k']}_{s['bid']}.json")
        link(s["b"] / "kamera.json", PKG / "18_camera_composition" / f"kamera_komposisi_{s['k']}_{s['bid']}.json")
        link(s["b"] / "validasi_kamera.json", PKG / "18_camera_composition" / f"validasi_kamera_{s['k']}_{s['bid']}.json")
        vi = json.loads((s["b"] / "validasi_p42.json").read_text())
        inter = s["inter"]
        col = {"build_id": s["bid"], "catatan": "tabrakan benda vs proxy OBB dunia statis, kontak permukaan ambil/letak (dicatat terpisah, "
                                                "tidak disembunyikan), kontak semantik cekung/bibir ↔ mulut (rasio thd ukuran benda), serah-terima",
               "validator": {k: v for k, v in vi["status"].items() if k.split(":")[0] in
                             ("tabrakan_dunia", "kontak_mulut", "serah_terima", "serah_terima_tabrakan", "tembus", "dudukan",
                              "pergelangan_fase_kontak", "cabang_siku", "transisi_kepemilikan", "melayang", "genggam")},
               "blocking_tabrakan": inter.get("blocking_tabrakan"), "serah_terima": inter.get("serah_terima"),
               "per_benda": {n: {k: p.get(k) for k in ("tabrakan_dunia_per_frame", "kontak_permukaan_ambil_letak_per_frame",
                                                       "kontak_mulut_per_frame")} for n, p in inter["props"].items()},
               "sebidang_zfighting": json.loads((s["b"] / "sebidang.json").read_text())}
        (PKG / "19_collision_semantic_contact").mkdir(exist_ok=True)
        (PKG / "19_collision_semantic_contact" / f"tabrakan_kontak_{s['k']}_{s['bid']}.json").write_text(json.dumps(col, indent=1, ensure_ascii=False))
        tr = {"build_id": s["bid"],
              "catatan": "fisik → presentasi: skala benda (harus konstan), geser presentasi/blocking (dibatasi geser_maks profil), "
                         "lompatan posisi benda di potongan kamera (DICATAT, tanpa ambang lolos/gagal), transisi kepemilikan",
              "lompatan_benda_di_potongan_kamera_m": vi.get("lompatan_benda_di_potongan_kamera_m"),
              "lompatan_layar_benda_px_dalam_shot": vi["ringkasan"].get("lompatan_layar_benda_px"),
              "transisi_kepemilikan": inter.get("transisi_kepemilikan"),
              "validator": {k: v for k, v in vi["status"].items() if k.split(":")[0] in ("skala_fisik_benda", "geser_presentasi", "temporal")},
              "per_benda": {n: {k: p.get(k) for k in ("skala_presentasi_min_max", "geser_blocking_presentasi_maks_m", "geser_maks_profil_m",
                                                      "frame_geser_di_atas_batas", "geser_presentasi_per_frame", "skala_min_profil")}
                            for n, p in inter["props"].items()}}
        if s["b41"]:
            d41 = val["pembanding_phase41_validator_lama"].get(s["k"])
            tr["pembanding_phase41"] = {"build_id": s["b41"], "lompatan_benda_di_potongan_kamera_m": d41 and d41["lompatan_benda_di_potongan_kamera_m"]}
        (PKG / "20_presentation_transform").mkdir(exist_ok=True)
        (PKG / "20_presentation_transform" / f"fisik_ke_presentasi_{s['k']}_{s['bid']}.json").write_text(json.dumps(tr, indent=1, ensure_ascii=False))
    log("teknis selesai")


def blend():
    """scene.blend final di-pack (semua gambar eksternal masuk) — disimpan sebagai SALINAN; file build tidak diubah"""
    d = PKG / "21_scene_packed"
    d.mkdir(exist_ok=True)
    for s in S:
        out = d / f"scene_packed_{s['k']}_{s['bid']}.blend"
        before = sha(s["b"] / "scene.blend")
        expr = ("import bpy; bpy.ops.file.pack_all(); "
                f"bpy.ops.wm.save_as_mainfile(filepath=r'{out}', copy=True, compress=True)")
        subprocess.run(["blender", "-b", str(s["b"] / "scene.blend"), "--python-expr", expr], check=True,
                       capture_output=True, text=True)
        assert sha(s["b"] / "scene.blend") == before, "scene.blend berubah!"
        log("blend", out.name, out.stat().st_size // 2**20, "MB; sumber sha256", before[:16])


def checksum():
    rows = {}
    for p in sorted(PKG.rglob("*")):
        if p.is_file() and "_tmp_frames" not in p.parts and p.name != "99_CHECKSUMS.json":
            rows[str(p.relative_to(PKG))] = {"sha256": sha(p), "bytes": p.stat().st_size}
    (PKG / "99_CHECKSUMS.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    log("checksum", len(rows), "file")


if __name__ == "__main__":
    steps = sys.argv[1:] or ["verifikasi", "video", "still", "banding", "komparasi", "diagnostik", "teknis", "blend", "checksum"]
    PKG.mkdir(parents=True, exist_ok=True)
    ver = verifikasi()
    for st in steps:
        if st == "verifikasi":
            continue
        if st == "teknis":
            teknis(ver)
        else:
            globals()[st]()
