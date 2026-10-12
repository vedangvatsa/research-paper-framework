"""Build the corrected manuscript, preserving the pre-correction artifacts."""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
ARCHIVE = PAPER / "results/correction_20261005/legacy_artifacts"
SOURCE = PAPER / "linguistic_markers_paper.md"
PDF = PAPER / "linguistic_markers_paper.pdf"
BUILD = PAPER / "latex_build_corrected"


def preserve_legacy():
    manifest = ARCHIVE / "manifest.json"
    if manifest.exists():
        return
    paths = [SOURCE, PDF, PAPER / "latex_build/paper.tex", PAPER / "latex_build/paper.pdf",
             PAPER / "scripts/build_paper_tex.py"]
    hashes = {}
    for source in paths:
        relative = source.relative_to(PAPER)
        target = ARCHIVE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            raise ValueError(f"Incomplete archive needs inspection: {target}")
        shutil.copy2(source, target)
        hashes[str(relative)] = hashlib.sha256(target.read_bytes()).hexdigest()
    manifest.write_text(json.dumps(hashes, indent=2) + "\n")
    print(f"Preserved prior manuscript and PDFs in {ARCHIVE}")


def build_supplement(preamble, desktop):
    source = PAPER / "SUPPLEMENTARY_METHODS.md"
    folder = BUILD / "supplement"
    folder.mkdir(exist_ok=True)
    title, body = source.read_text().split("\n", 1)
    (folder / "body.md").write_text(body)
    converted = subprocess.run(
        ["pandoc", str(folder / "body.md"), "--standalone", "--shift-heading-level-by=-1",
         "--metadata", f"title={title.removeprefix('# ')}", "--metadata", "author=Vedang Ratan Vatsa",
         "--metadata", "date=", "--variable", "geometry:margin=1in", "--variable", "fontsize:11pt",
         "--include-in-header", str(preamble), "--output", str(folder / "supplement.tex")],
        text=True, capture_output=True, check=True)
    tex = folder / "supplement.tex"
    content = re.sub(r"\\texttt\{([^{}]*/[^{}]*)\}",
                     lambda match: "\\nolinkurl{" + match[1].replace("\\_", "_") + "}", tex.read_text())
    content = re.sub(r"(\\subsection\{[^}]+\}\\label\{[^}]+\})",
                     lambda match: "\\Needspace{" + ("12" if "Variant B" in match[0] else "5")
                     + "\\baselineskip}\n" + match[0], content)
    content = re.sub(r"(\\textbf\{(?:Hedges|Boosters|Self-mentions|Connectors)\.\}.*?)(?=\n\n)",
                     lambda match: "\\begingroup\\raggedright\n" + match[1] + "\\par\\endgroup",
                     content, flags=re.DOTALL)
    tex.write_text(content)
    compiled = subprocess.run(["tectonic", "--keep-logs", "supplement.tex"], cwd=folder,
                              capture_output=True, text=True)
    log = converted.stdout + converted.stderr + compiled.stdout + compiled.stderr
    (folder / "build.log").write_text(log)
    print(log)
    compiled.check_returncode()
    target = PAPER / "supplementary_methods.pdf"
    shutil.copy2(folder / "supplement.pdf", target)
    if desktop:
        shutil.copy2(target, Path.home() / "Desktop/high_accuracy_poor_transfer_supplement.pdf")
    print(f"Built {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-only", action="store_true")
    parser.add_argument("--desktop", action="store_true")
    args = parser.parse_args()
    preserve_legacy()
    if args.archive_only:
        return
    BUILD.mkdir(exist_ok=True)
    manuscript = SOURCE.read_text()
    title = manuscript.splitlines()[0].removeprefix("# ")
    body = manuscript[manuscript.index("## Abstract"):]
    (BUILD / "body.md").write_text(body)
    preamble = BUILD / "preamble.tex"
    preamble.write_text(
        "\\usepackage{microtype}\n\\usepackage{etoolbox}\n"
        "\\usepackage{float}\n\\usepackage{needspace}\n\\usepackage{xurl}\n"
        "\\usepackage{caption}\n\\captionsetup{font=small,labelfont=bf}\n"
        "\\AtBeginEnvironment{longtable}{\\footnotesize}\n"
        "\\hyphenpenalty=5000\n\\setlength{\\emergencystretch}{3em}\n"
    )
    command = ["pandoc", str(BUILD / "body.md"), "--standalone", "--shift-heading-level-by=-1",
               "--metadata", f"title={title}", "--metadata", "author=Vedang Ratan Vatsa",
               "--metadata", "date=", "--variable", "geometry:margin=1in",
               "--variable", "fontsize:11pt", "--variable", "colorlinks:true",
               "--variable", "urlcolor:blue", "--include-in-header", str(preamble),
               "--resource-path", str(PAPER), "--output", str(BUILD / "paper.tex")]
    converted = subprocess.run(command, cwd=PAPER, text=True, capture_output=True, check=True)
    tex = BUILD / "paper.tex"
    # Pandoc's generated graphics paths are relative to the original paper.
    content = tex.read_text()
    content = re.sub(r"(\\includegraphics\[[^\n]*\]\{)results/",
                     lambda match: match[1] + "../results/", content)
    content = re.sub(r"\\texttt\{([^{}]*/[^{}]*)\}",
                     lambda match: "\\nolinkurl{" + match[1].replace("\\_", "_") + "}", content)
    content = content.replace("\\begin{figure}", "\\begin{figure}[H]")
    content = re.sub(r"\\begin\{figure\}\[H\](?:(?!\\end\{figure\}).)*?fig4_confusion\.png",
                     lambda match: match[0].replace("[H]", "[!htbp]", 1), content, flags=re.DOTALL)
    content = content.replace("\\includegraphics[keepaspectratio,", "\\includegraphics[width=0.97\\linewidth,keepaspectratio,")
    content = re.sub(r"(\\includegraphics\[)width=0\.97\\linewidth(,[^\n]+fig4_confusion\.png)",
                     lambda match: match[1] + "width=0.65\\linewidth" + match[2], content)
    content = content.replace("\\textbf{Table ", "\\Needspace{16\\baselineskip}\n\\textbf{Table ")
    content = re.sub(r"(\\subsection\{4\.[2456][^}]+\}\\label\{[^}]+\})",
                      lambda match: "\\Needspace{20\\baselineskip}\n" + match[0], content)
    content = content.replace("\\begin{enumerate}", "\\Needspace{8\\baselineskip}\n\\begin{enumerate}")
    content = re.sub(r"(\\section\{7\. Data and Code\s+Availability\})",
                      lambda match: "\\Needspace{8\\baselineskip}\n" + match[0], content)
    content = content.replace("\\section{8. References}",
                              "\\Needspace{5\\baselineskip}\n\\section{8. References}\\begingroup\\small\\raggedright")
    content = content.replace("\\end{document}", "\\endgroup\n\\end{document}")
    content = re.sub(r"\\href\{([^}]+)\}\{([^}]+)\}",
                     lambda match: "\\href{" + match[1] + "}{\\nolinkurl{" + match[2] + "}}", content)
    content = content.replace("\\author{Vedang Ratan Vatsa}",
                              "\\author{Vedang Ratan Vatsa \\\\ \\texttt{vedangvats@gmail.com}}")
    tex.write_text(content)
    compiled = subprocess.run(["tectonic", "--keep-logs", "paper.tex"], cwd=BUILD,
                              capture_output=True, text=True)
    log = converted.stdout + converted.stderr + compiled.stdout + compiled.stderr
    (BUILD / "build.log").write_text(log)
    print(log)
    compiled.check_returncode()
    shutil.copy2(BUILD / "paper.pdf", PDF)
    if args.desktop:
        desktop = Path.home() / "Desktop"
        if not desktop.is_dir():
            raise ValueError("Desktop directory does not exist")
        shutil.copy2(PDF, desktop / "linguistic_markers_paper_corrected.pdf")
        shutil.copy2(PDF, desktop / "high_accuracy_poor_transfer.pdf")
    print(f"Built {PDF}")
    build_supplement(preamble, args.desktop)


if __name__ == "__main__":
    main()
