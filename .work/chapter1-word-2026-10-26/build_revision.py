"""Patch the editable body while preserving the user's school-format package."""
from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
import hashlib
import json
import re
from lxml import etree

ROOT = Path(__file__).resolve().parent
VAULT = Path(r'D:\Projects\LandGrand-Sources\LandGrand')
SOURCE = ROOT / 'reference.docx'
OUTPUT = VAULT / 'Manuscript' / 'Drafts' / 'Land Grand - Chapter I - Revised.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
q = lambda tag: '{' + W + '}' + tag

# Each paragraph reuses the reference pattern given in the second field.
paragraphs = [
('title', 1, 'CHAPTER I'),
('title', 2, 'INTRODUCTION'),
('intro', 3, 'This chapter presents the context, purpose, objectives, scope, and limitations of Land Grand. The proposed educational game focuses on landforms, rocks, and minerals for Grade 5 learners at Baluan Elementary School.'),
('heading', 4, 'Project Context'),
('body', 5, 'Land Grand is proposed as a supplementary resource for Science learning at home. It would give Grade 5 learners another way to study landforms, rocks, and minerals alongside printed learning materials. Its rationale draws on international guidance on educational technology, Philippine distance-learning experience, and the concerns reported by parents and teachers at Baluan Elementary School.'),
('body', 5, "International discussions of educational technology emphasize whether a tool addresses a learning need in its intended setting. UNESCO's 2023 Global Education Monitoring Report recommends considering local suitability, inclusion, evidence, and sustainability when selecting educational technology. It places learners and teachers at the centre of these decisions (UNESCO, 2023). For this project, that guidance supports examining the relationship between the proposed content, learning activities, and learners' access to devices before assuming that digital delivery improves learning."),
('body', 5, 'An exploration game offers a way to connect explanations with activities such as moving through a landscape, identifying items, and reviewing their descriptions. For Land Grand, these activities would focus on selected Science concepts rather than serve only as rewards for completing a level. Their educational value would still require evaluation. Animation, collected items, and gameplay stars alone cannot establish that learners understand the concepts presented.'),
('body', 5, "In the Philippines, distance-learning arrangements during the COVID-19 period included printed and digital modular approaches. The Department of Education's 2020 guidance allowed supplementary resources, including interactive electronic materials, and described support from household learning facilitators (Department of Education, 2020, Appendix A and Appendix B). This historical experience provides a national context for supplementing home learning. It also directs attention to the explanations available to learners and the assistance parents may provide when children use printed modules."),
('body', 5, 'Disaster-related disruption is relevant to the regional setting. DOST-PHIVOLCS documented a magnitude 7.8 earthquake offshore Sarangani on June 8, 2026 (DOST-PHIVOLCS, 2026). As of October 2026, Baluan Elementary School holds face-to-face classes, with modular learning considered a contingency if another strong earthquake or other event disrupts classroom instruction. The proposed game would therefore support supplementary home study during regular schooling and potential disruptions.'),
('body', 5, "A preliminary school survey conducted on July 7, 2026 provides local information for the project. It contains 20 parent responses and 20 teacher responses. Respondent selection was reported as randomized. The parent group covered Grades 4–6 because those grades had a scheduled parents' orientation meeting."),
('body', 5, 'The parent responses cover Grades 4, 5, and 6, with six, six, and eight records, respectively. Teacher responses cover Kindergarten and Grades 3, 4, 5, and 6, with two, four, five, five, and four records, respectively. Full-group results describe perceptions across these grades; the Grade 5 subsets are considered separately below.'),
('body', 5, 'Difficulty explaining module lessons emerged in the parent responses. Seventeen of 20 parents, or 85%, answered Yes when asked whether they had difficulty explaining lessons in modules to their child. Two answered No and one answered Maybe. These responses support considering additional explanations for home learning while recognizing that the reported difficulty was not shared by every respondent.'),
('body', 5, 'Science ratings also relate to the proposed content area. Seventeen of 20 parent ratings and 13 of 20 teacher ratings placed Science in the Difficult or Very Difficult categories. Within the smaller Grade 5 subsets, all six parent ratings and four of five teacher ratings fell in these categories. Grade 5 free-text responses included mentions of landforms, minerals, and rocks. These small subgroups provide descriptive context for the proposed focus; they do not establish the prevalence of a learning deficit among all Grade 5 learners.'),
('body', 5, 'Responses about mobile learning indicate interest in an additional resource. Fourteen of 20 parents believed that a mobile game could support printed modules; two answered No and four answered Maybe. Fifteen of 20 teachers believed that a mobile game could enhance understanding alongside modules; one answered No and four answered Maybe. These answers express expectations about a possible learning resource rather than evidence from using Land Grand.'),
('body', 5, "Access and willingness place limits on the proposed delivery format. Eighteen parents reported household access to a smartphone, tablet, or computer, while one answered No and one answered Maybe. Thirteen would allow their child to use a mobile learning game, five would not, and two were uncertain. The combined device-access question does not establish that every household has a compatible Android device available for learning. The game is consequently proposed as a supplement to existing materials and teacher guidance."),
('lead', 10, 'The survey findings and the learning-continuity context identify the following concerns and design needs. The first two are reported concerns; the remaining two are proposed responses to the learning setting:'),
('problem', 11, 'Parents reported difficulty explaining lessons in printed modules, indicating a need to consider additional explanations for home study.'),
('problem', 11, 'Parents and teachers reported perceived Science difficulty, including within the small Grade 5 subsets, supporting consideration of a focused supplementary resource.'),
('problem', 11, 'Favourable expectations about mobile learning support exploring an interactive activity that connects Science explanations with practice and review.'),
('problem', 11, 'Potential interruptions to classroom instruction create a design need for an activity that operates offline and allows learners to resume saved progress.'),
('body', 5, 'These concerns provide a reason to develop supplementary material while regular classes continue, before another disruption increases reliance on home study. Land Grand would connect short lessons with exploration, item descriptions, and review focused on the selected Science content. Its offline design and local progress records would support use across separate sessions. Developing the application would make these proposed activities available for subsequent review and evaluation; any conclusion about improved knowledge would require an appropriate study and actual results.'),
('heading', 15, 'Purpose and Description of the Project'),
('body', 16, 'The purpose of Land Grand is to support Grade 5 learners at Baluan Elementary School in studying landforms, rocks, and minerals through an offline Android exploration game. It is intended for supplementary use at home alongside printed learning materials and teacher guidance.'),
('body', 16, 'The proposed game contains four episodes covering Mountains, Hills, Plains, and Plateaus. Before each level, the learner would read a short lesson about the landform and selected rocks and minerals. The learner would then control an explorer character, move through a two-dimensional environment, and collect items. Each collected item would display its name and a short description, linking the activity to the content introduced in the lesson.'),
('body', 16, 'After a level, the game would display the collected items, a short review, and up to three gameplay stars. Learners could replay completed content or continue to the next available level. Progress would be saved on the device for later sessions. The project combines explanation, exploration, collection, and review for a defined audience and content area. Its proposed value lies in this connection between learning material and activity, while its effect on knowledge remains to be evaluated.'),
('heading', 17, 'Objectives of the Project'),
('body', 18, 'The objectives define the application deliverables intended to address the reported concerns and design needs. The general objective is to develop Land Grand, an interactive exploration game for enhancing Grade 5 learners\u2019 knowledge of landforms, rocks, and minerals at Baluan Elementary School. The planned project completion window is November–December 2026.'),
('lead', 18, 'Specifically, the project seeks to complete the following deliverables within that planned window:'),
('objective', 11, 'Provide a short lesson before every level and display the name and a short description of each collected rock or mineral to support explanations of the covered concepts.'),
('objective', 11, 'Develop four landform episodes covering Mountains, Hills, Plains, and Plateaus, with selected rocks and minerals relevant to the intended Grade 5 content.'),
('objective', 11, 'Implement touch-controlled movement, jumping, exploration, item collection, and an end-of-level review as interactive activities that supplement printed learning materials.'),
('objective', 11, "Enable offline single-player use on Android 10 and above, with automatic local saving and loading of the learner's name, unlocked episodes, completed levels, stars, and collected items."),
('heading', 23, 'Scope and Limitations of the Project'),
('body', 24, 'This section defines the proposed application, its coverage, and its boundaries. Development concerns supplementary Science learning for Grade 5 learners at Baluan Elementary School, with project completion planned for November–December 2026.'),
('subheading', 25, 'Scope'),
('nested', 26, 'Land Grand is proposed as a single-player Android game developed using Unity and C#, with Piskel and Clip Studio Paint for graphical assets. The application would use simple two-dimensional graphics, large touch buttons, background music, and sound effects. Its proposed coverage includes the following:'),
('scope', 28, 'Four episodes representing Mountains, Hills, Plains, and Plateaus, together with selected rocks and minerals associated with the covered content.'),
('scope', 28, 'Easy, Normal, and Hard difficulty modes with 3, 5, and 7 levels per episode, respectively, for a proposed total of 60 levels across four episodes.'),
('scope', 28, 'Short lessons before each level, item names and descriptions during collection, and review material after completion.'),
('scope', 28, 'Touch controls for moving and jumping, with exploration and collection challenges involving obstacles, traps, pitfalls, and time limits.'),
('scope', 28, 'Sequential progression through difficulty modes and episodes, with replay, continuation to available levels, a landform summary, and a final completion screen.'),
('scope', 28, 'Up to three gameplay stars after a level, with detailed award and completion criteria to be specified during development.'),
('scope', 28, 'A Main Menu offering Play, Settings, Tutorial, and Exit, and a Landform Map for selecting unlocked episodes.'),
('scope', 28, "Automatic local saving and loading of the player's name, unlocked episodes, completed levels, earned stars, and collected rocks and minerals."),
('scope', 28, 'Offline operation on Android phones and tablets running Android 10 and above. The declared minimum targets are 2 GB RAM and 300 MB free storage; actual compatibility remains subject to device testing.'),
('subheading', 33, 'Limitations'),
('nested', 34, 'The proposed application and the interpretation of the preliminary survey are subject to the following boundaries:'),
('limit', 36, 'The intended learners are in Grade 5 at Baluan Elementary School. The preliminary survey also includes other grades; its full-group figures cannot be treated as Grade 5-only findings.'),
('limit', 36, 'Content is limited to the four selected landforms and selected related rocks and minerals rather than all Earth Science topics. Detailed content and competency alignment require validation.'),
('limit', 36, 'The game excludes multiplayer, online features, online accounts, cloud storage, websites, and an administrator panel.'),
('limit', 36, 'Progress remains on the device being used. The proposed application provides no centralized teacher monitoring or shared learner-record system.'),
('limit', 36, 'Learning activities exclude separate quiz screens, GPS features, and real-world scanning.'),
('limit', 36, 'The application supplements printed materials and teacher guidance. Gameplay stars, collected items, and completed levels do not independently measure learning gains.'),
('limit', 36, 'The preliminary survey describes perceptions and expectations. It does not establish the effectiveness of Land Grand; conclusions about learning outcomes require a defined evaluation method and actual results.'),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

with ZipFile(SOURCE) as archive:
    original = {item.filename: archive.read(item.filename) for item in archive.infolist()}
    infos = archive.infolist()
assert sha(SOURCE.read_bytes()) == '8701feed03dc35bf065cba7b20911eb7251335b14eee6e0ab58d3317962b72d7'
tree = etree.fromstring(original['word/document.xml'])
body = tree.find('w:body', NS)
templates = [p for p in body.findall('w:p', NS) if ''.join(p.itertext()).strip()]
# Select by displayed text, excluding formatting whitespace in an XML node.
templates = [p for p in body.findall('w:p', NS) if ''.join(p.xpath('.//w:t/text()', namespaces=NS)).strip()]
assert len(templates) == 41
section = deepcopy(body.find('w:sectPr', NS))
section_before = etree.tostring(section, method='c14n', exclusive=True)

def paragraph(role, index, text):
    template = templates[index-1]
    p = etree.Element(q('p'))
    properties = template.find('w:pPr', NS)
    if properties is not None:
        p.append(deepcopy(properties))
    props = p.find('w:pPr', NS)
    if props is None:
        props = etree.SubElement(p, q('pPr'))
    if role in ('heading', 'subheading', 'lead') and props.find('w:keepNext', NS) is None:
        # Element order follows CT_PPr: keep controls precede spacing/indents.
        props.insert(0, etree.Element(q('keepNext')))
    if role in ('problem', 'objective', 'scope', 'limit') and props.find('w:keepLines', NS) is None:
        props.insert(0, etree.Element(q('keepLines')))
    run = etree.SubElement(p, q('r'))
    source_runs = template.findall('w:r', NS)
    source_run = next((r for r in source_runs if r.find('w:t', NS) is not None), source_runs[0])
    runprops = source_run.find('w:rPr', NS)
    if runprops is not None:
        run.append(deepcopy(runprops))
    node = etree.SubElement(run, q('t'))
    node.text = text
    return p

for child in list(body):
    body.remove(child)
for record in paragraphs:
    body.append(paragraph(*record))
body.append(section)
assert etree.tostring(body.find('w:sectPr', NS), method='c14n', exclusive=True) == section_before
patched = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUTPUT, 'w') as archive:
    for item in infos:
        archive.writestr(item, patched if item.filename == 'word/document.xml' else original[item.filename])
