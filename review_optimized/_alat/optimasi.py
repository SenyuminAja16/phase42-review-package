"""Salinan ramah-akses untuk reviewer (Phase 4.2): semua file keluaran < 800 KB.
Hanya MEMBACA artefak asli di repo (tidak mengubah/mengganti apa pun), tidak merender ulang, tidak menyentuh engine.
  .venv/bin/python <repo>/review_optimized/_alat/optimasi.py
Keluaran: <repo>/review_optimized/ (stills_jpg/, before_after_jpg/, provenance_split/, contact_sheets/, 00_INDEX.md, index.json)"""
import hashlib
import io
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "review_optimized"
LIMIT = 800 * 1024 - 1024            # < 800 KB dengan margin 1 KB
FONT = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONTB = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FPS = 30
STORIES = {"06_stills_benchmark": ("benchmark", "P4-486e18fc49"),
           "07_stills_generalization": ("generalization", "P4-2d0645d14d"),
           "08_stills_third_story": ("third_story", "P4-b1767c3b5e")}
# video asli: Release phase42-final (file yang sama ada di review_package lokal, bukan di repo karena > 100 MB)
VID_SRC = REPO.parent / "review_package"
VIDEOS = [("01_benchmark_phase42_P4-486e18fc49.mp4", "benchmark", "P4-486e18fc49", 5),
          ("02_generalization_phase42_P4-2d0645d14d.mp4", "generalization", "P4-2d0645d14d", 5),
          ("03_third_story_phase42_P4-b1767c3b5e.mp4", "third_story", "P4-b1767c3b5e", 5),
          ("05_interaction_diagnostic_P4-486e18fc49_P4-2d0645d14d_P4-b1767c3b5e.mp4", "diagnostic", "3 build", 3)]
REL = "https://github.com/SenyuminAja16/phase42-review-package/releases/download/phase42-final/"
INDEX = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def font(n, b=False):
    return ImageFont.truetype(FONTB if b else FONT, n)


def save_jpeg(im, dst, q_hi=92, q_lo=70):
    """kualitas tertinggi yang < LIMIT pada resolusi asli; bila q_lo pun terlalu besar, perkecil 10% per langkah"""
    im = im.convert("RGB")
    scale = 1.0
    while True:
        cur = im if scale == 1.0 else im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        for q in range(q_hi, q_lo - 1, -2):
            buf = io.BytesIO()
            cur.save(buf, "JPEG", quality=q, optimize=True, progressive=True, subsampling="4:4:4" if q >= 90 else "4:2:0")
            if buf.tell() < LIMIT:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(buf.getvalue())
                return {"kualitas_jpeg": q, "skala": round(scale, 3), "resolusi": [cur.width, cur.height], "bytes": buf.tell()}
        scale *= 0.9


def stills():
    for d, (key, bid) in STORIES.items():
        raw_names = {p.name.replace("_raw.png", "") for p in (REPO / d / "raw").glob("*.png")}
        for p in sorted((REPO / d / "graded").glob("*.png")):
            im = Image.open(p)
            tag = p.name.replace("_graded.png", "")
            dst = OUT / "stills_jpg" / key / (tag + "_graded.jpg")
            r = save_jpeg(im, dst)
            f, s = tag.split("_")[0][1:], tag.split("_")[1][1:]
            INDEX.append({"jenis": "still_graded", "optimasi": str(dst.relative_to(OUT)), "asli": f"{d}/graded/{p.name}",
                          "asli_raw": f"{d}/raw/{tag}_raw.png" if tag in raw_names else None,
                          "cerita": key, "build_id": bid, "frame": int(f), "shot": int(s), "asli_sha256": sha(p),
                          "asli_bytes": p.stat().st_size, **r})
        print("stills", key)
    for p in sorted((REPO / "09_before_after" / "_sumber_phase41").glob("*.png")):
        key, rest = p.name.split("_", 1)
        f, bid = rest.replace(".png", "").split("_")
        dst = OUT / "stills_jpg" / "phase41_reference" / p.name.replace(".png", ".jpg")
        r = save_jpeg(Image.open(p), dst)
        INDEX.append({"jenis": "still_phase41_referensi", "optimasi": str(dst.relative_to(OUT)),
                      "asli": f"09_before_after/_sumber_phase41/{p.name}", "cerita": key, "build_id": bid,
                      "frame": int(f[1:]), "asli_sha256": sha(p), "asli_bytes": p.stat().st_size, **r})


