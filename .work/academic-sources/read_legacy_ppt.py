"""Read retained .ppt text without modifying or launching Office.

Uses MS-CFB sectors and the current MS-PPT persist directory, not stale
strings from previous saves. Output is reading evidence, not a renderer.
"""
from pathlib import Path
import json
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
WORK = Path(__file__).parent
SOURCE = Path(r'D:\Projects\LandGrand-Sources\LandGrand\Sources\Attachments\s02 CAPSTONE chapters 1-3.ppt')
data = SOURCE.read_bytes()
u16 = lambda b, o: struct.unpack_from('<H', b, o)[0]
u32 = lambda b, o: struct.unpack_from('<I', b, o)[0]
assert data[:8] == bytes.fromhex('d0cf11e0a1b11ae1')
sector_size = 1 << u16(data, 30)

def sector(sid):
    assert sid < 0xfffffffa
    start = (sid + 1) * sector_size
    result = data[start:start + sector_size]
    assert len(result) == sector_size
    return result

fat_sectors = [x for x in struct.unpack_from('<109I', data, 76) if x < 0xfffffffa]
difat = u32(data, 68)
for _ in range(u32(data, 72)):
    values = struct.unpack('<' + 'I' * (sector_size // 4), sector(difat))
    fat_sectors.extend(x for x in values[:-1] if x < 0xfffffffa)
    difat = values[-1]
assert len(fat_sectors) == u32(data, 44)
fat = []
for sid in fat_sectors:
    fat.extend(struct.unpack('<' + 'I' * (sector_size // 4), sector(sid)))

def chain(first, table, get_sector):
    seen = set()
    chunks = []
    sid = first
    while sid < 0xfffffffa:
        assert sid not in seen and sid < len(table)
        seen.add(sid)
        chunks.append(get_sector(sid))
        sid = table[sid]
    assert sid in (0xfffffffe, 0xffffffff)
    return b''.join(chunks)

directory = chain(u32(data, 48), fat, sector)
entries = {}
for pos in range(0, len(directory), 128):
    entry = directory[pos:pos + 128]
    size = u16(entry, 64)
    if size >= 2 and entry[66] in (2, 5):
        name = entry[:size - 2].decode('utf-16le')
        length = struct.unpack_from('<Q', entry, 120)[0]
        entries[name] = (u32(entry, 116), length, entry[66])
root_start, root_size, _ = next(v for v in entries.values() if v[2] == 5)
mini_stream = chain(root_start, fat, sector)[:root_size]
mini_fat_bytes = chain(u32(data, 60), fat, sector)
mini_fat = list(struct.unpack('<' + 'I' * (len(mini_fat_bytes) // 4), mini_fat_bytes))

def stream(name):
    first, length, kind = entries[name]
    if length < u32(data, 56) and kind != 5:
        result = chain(first, mini_fat, lambda sid: mini_stream[sid * 64:(sid + 1) * 64])
    else:
        result = chain(first, fat, sector)
    assert len(result) >= length
    return result[:length]

ppt = stream('PowerPoint Document')
current = stream('Current User')

def records(buf, start=0, end=None):
    if end is None:
        end = len(buf)
    pos = start
    while pos < end:
        assert pos + 8 <= end, (pos, end)
        flags, kind, length = struct.unpack_from('<HHI', buf, pos)
        assert pos + 8 + length <= end, (pos, kind, length, end)
        yield {'offset': pos, 'version': flags & 15, 'instance': flags >> 4,
               'type': kind, 'length': length, 'payload': buf[pos + 8:pos + 8 + length]}
        pos += 8 + length

def record_at(offset):
    flags, kind, length = struct.unpack_from('<HHI', ppt, offset)
    return {'offset': offset, 'version': flags & 15, 'instance': flags >> 4,
            'type': kind, 'length': length, 'payload': ppt[offset + 8:offset + 8 + length]}

# Most recent mappings take precedence over mappings from older edit records.
edit_offset = u32(current, 16)
persist = {}
edit_count = 0
while edit_offset:
    edit = record_at(edit_offset)
    assert edit['type'] == 4085
    atom = edit['payload']
    if edit_count == 0:
        document_id = u32(atom, 16)
    directory_atom = record_at(u32(atom, 12))
    assert directory_atom['type'] == 6002
    payload = directory_atom['payload']
    pos = 0
    while pos < len(payload):
        packed = u32(payload, pos)
        pos += 4
        first, count = packed & 0xfffff, packed >> 20
        assert count > 0
        for i in range(count):
            persist.setdefault(first + i, u32(payload, pos))
            pos += 4
    edit_offset = u32(atom, 8)
    edit_count += 1
    assert edit_count < 1000

document = record_at(persist[document_id])
assert document['type'] == 1000
slide_lists = [r for r in records(document['payload']) if r['type'] == 4080]
main = [r for r in slide_lists if r['instance'] == 0]
assert len(main) == 1
slides = []
slide = None
for r in records(main[0]['payload']):
    if r['type'] == 1011:
        slide = {'slide': len(slides) + 1, 'persist_id': u32(r['payload'], 0),
                 'slide_id': u32(r['payload'], 12), 'text': [], 'shape_text': [], 'notes': []}
        slides.append(slide)
    elif r['type'] in (4000, 4008):
        assert slide is not None
        text = r['payload'].decode('utf-16le' if r['type'] == 4000 else 'cp1252')
        slide['text'].append(text)

def text_in_records(buf):
    output = []
    for r in records(buf):
        if r['type'] in (4000, 4008):
            output.append(r['payload'].decode('utf-16le' if r['type'] == 4000 else 'cp1252'))
        elif r['version'] == 15:
            output.extend(text_in_records(r['payload']))
        elif r['type'] == 0xf00d:
            output.extend(text_in_records(r['payload']))
    return output

for slide in slides:
    container = record_at(persist[slide['persist_id']])
    assert container['type'] == 1006
    slide['shape_text'] = text_in_records(container['payload'])
    atoms = [r for r in records(container['payload']) if r['type'] == 1007]
    assert len(atoms) == 1
    note_id = u32(atoms[0]['payload'], 16)
    if note_id and note_id in persist:
        notes_container = record_at(persist[note_id])
        if notes_container['type'] == 1008:
            slide['notes'] = text_in_records(notes_container['payload'])
    print(f"\n===== SLIDE {slide['slide']} (id {slide['slide_id']}) =====")
    for field in ['text', 'shape_text', 'notes']:
        if slide[field]:
            print(field.upper())
            print('\n'.join(slide[field]).replace('\r', '\n').replace('\v', '\n'))

result = {'source': str(SOURCE), 'edit_count': edit_count, 'slide_count': len(slides),
          'slide_lists': [{'instance': r['instance'], 'length': r['length']} for r in slide_lists],
          'slides': slides}
(WORK / 'guidelines-slides.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print('\nSLIDE_COUNT', len(slides), 'EDIT_COUNT', edit_count)
