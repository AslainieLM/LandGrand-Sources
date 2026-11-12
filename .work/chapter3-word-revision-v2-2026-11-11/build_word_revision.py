from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import json
import re
import sys

from lxml import etree
from PIL import Image


BASELINE = "b4b153e68a6ca4c62725303d8f157b1d03c5b8a8fbce18bd1d61837836c5ba5b"
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
}
RELATIONSHIPS = "http://schemas.openxmlformats.org/package/2006/relationships"
WP14 = "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
DOCUMENT = "word/document.xml"
REL_PART = "word/_rels/document.xml.rels"
EMU_PER_INCH = 914400

PROCEDURE = (
    "This section explains how learners will use Land Grand and how the game will save their "
    "progress. Figures 4A to 4E show the proposed procedure.",
    "Land Grand will load available progress from the device at startup. The Main Menu will "
    "offer Play, Settings, Tutorial, and Exit. Play will open the Landform Map (Figure\u00a04A).",
    "Learners will select an unlocked episode and an available level. The four episodes will cover "
    "Mountains, Hills, Plains, and Plateaus. Each episode will have three Easy, five Normal, "
    "and seven Hard levels, for a total of 60 (Figure\u00a04B).",
    "Before each level, a short lesson will introduce the landform and related rocks or minerals. "
    "Learners will move and jump with touch controls. An item pop-up will show each collected "
    "item's illustration, name, and short description. Reaching the end goal will complete the "
    "level. If time runs out or the learner falls into a pit, the game will offer Retry and Back "
    "to Main Menu (Figure\u00a04C).",
    "The game will award up to three stars using thresholds for the number of rocks collected. "
    "It will automatically save the level result on the device. Clearing all three Easy levels "
    "will unlock Normal. Clearing all five Normal levels will unlock Hard. The Result Screen "
    "will show earned stars, collected items, and a short review (Figure\u00a04D).",
    "Learners may replay or continue to the next available level. After the required levels are "
    "complete, the game will show a landform summary and unlock the next episode if available. "
    "The Completion Screen will show total stars, collected items, and a congratulatory message "
    "after all four episodes (Figure\u00a04E).",
)
PANELS = (
    ("01-launch-and-main-menu.png", "Launch and Main Menu",
     "Land Grand loads saved progress when available. The Main Menu offers Play, Settings, Tutorial, and Exit.",
     "051a95d266e2f49c34f8833ef96c281d4eacd85756a8a34d1f7f829a49a5130d"),
    ("02-select-episode-and-level.png", "Episode and Level Selection",
     "The Landform Map checks episode and level access. Each episode has three Easy, five Normal, and seven Hard levels.",
     "09b81c3b73c3e94dd4addaec8dbd1e12f81f073bf9aea95ca1417232fafea718"),
    ("03-lesson-gameplay-and-level-outcomes.png", "Lesson and Level Outcomes",
     "A lesson leads to exploration and item descriptions. The end goal completes the level. Timeout or pit fall offers Retry or Back to Main Menu.",
     "89fa8371846567f595e709ce456bc384ec771129de3342f82fa7aedb88001c37"),
    ("04-score-save-and-unlock-difficulty.png", "Scoring, Local Saving, and Difficulty Unlocks",
     "The collected rock count determines stars through thresholds. The game saves the result and unlocks Normal after three Easy levels and Hard after five Normal levels.",
     "fc7ebe0166968b40af277f1d8a2d8c98943566778d5838c19bf593ba35af887e"),
    ("05-continue-and-complete-episodes.png", "Episode Progression and Game Completion",
     "The learner continues to the next available level or sees a landform summary after finishing an episode. The Completion Screen follows all four episodes.",
     "770762f60f699dd4b0aa72ca407d9005543db94a42015063143e7cf01c208872"),
)


def q(prefix, name):
    return f"{{{NS[prefix]}}}{name}"


def paragraph_text(element):
    return "".join(element.xpath(".//w:t/text()", namespaces=NS))


def clone_text(pattern, value):
    paragraph = deepcopy(pattern)
    text_nodes = paragraph.findall(".//w:t", NS)
    assert len(text_nodes) == 1, paragraph_text(pattern)
    text_nodes[0].text = value
    return paragraph


