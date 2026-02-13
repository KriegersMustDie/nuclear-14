#!/usr/bin/env python3

file_path = r'f:\Github\nuclear-14\Resources\Maps\Corvax\CorvaxSunnyvaleUnderground.yml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('Домашнее задание', 'Homework'),
    ('Тема: Чистота и здоровье', 'Topic: Cleanliness and Health'),
    ('Имя:', 'Name:'),
    ('Класс:', 'Class:'),
    ('Инструкции: Ответьте на следующие вопросы, основанные на обсуждении в классе важности поддержания чистоты в нашем убежище.', 'Instructions: Answer the following questions based on class discussion about the importance of maintaining cleanliness in our vault.'),
    ('Почему важно поддерживать чистоту в нашем убежище?', 'Why is it important to maintain cleanliness in our vault?'),
    ('Перечислите три способа, которыми мы можем помочь поддерживать порядок в нашем жилом пространстве:', 'List three ways we can help maintain order in our living space:'),
    ('Что делать, если вы видите беспорядок?', 'What should you do if you see a mess?'),
    ('Нарисуйте свое любимое чистое место в убежище:', 'Draw your favorite clean place in the vault:'),
    ('(Используйте пробел ниже)', '(Use the space below)'),
]

for old, new in replacements:
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        print(f'Replaced {count} instances of: {old}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('All CorvaxSunnyvaleUnderground map Russian content translated!')