def sheets():
    for p in sorted((REPO / "09_before_after").glob("*.jpg")):
        dst = OUT / "before_after_jpg" / p.name
        if p.stat().st_size < LIMIT:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
            im = Image.open(p)
            r = {"kualitas_jpeg": "asli (disalin)", "skala": 1.0, "resolusi": [im.width, im.height], "bytes": p.stat().st_size}
        else:
            r = save_jpeg(Image.open(p), dst)
        INDEX.append({"jenis": "lembar_before_after", "optimasi": str(dst.relative_to(OUT)), "asli": f"09_before_after/{p.name}",
                      "asli_sha256": sha(p), "asli_bytes": p.stat().st_size, **r})
    print("sheets")


def split_json(obj, base, name, parts, limit=LIMIT):
    """tulis obj ke base/name.json; bila > limit, pecah dict/list menjadi potongan berurutan"""
    txt = json.dumps(obj, indent=1, ensure_ascii=False)
    if len(txt.encode()) < limit:
        (base / f"{name}.json").write_text(txt)
        parts.append(f"{name}.json")
        return
    if isinstance(obj, dict):
        items = list(obj.items())
        chunk, n = {}, 1
        for k, v in items:
            trial = dict(chunk, **{k: v})
            if chunk and len(json.dumps(trial, indent=1, ensure_ascii=False).encode()) >= limit:
                ks = list(chunk)
                split_json(chunk, base, f"{name}_bagian{n:02d}_{ks[0]}-{ks[-1]}", parts, limit)
                chunk, n = {}, n + 1
            chunk[k] = v
        if chunk:
            ks = list(chunk)
            split_json(chunk, base, f"{name}_bagian{n:02d}_{ks[0]}-{ks[-1]}", parts, limit)
    else:
        raise SystemExit(f"tidak bisa memecah {name}")


def provenance():
    src = REPO / "15_build_provenance.json"
    d = json.loads(src.read_text())
    base = OUT / "provenance_split"
    base.mkdir(parents=True, exist_ok=True)
    parts = []
    split_json({k: d[k] for k in ("catatan", "verifikasi_paket", "build_dibuang_selama_gate_E")}, base, "00_ringkasan", parts)
    for key in ("benchmark", "generalization", "third_story"):
        s = d[key]
        split_json({"build_id": s["build_id"], "provenance": s["provenance"]}, base, f"{key}_01_provenance_laporan", parts)
        split_json({"build_id": s["build_id"], "video_sha256_disk": s["video_sha256_disk"],
                    "video_checksum_final": s["video_checksum_final"],
                    "video_checksum_riwayat_build_lama": s["video_checksum_riwayat_build_lama"],
                    "scene_build": s["scene_build"]}, base, f"{key}_02_video_dan_scene", parts)
        fr = s["frame"]
        keys = sorted(fr, key=int)
        step = 150
        for i in range(0, len(keys), step):
            ks = keys[i:i + step]
            split_json({"build_id": s["build_id"], "skema": s["frames_json_skema"], "catatan": s["frames_json_catatan"],
                        "frame": {k: fr[k] for k in ks}}, base, f"{key}_03_frame_{int(ks[0]):04d}-{int(ks[-1]):04d}", parts)
    # bukti utuh: gabungan potongan == asli
    re = {"catatan": None, "verifikasi_paket": None, "build_dibuang_selama_gate_E": None}
    chk = json.loads((base / "00_ringkasan.json").read_text())
    re.update(chk)
    for key in ("benchmark", "generalization", "third_story"):
        a = json.loads((base / f"{key}_01_provenance_laporan.json").read_text())
        b = json.loads((base / f"{key}_02_video_dan_scene.json").read_text())
        frames = {}
        sk = ct = None
        for p in sorted(base.glob(f"{key}_03_frame_*.json")):
            c = json.loads(p.read_text())
            frames.update(c["frame"])
            sk, ct = c["skema"], c["catatan"]
        re[key] = {"build_id": a["build_id"], "provenance": a["provenance"], "frames_json_skema": sk, "frames_json_catatan": ct,
                   "frame": frames, "video_checksum_final": b["video_checksum_final"],
                   "video_checksum_riwayat_build_lama": b["video_checksum_riwayat_build_lama"],
                   "video_sha256_disk": b["video_sha256_disk"], "scene_build": b["scene_build"]}
    ok = json.dumps(re, sort_keys=True) == json.dumps(d, sort_keys=True)
    for p in parts:
        q = base / p
        INDEX.append({"jenis": "provenance_potongan", "optimasi": str(q.relative_to(OUT)), "asli": "15_build_provenance.json",
                      "asli_sha256": sha(src), "bytes": q.stat().st_size, "gabungan_sama_dengan_asli": ok})
    print("provenance", len(parts), "file; gabungan identik:", ok)
    if not ok:
        raise SystemExit("pemecahan provenance tidak identik")