def clone_picture(pattern, relation_id, letter, title, alt, size):
    paragraph = deepcopy(pattern)
    properties = paragraph.find("w:pPr", NS)
    assert properties.find("w:pageBreakBefore", NS) is None
    properties.insert(0, etree.Element(q("w", "pageBreakBefore")))

    inline = paragraph.find(".//wp:inline", NS)
    assert inline is not None
    width = 6 * EMU_PER_INCH
    height = round(width * size[1] / size[0])
    for extent in (inline.find("wp:extent", NS), inline.find(".//a:xfrm/a:ext", NS)):
        extent.attrib.update({"cx": str(width), "cy": str(height)})
    assert inline.find(".//a:srcRect", NS) is None
    inline.find(".//a:blip", NS).set(q("r", "embed"), relation_id)

    doc_property = inline.find("wp:docPr", NS)
    picture_property = inline.find(".//pic:cNvPr", NS)
    number = str(201 + ord(letter) - ord("A"))
    for property_element in (doc_property, picture_property):
        property_element.set("id", number)
        property_element.set("name", f"Figure 4{letter}. {title}")
    doc_property.set("descr", alt)
    for name in ("anchorId", "editId"):
        attr = f"{{{WP14}}}{name}"
        if attr in inline.attrib:
            inline.set(attr, f"{0x31A00000 + int(number):08X}")
    return paragraph


def build(source, image_dir, target):
    assert source != target and sha256(source.read_bytes()).hexdigest() == BASELINE
    with ZipFile(source) as reference:
        document = etree.fromstring(reference.read(DOCUMENT))
        relations = etree.fromstring(reference.read(REL_PART))
        body = document.find("w:body", NS)
        assert paragraph_text(body[62]) == "How the project will work"
        assert paragraph_text(body[63]).startswith("This section")
        assert body[-1].tag == q("w", "sectPr")
        assert paragraph_text(body[67]).startswith("Figure 4A.")
        assert body[66].find(".//wp:inline", NS) is not None

        content_types = etree.fromstring(reference.read("[Content_Types].xml"))
        assert any(x.get("Extension") == "png" and x.get("ContentType") == "image/png"
                   for x in content_types)
        normal, picture, caption = body[63], body[66], body[67]
        replacements = [clone_text(normal, text) for text in PROCEDURE]
        new_parts = {}
        figures = []

        for index, (file_name, title, alt, expected_hash) in enumerate(PANELS):
            letter = chr(ord("A") + index)
            path = image_dir / file_name
            png = path.read_bytes()
            assert sha256(png).hexdigest() == expected_hash, path
            with Image.open(path) as image:
                assert image.width == 2400 and round(image.info["dpi"][0]) == 400
                size = image.size
                image.verify()
            relation_id = f"rIdLandGrandProcess{letter}"
            assert not any(el.get("Id") == relation_id for el in relations)
            media_target = f"media/landgrand-process-4{letter.lower()}.png"
            etree.SubElement(relations, f"{{{RELATIONSHIPS}}}Relationship", Id=relation_id,
                             Type=f"{NS['r']}/image", Target=media_target)
            new_parts[f"word/{media_target}"] = png
            replacements.append(clone_picture(picture, relation_id, letter, title, alt, size))
            replacements.append(clone_text(caption, f"Figure 4{letter}. {title}"))
            figures.append({"figure": f"4{letter}", "source": str(path), "sha256": expected_hash})

        for old in list(body)[63:-1]:
            body.remove(old)
        for paragraph in replacements:
            body.insert(len(body) - 1, paragraph)

        modified = {
            DOCUMENT: etree.tostring(document, encoding="UTF-8", xml_declaration=True, standalone=True),
            REL_PART: etree.tostring(relations, encoding="UTF-8", xml_declaration=True, standalone=True),
        }
        assert not (set(reference.namelist()) & new_parts.keys())
        with ZipFile(target, "w", compression=ZIP_DEFLATED) as output:
            for part in reference.infolist():
                output.writestr(part, modified[part.filename] if part.filename in modified
                                else reference.read(part.filename))
            for name, contents in new_parts.items():
                output.writestr(name, contents)

    report = {
        "source_sha256": BASELINE,
        "word_sha256": sha256(target.read_bytes()).hexdigest(),
        "procedure_words": len(re.findall(r"\S+", " ".join(PROCEDURE))),
        "embedded_panels": figures,
    }
    (target.parent / "build-evidence.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "embedded_panels"}))


if __name__ == "__main__":
    build(*map(Path, sys.argv[1:]))

