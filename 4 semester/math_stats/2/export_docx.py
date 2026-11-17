from __future__ import annotations

import re
import struct
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = text.replace("`", "")
    return text.strip()


def paragraph(text: str, size: int = 22, bold: bool = False, align: str = "left") -> str:
    if not text:
        return "<w:p/>"
    alignment = {
        "left": "<w:jc w:val=\"left\"/>",
        "center": "<w:jc w:val=\"center\"/>",
        "right": "<w:jc w:val=\"right\"/>",
    }[align]
    run_props = (
        f"<w:rPr><w:rFonts w:ascii=\"Times New Roman\" w:hAnsi=\"Times New Roman\" w:cs=\"Times New Roman\"/>"
        f"<w:sz w:val=\"{size}\"/><w:szCs w:val=\"{size}\"/>{'<w:b/><w:bCs/>' if bold else ''}</w:rPr>"
    )
    safe_text = escape(text)
    return (
        f"<w:p><w:pPr>{alignment}</w:pPr><w:r>{run_props}<w:t xml:space=\"preserve\">{safe_text}</w:t></w:r></w:p>"
    )


def heading(text: str, level: int) -> str:
    sizes = {1: 32, 2: 28, 3: 24}
    return paragraph(text, size=sizes[level], bold=True)


def table_xml(rows: list[list[str]]) -> str:
    parts = [
        "<w:tbl>",
        "<w:tblPr>",
        "<w:tblBorders>",
        "<w:top w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"auto\"/>",
        "<w:left w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"auto\"/>",
        "<w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"auto\"/>",
        "<w:right w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"auto\"/>",
        "<w:insideH w:val=\"single\" w:sz=\"6\" w:space=\"0\" w:color=\"auto\"/>",
        "<w:insideV w:val=\"single\" w:sz=\"6\" w:space=\"0\" w:color=\"auto\"/>",
        "</w:tblBorders>",
        "</w:tblPr>",
    ]
    for row_index, row in enumerate(rows):
        parts.append("<w:tr>")
        for cell in row:
            parts.append("<w:tc>")
            parts.append("<w:tcPr><w:tcW w:w=\"0\" w:type=\"auto\"/></w:tcPr>")
            parts.append(paragraph(strip_inline_markdown(cell), size=21, bold=(row_index == 0)))
            parts.append("</w:tc>")
        parts.append("</w:tr>")
    parts.append("</w:tbl>")
    return "".join(parts)


def page_break() -> str:
    return "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"