def tc(f):
    t = (f - 1) / FPS
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def contact(video, key, bid, every, seg_map=None):
    """lembar kontak berurutan: 1 dari tiap `every` frame, label nomor frame + timecode (+ frame cerita asli untuk diagnostik)"""
    src = VID_SRC / video
    cols, rows = (5, 4) if key == "diagnostic" else (6, 4)
    tw, th = (324, 576) if key == "diagnostic" else (270, 480)
    per = cols * rows
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-vf",
                        f"select='not(mod(n\\,{every}))',scale={tw}:{th}:flags=lanczos", "-vsync", "0",
                        str(Path(td) / "t_%05d.png")], check=True)
        thumbs = sorted(Path(td).glob("t_*.png"))
        frames = [1 + i * every for i in range(len(thumbs))]
        n_sheets = (len(thumbs) + per - 1) // per
        lab_h, head = 52, 90
        for si in range(n_sheets):
            sub = list(zip(frames, thumbs))[si * per:(si + 1) * per]
            W, H = cols * tw + (cols + 1) * 6, head + rows * (th + lab_h + 6) + 6
            im = Image.new("RGB", (W, H), (22, 22, 24))
            dr = ImageDraw.Draw(im)
            f0, f1 = sub[0][0], sub[-1][0]
            title = f"{video}  |  lembar {si + 1}/{n_sheets}  |  frame video {f0}-{f1}, tiap {every} frame"
            dr.text((10, 8), title, font=font(24, True), fill=(255, 255, 255))
            dr.text((10, 44), f"build {bid}  |  timecode = (frame-1)/30 fps  |  thumbnail {tw}x{th} dari video final (1080x1920)",
                    font=font(20), fill=(220, 200, 120))
            for i, (f, p) in enumerate(sub):
                x = 6 + (i % cols) * (tw + 6)
                y = head + (i // cols) * (th + lab_h + 6)
                im.paste(Image.open(p).convert("RGB"), (x, y))
                lab = f"f{f}  {tc(f)}"
                extra = ""
                if seg_map:
                    seg = next((s for s in seg_map if s["v0"] <= f <= s["v1"]), None)
                    if seg:
                        extra = f"{seg['cerita']} f{seg['a'] + f - seg['v0']}"
                dr.text((x + 4, y + th + 2), lab, font=font(22, True), fill=(255, 230, 120))
                if extra:
                    dr.text((x + 4, y + th + 26), extra, font=font(18), fill=(200, 200, 200))
            dst = OUT / "contact_sheets" / key / f"{Path(video).stem}_lembar{si + 1:02d}_f{f0:04d}-{f1:04d}.jpg"
            r = save_jpeg(im, dst, q_hi=88, q_lo=60)
            INDEX.append({"jenis": "lembar_kontak_video", "optimasi": str(dst.relative_to(OUT)), "asli": video,
                          "asli_url": REL + video, "asli_sha256": sha(src), "build_id": bid, "frame_video": [f0, f1],
                          "langkah_frame": every, "timecode": [tc(f0), tc(f1)], **r})
    print("contact", key, n_sheets)


def diag_map():
    """segmen video diagnostik dari 05_interaction_diagnostic_INDEX.md -> rentang frame video + frame cerita"""
    segs, v = [], 1
    for line in (REPO / "05_interaction_diagnostic_INDEX.md").read_text().splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) > 6 and c[1].isdigit():
            a, b = (int(x) for x in c[4].lstrip("f").replace("–", "-").split("-"))
            segs.append({"cerita": {"Satu Bungkus Lagi": "bench", "Teh Sore untuk Ibu": "gen"}.get(c[2], "uji3"),
                         "build": c[3], "a": a, "b": b, "v0": v, "v1": v + b - a})
            v += b - a + 1
    return segs