with ZipFile(OUTPUT) as archive:
    assert archive.testzip() is None
    preserved = [name for name in original if name != 'word/document.xml' and archive.read(name) == original[name]]
    assert len(preserved) == len(original)-1

text_all = '\n\n'.join(text for _, _, text in paragraphs)
assert all(term not in text_all for term in ('[confirmed', 'P-01', 'O-01', 'TODO', 'CSV', '[['))
assert sum(role == 'objective' for role,_,_ in paragraphs) == 4
headings = [text for role,_,text in paragraphs if role == 'heading']
assert headings == ['Project Context', 'Purpose and Description of the Project', 'Objectives of the Project', 'Scope and Limitations of the Project']
word_count = lambda s: len(re.findall(r"\b[\w]+(?:[’'–-][\w]+)*\b", s))
context = text_all.split('Project Context\n\n',1)[1].split('\n\nPurpose and Description',1)[0]
audit = {'output':str(OUTPUT), 'reference_sha256':sha(SOURCE.read_bytes()), 'output_sha256':sha(OUTPUT.read_bytes()), 'paragraphs':len(paragraphs), 'words':word_count(text_all), 'context_words':word_count(context), 'preserved_parts':preserved, 'headings':headings, 'specific_objectives':4}
(ROOT/'build-audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
(ROOT/'chapter-paragraphs.json').write_text(json.dumps(paragraphs, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT/'revised-body.txt').write_text(text_all, encoding='utf-8')
print(json.dumps(audit, indent=2))
