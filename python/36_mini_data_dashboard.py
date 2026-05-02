# ============================================================
# Program Title : Mini Data Dashboard (Text-based)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Reads a dataset, computes summary stats,
#                 and renders ASCII bar charts -- stdlib only.
# ============================================================

import statistics

def parse_csv(text):
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    headers = [h.strip() for h in lines[0].split(',')]
    rows = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(',')]
        row = {}
        for h, v in zip(headers, values):
            try:    row[h] = float(v)
            except: row[h] = v
        rows.append(row)
    return headers, rows

def num_stats(rows, col):
    vals = [r[col] for r in rows if isinstance(r[col], (int, float))]
    if not vals: return {}
    return {
        'count' : len(vals),
        'mean'  : round(statistics.mean(vals), 2),
        'median': statistics.median(vals),
        'stdev' : round(statistics.stdev(vals), 2) if len(vals)>1 else 0,
        'min'   : min(vals),
        'max'   : max(vals),
    }

def bar_chart(data, title, width=40):
    print(f'\n{title}')
    print('-' * (width + 20))
    max_val = max(data.values()) if data else 1
    for label, val in sorted(data.items(), key=lambda x: -x[1]):
        bar_len = int((val / max_val) * width)
        bar     = chr(9608) * bar_len
        print(f'  {str(label):<15} {bar:<{width}} {val}')
    print()

CSV_DATA = (
    'name,subject,score,hours_studied\n'
    'Alice,Maths,92,6\n'
    'Bob,Maths,75,4\n'
    'Cara,Maths,88,5\n'
    'David,Science,95,7\n'
    'Eve,Science,70,3\n'
    'Frank,Science,82,5\n'
    'Grace,English,90,6\n'
    'Hana,English,78,4\n'
    'Ivan,English,85,5\n'
    'Jane,Maths,80,4\n'
)

if __name__ == '__main__':
    headers, rows = parse_csv(CSV_DATA)

    print('=' * 55)
    print('  STUDENT PERFORMANCE DASHBOARD')
    print('=' * 55)

    for col in ['score', 'hours_studied']:
        st = num_stats(rows, col)
        print(f'\n[{col.upper()}]')
        for k, v in st.items():
            print(f'  {k:<8}: {v}')

    subjects = {}
    for r in rows:
        s = r['subject']
        subjects.setdefault(s, []).append(r['score'])
    avg_by_sub = {s: round(sum(v)/len(v), 1) for s, v in subjects.items()}
    bar_chart(avg_by_sub, 'Average Score by Subject')

    top3 = sorted(rows, key=lambda x: x['score'], reverse=True)[:3]
    print('Top 3 Students:')
    for i, r in enumerate(top3, 1):
        print(f"  {i}. {r['name']:<8} ({r['subject']}) - {r['score']}")