def index_md():
    (OUT / "index.json").write_text(json.dumps(INDEX, indent=1, ensure_ascii=False))
    big = [e for e in INDEX if e.get("bytes", 0) >= LIMIT]
    by = {}
    for e in INDEX:
        by.setdefault(e["jenis"], []).append(e)
    L = ["# review_optimized — salinan ramah-akses untuk reviewer", "",
         "Folder ini **hanya berisi salinan turunan** agar dapat dibuka lewat integrasi GitHub (batas praktis ~1 MB per file). "
         "**Semua file di sini < 800 KB.** Artefak asli di root repo dan video di Release `phase42-final` **tidak diubah, diganti, atau dihapus**. "
         "Tidak ada render ulang; engine tidak disentuh. Bila ada keraguan kualitas, file asli yang berlaku.", "",
         f"- Jumlah file turunan: {len(INDEX)}; file ≥ 800 KB: {len(big)}.",
         "- Pemetaan lengkap mesin-baca (file turunan → file asli, SHA-256 asli, frame, shot, build ID, kualitas JPEG, resolusi): `index.json`.",
         "- Skrip pembuat: `_alat/optimasi.py` (dapat dijalankan ulang).", "",
         "## Isi", "",
         "| Folder | Isi | Jumlah |", "|---|---|---|",
         f"| `stills_jpg/benchmark/`, `generalization/`, `third_story/` | Still **graded** (render final Colab + grading video, tanpa subtitle) → JPEG resolusi asli 1080×1920 | {len(by.get('still_graded', []))} |",
         f"| `stills_jpg/phase41_reference/` | Still Phase 4.1 yang dipakai lembar before–after (build 4.1, berlabel) | {len(by.get('still_phase41_referensi', []))} |",
         f"| `before_after_jpg/` | Semua lembar before–after; yang sudah < 800 KB disalin apa adanya | {len(by.get('lembar_before_after', []))} |",
         f"| `provenance_split/` | `15_build_provenance.json` dipecah per cerita: laporan provenance, video & scene, frame per 150 | {len(by.get('provenance_potongan', []))} |",
         f"| `contact_sheets/` | Lembar kontak berurutan video final (tiap 5 frame) dan video diagnostik (tiap 3 frame), dengan nomor frame & timecode | {len(by.get('lembar_kontak_video', []))} |", "",
         "Catatan:",
         "- Still **raw** (PNG mentah) tidak dikonversi; aslinya di `0X_stills_*/raw/`. Kolom `asli_raw` di tabel menunjuk ke file raw dengan frame yang sama (kosong untuk 4 frame cerita ke-3 yang hanya dibuat graded untuk lembar 06b/09b).",
         "- `provenance_split/`: menggabungkan kembali semua potongan menghasilkan JSON **identik** dengan `15_build_provenance.json` (diverifikasi skrip).",
         "- Lembar kontak diagnostik: label kuning = frame & timecode **video diagnostik**; label abu = cerita dan **frame asli cerita** (lihat `05_interaction_diagnostic_INDEX.md`).",
         "- File `.blend` di `21_scene_packed/` (17–48 MB) tidak dapat diperkecil tanpa mengubah isinya; tidak disertakan di sini.", ""]
    L += ["## Still graded", "", "| File JPEG | Asli PNG | Cerita | Build | Frame | Shot | Kualitas | Resolusi | KB |", "|---|---|---|---|---|---|---|---|---|"]
    for e in by.get("still_graded", []):
        L.append(f"| `{e['optimasi']}` | `{e['asli']}` | {e['cerita']} | {e['build_id']} | {e['frame']} | {e['shot']} | q{e['kualitas_jpeg']} | "
                 f"{e['resolusi'][0]}×{e['resolusi'][1]} | {e['bytes'] // 1024} |")
    L += ["", "## Still Phase 4.1 (referensi)", "", "| File JPEG | Asli PNG | Build | Frame | KB |", "|---|---|---|---|---|"]
    for e in by.get("still_phase41_referensi", []):
        L.append(f"| `{e['optimasi']}` | `{e['asli']}` | {e['build_id']} | {e['frame']} | {e['bytes'] // 1024} |")
    L += ["", "## Lembar before–after", "", "| File | Asli | Kualitas | Resolusi | KB (asli → turunan) |", "|---|---|---|---|---|"]
    for e in by.get("lembar_before_after", []):
        L.append(f"| `{e['optimasi']}` | `{e['asli']}` | {e['kualitas_jpeg']} | {e['resolusi'][0]}×{e['resolusi'][1]} | {e['asli_bytes'] // 1024} → {e['bytes'] // 1024} |")
    L += ["", "## Provenance terpecah", "", "| File | KB |", "|---|---|"]
    for e in by.get("provenance_potongan", []):
        L.append(f"| `{e['optimasi']}` | {e['bytes'] // 1024} |")
    L += ["", "## Lembar kontak video", "", "| File | Video asli (Release) | Build | Frame video | Timecode | Langkah | KB |", "|---|---|---|---|---|---|---|"]
    for e in by.get("lembar_kontak_video", []):
        L.append(f"| `{e['optimasi']}` | [{e['asli'][:40]}…]({e['asli_url']}) | {e['build_id']} | {e['frame_video'][0]}–{e['frame_video'][1]} | "
                 f"{e['timecode'][0]}–{e['timecode'][1]} | {e['langkah_frame']} | {e['bytes'] // 1024} |")
    (OUT / "00_INDEX.md").write_text("\n".join(L) + "\n")
    print("index", len(INDEX), "entri; >= limit:", len(big))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for sub in ("stills_jpg", "before_after_jpg", "provenance_split", "contact_sheets"):
        shutil.rmtree(OUT / sub, ignore_errors=True)
    stills()
    sheets()
    provenance()
    for v, k, b, e in VIDEOS:
        contact(v, k, b, e, diag_map() if k == "diagnostic" else None)
    index_md()
