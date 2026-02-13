#!/usr/bin/env python3

file_path = r'f:\Github\nuclear-14\Resources\Maps\Corvax\CorvaxSunnyvaleUnderground.yml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('а) ________________________________________________________', 'a) ________________________________________________________'),
    ('б) ________________________________________________________', 'b) ________________________________________________________'),
    ('в) ________________________________________________________', 'c) ________________________________________________________'),
    ('Примечание учителя: Помните, что чистое убежище означает здоровое!', "Teacher's Note: Remember that a clean vault means a healthy one!"),
]

for old, new in replacements:
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        print(f'Replaced {count} instances')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Map translation complete!')
