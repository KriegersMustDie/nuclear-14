#!/usr/bin/env python3

file_path = r'f:\Github\nuclear-14\Resources\Prototypes\Corvax\Trade\trade.yml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Additional store categories found
replacements = [
    ('name: "Головные уборы"', 'name: "Headwear"'),
    ('name: "Броня"', 'name: "Armor"'),
    ('name: "Экипировка (РПС)"', 'name: "Gear (RPS)"'),
    ('name: "Материалы и хлам"', 'name: "Materials and Junk"'),
    ('name: Рыбалка', 'name: Fishing'),
    ('name: "Руда и валюта"', 'name: "Ore and Currency"'),
    ('name: "Алкоголь"', 'name: "Alcohol"'),
]

for old, new in replacements:
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        print(f'Replaced {count} instances of: {old}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('All additional trade.yml Russian categories translated!')
