#!/usr/bin/env python3

file_path = r'f:\Github\nuclear-14\Resources\Prototypes\Corvax\Trade\trade.yml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('name: "Револьверы"', 'name: "Revolvers"'),
    ('name: "Пистолеты"', 'name: "Pistols"'),
    ('name: "Пистолеты-пулеметы"', 'name: "Submachine Guns"'),
    ('name: "Дробовики"', 'name: "Shotguns"'),
    ('name: "Штурмовые винтовки"', 'name: "Assault Rifles"'),
    ('name: "Пулеметы"', 'name: "Machine Guns"'),
    ('name: "Винтовки"', 'name: "Rifles"'),
    ('name: "Энергооружие"', 'name: "Energy Weapons"'),
    ('name: "Патроны"', 'name: "Ammunition"'),
    ('name: "Ближний бой"', 'name: "Melee"'),
]

for old, new in replacements:
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        print(f'Replaced {count} instances of: {old}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('All trade.yml Russian categories translated!')