def png_size(image_bytes: bytes) -> tuple[int, int]:
    if image_bytes[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Поддерживаются только PNG-изображения.")
    return struct.unpack(">II", image_bytes[16:24])


def image_paragraph(rid: str, image_bytes: bytes, docpr_id: int) -> str:
    px_width, px_height = png_size(image_bytes)
    max_width = 5_800_000
    width_emu = min(max_width, int(px_width * 9525))
    height_emu = int(width_emu * px_height / px_width)
    return f"""
<w:p>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="{WP_NS}">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:docPr id="{docpr_id}" name="Picture {docpr_id}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks noChangeAspect="1" xmlns:a="{A_NS}"/>
        </wp:cNvGraphicFramePr>
        <a:graphic xmlns:a="{A_NS}">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="{PIC_NS}">
              <pic:nvPicPr>
                <pic:cNvPr id="{docpr_id}" name="image{docpr_id}.png"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rid}" xmlns:r="{R_NS}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{width_emu}" cy="{height_emu}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
""".strip()


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        row = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        if len(row) > 1 and not all(set(cell) <= {"-", ":"} for cell in row):
            rows.append(row)
        index += 1
    return rows, index


def build_document(report_path: Path) -> tuple[str, list[tuple[str, bytes, str]]]:
    lines = report_path.read_text(encoding="utf-8").splitlines()
    variant = ""
    for line in lines:
        if line.startswith("Вариант:"):
            variant = strip_inline_markdown(line.split(":", 1)[1])
            break

    body: list[str] = [
        paragraph("Министерство науки и высшего образования Российской Федерации", size=24, align="center"),
        paragraph("Национальный исследовательский университет ИТМО", size=24, align="center"),
        paragraph("Факультет систем управления и робототехники", size=24, align="center"),
        paragraph("", size=22),
        paragraph("Математическая статистика", size=28, bold=True, align="center"),
        paragraph("", size=22),
        paragraph("Расчётно-графическая работа №1", size=32, bold=True, align="center"),
        paragraph("Описание выборки. Оценивание параметров. Доверительные интервалы", size=26, bold=True, align="center"),
        paragraph("", size=22),
        paragraph(f"Вариант: {variant}", size=26, align="center"),
        paragraph("", size=22),
        paragraph("Санкт-Петербург", size=24, align="center"),
        paragraph("2026", size=24, align="center"),
        page_break(),
    ]
    images: list[tuple[str, bytes, str]] = []
    image_index = 1
    docpr_id = 1
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("# "):
            body.append(heading(strip_inline_markdown(stripped[2:]), 1))
            i += 1
            continue
        if stripped.startswith("## "):
            body.append(heading(strip_inline_markdown(stripped[3:]), 2))
            i += 1
            continue
        if stripped.startswith("### "):
            body.append(heading(strip_inline_markdown(stripped[4:]), 3))
            i += 1
            continue
        if stripped.startswith("|"):
            rows, i = parse_table(lines, i)
            if rows:
                body.append(table_xml(rows))
            continue
        image_match = re.search(r"!\[]\(([^)]+)\)", stripped)
        if image_match:
            prefix = strip_inline_markdown(stripped[: image_match.start()]).rstrip(": ").strip()
            if prefix:
                body.append(paragraph(prefix, bold=True))
            image_path = (report_path.parent / image_match.group(1)).resolve()
            image_bytes = image_path.read_bytes()
            rid = f"rId{image_index}"
            images.append((rid, image_bytes, f"image{image_index}.png"))
            body.append(image_paragraph(rid, image_bytes, docpr_id))
            image_index += 1
            docpr_id += 1
            i += 1
            continue
        body.append(paragraph(strip_inline_markdown(stripped)))
        i += 1

    section = (
        "<w:sectPr>"
        "<w:pgSz w:w=\"11906\" w:h=\"16838\"/>"
        "<w:pgMar w:top=\"1134\" w:right=\"850\" w:bottom=\"1134\" w:left=\"1134\" "
        "w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/>"
        "</w:sectPr>"
    )
    document_xml = (
        f"<w:document xmlns:w=\"{W_NS}\" xmlns:r=\"{R_NS}\">"
        f"<w:body>{''.join(body)}{section}</w:body></w:document>"
    )
    return document_xml, images


def content_types_xml(has_images: bool) -> str:
    image_default = '<Default Extension="png" ContentType="image/png"/>' if has_images else ""
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f"{image_default}"
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )


def root_rels_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/>'
        "</Relationships>"
    )


def document_rels_xml(images: list[tuple[str, bytes, str]]) -> str:
    relations = []
    for rid, _, file_name in images:
        relations.append(
            f'<Relationship Id="{rid}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="media/{file_name}"/>'
        )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f"{''.join(relations)}"
        "</Relationships>"
    )


def write_docx(report_path: Path, out_path: Path) -> None:
    document_xml, images = build_document(report_path)
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types_xml(bool(images)))
        docx.writestr("_rels/.rels", root_rels_xml())
        docx.writestr("word/document.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + document_xml)
        docx.writestr("word/_rels/document.xml.rels", document_rels_xml(images))
        for _, image_bytes, file_name in images:
            docx.writestr(f"word/media/{file_name}", image_bytes)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    report_path = base_dir / "report.md"
    out_path = base_dir / "report.docx"
    try:
        write_docx(report_path, out_path)
        print(out_path.name)
    except PermissionError:
        fallback = base_dir / "report_updated.docx"
        write_docx(report_path, fallback)
        print(fallback.name)


if __name__ == "__main__":
    main()
