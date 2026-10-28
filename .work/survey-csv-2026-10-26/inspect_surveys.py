"""Inspect supplied survey exports without printing response-level identifiers."""
from pathlib import Path
from collections import Counter
import csv
import io
import json
import re

ROOT = Path(__file__).resolve().parent
WORD_INSPECTION = ROOT.parent / 'tally-import-2026-10-26/inspection.json'
word_tables = {b['number']: b['rows'] for b in json.loads(WORD_INSPECTION.read_text(encoding='utf-8'))['blocks'] if b['kind'] == 'table'}
result = {'files': {}, 'word_tally_mismatches': []}
for name, first_question, first_rating, closed_table, rating_table in [
    ('Parent.csv', 5, 15, 1, 2), ('Teacher.csv', 6, 16, 3, 4)
]:
    raw = (ROOT / name).read_bytes()
    rows = list(csv.reader(io.StringIO(raw.decode('utf-8-sig'), newline='')))
    header, records = rows[0], rows[1:]
    assert len(records) == 20
    assert all(len(record) == len(header) for record in records)
    grades = dict(Counter(record[2].strip() for record in records))
    dates = dict(Counter(record[0].split(' ', 1)[0] for record in records))
    personal_fields = {label: sum(bool(row[i].strip()) for row in records)
                       for i, label in enumerate(header) if label.startswith(('Name', 'Email'))}
    schools = dict(Counter(row[3].strip() for row in records)) if name == 'Teacher.csv' else None
    closed = []
    for question in range(10):
        column = first_question + question
        counts = dict(Counter(row[column].strip() for row in records))
        assert set(counts) <= {'Yes', 'No', 'Maybe'}
        closed.append({'question': question + 1, 'csv_column_number': column+1,
                       'label': header[column].strip(), 'counts': counts})
        reported = word_tables[closed_table][question+1]
        expected = {key: int(reported[i+2]) for i, key in enumerate(['Yes', 'No', 'Maybe'])}
        actual = {key: counts.get(key,0) for key in expected}
        if expected != actual:
            result['word_tally_mismatches'].append({'file': name, 'question': question+1,
                                                    'word_counts': expected, 'csv_counts': actual})
    ratings = []
    for column in range(first_rating, first_rating+8):
        subject = re.search(r'\[([^\]]+)\]',header[column]).group(1)
        counts = Counter(int(row[column].strip()) for row in records)
        assert set(counts) <= {1,2,3,4,5}
        simple = subject.split(' (',1)[0]
        reported = next(row for row in word_tables[rating_table][1:] if row[0] == simple)
        expected = {str(i+1): int(reported[i+3]) for i in range(5)}
        actual = {str(i):counts.get(i,0) for i in range(1,6)}
        if expected != actual:
            result['word_tally_mismatches'].append({'file': name, 'subject': simple,
                                                    'word_counts': expected, 'csv_counts': actual})
        ratings.append({'subject':subject,'counts':actual})
    result['files'][name] = {'encoding': 'UTF-8 (BOM accepted)', 'data_records':len(records),
                            'columns':len(header), 'grade_column_number':3,
                            'grade_column_label':header[2], 'grade_counts':grades,
                            'timestamp_date_counts':dates,
                            'populated_name_email_fields':personal_fields,
                            'teacher_school_counts':schools,
                            'closed_questions':closed, 'ratings':ratings}
(ROOT/'aggregate-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
summary = {'files': {name:{key:value for key,value in details.items() if key not in {'closed_questions','ratings'}}
                    for name, details in result['files'].items()},
           'word_tally_mismatches':result['word_tally_mismatches']}
print(json.dumps(summary,ensure_ascii=False,indent=2))
