"""Check PDF content, links, page bounds and the preserved artifact snapshot."""

import hashlib
import json
import re
import unicodedata
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw


PAPER = Path(__file__).resolve().parents[1]
BUILD = PAPER / "latex_build_corrected"


def main():
    pdf = PAPER / "linguistic_markers_paper.pdf"
    document = pymupdf.open(pdf)
    text = "\n".join(page.get_text(sort=True) for page in document)
    links = {link["uri"] for page in document for link in page.get_links() if "uri" in link}
    manuscript = (PAPER / "linguistic_markers_paper.md").read_text()
    reference_urls = set(re.findall(r"\]\((https://[^)]+)\)", manuscript))
    assert reference_urls <= links, reference_urls - links
    for value in ["74,513", "149,026", "95.99%", "90.38%", "94.82%", "3.60%", "71,831", "2,682", "3,288", "71,225", "53.89%", "11.73%", "68.91%", "8,319", "98,907"]:
        assert value in text, value
    for stale in ["95.69%", "October 2024", "2403.19074", "CBO9781139524599"]:
        assert stale not in text, stale
    compact_text = re.sub(r"\s+", "", unicodedata.normalize("NFKC", text))
    assert "../results/" not in compact_text
    for corrected_fact in ("on5October2026(UTC)", "Authoridentitieswerenotretrieved.",
                           "retaininginternalapostrophes", "notpubliclyreleased", "SupplementaryMethods"):
        assert corrected_fact in compact_text, corrected_fact
    assert "becausethoselabelsareunavailable" not in compact_text
    for leaked in ("reviewer-objection", "FACTUAL_AUDIT.md", "This research draft needs", "You are a scientific researcher"):
        assert leaked not in text, leaked
    assert len(re.findall(r"Figure\s+[1-4]:", text)) == 4
    assert document.metadata["author"].startswith("Vedang Ratan Vatsa")
    assert document.metadata["title"].startswith("High Accuracy, Poor Transfer")
    assert not re.search(r"Overfull|Missing character|Underfull", (BUILD / "build.log").read_text())

    outside = []
    for page in document:
        for word in page.get_text("words"):
            x0, y0, x1, y1, value, *_ = word
            if min(x0, y0) < 0 or x1 > page.rect.width + 1 or y1 > page.rect.height + 1:
                outside.append({"page": page.number+1, "text": value})
    assert not outside, outside

    archive = PAPER / "results/correction_20261005/legacy_artifacts"
    for name, expected in json.loads((archive / "manifest.json").read_text()).items():
        assert hashlib.sha256((archive / name).read_bytes()).hexdigest() == expected, name
    desktop = Path.home() / "Desktop/linguistic_markers_paper_corrected.pdf"
    assert pdf.read_bytes() == desktop.read_bytes()
    assert pdf.read_bytes() == (Path.home() / "Desktop/high_accuracy_poor_transfer.pdf").read_bytes()

    supplement_path = PAPER / "supplementary_methods.pdf"
    supplement = pymupdf.open(supplement_path)
    supplement_text = "\n".join(page.get_text(sort=True) for page in supplement)
    supplement_compact = re.sub(r"\s+", "", unicodedata.normalize("NFKC", supplement_text))
    for value in ("results/full_verification_20261005/revision4/", "S1.Textprocessing", "S2.Wordlists",
                  "S3.Foldassignment", "S4.Configuredgenerationprompts", "S5.Versionsandartifactlocations",
                  "e57f64187974277726a3417ca6f181ec5403676c717672eef6a748a7b20e0106"):
        assert value in supplement_compact, value
    assert not re.search(r"Overfull|Missing character|Underfull", (BUILD / "supplement/build.log").read_text())
    for page in supplement:
        for x0, y0, x1, y1, value, *_ in page.get_text("words"):
            assert min(x0, y0) >= 0 and x1 <= page.rect.width + 1 and y1 <= page.rect.height + 1, value
    assert supplement_path.read_bytes() == (Path.home() / "Desktop/high_accuracy_poor_transfer_supplement.pdf").read_bytes()

    previews = BUILD / "qa_pages"
    previews.mkdir(exist_ok=True)
    tiles = []
    for page in document:
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(1, 1), alpha=False)
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        image.thumbnail((360, 500))
        tile = Image.new("RGB", (380, 525), "#e5e7eb")
        tile.paste(image, ((380-image.width)//2, 20))
        ImageDraw.Draw(tile).text((12, 505), f"Page {page.number+1}", fill="black")
        tiles.append(tile)
    sheet = Image.new("RGB", (380*3, 525*((len(tiles)+2)//3)), "white")
    for i, tile in enumerate(tiles):
        sheet.paste(tile, ((i % 3)*380, (i//3)*525))
    sheet.save(previews / "contact_sheet.png")
    report = {"pages": len(document), "reference_urls_verified": len(reference_urls),
              "figure_captions": 4, "tex_layout_warnings": 0, "text_outside_page": outside,
              "legacy_archive_unchanged": True, "desktop_copy_matches": True,
              "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
              "supplement_pages": len(supplement), "supplement_tex_layout_warnings": 0,
              "supplement_sha256": hashlib.sha256(supplement_path.read_bytes()).hexdigest()}
    (BUILD / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
