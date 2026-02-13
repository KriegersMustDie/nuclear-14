#!/usr/bin/env python3
import re

file_path = r'f:\Github\nuclear-14\Resources\Prototypes\Datasets\tips.yml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('Вы в любое время можете просмотреть и изменить привязки клавиш в меню "Настройки."', 'You can view and change key bindings in the Settings menu at any time.'),
    ('Вы можете открыть внутриигровое Руководство через меню на клавишу Esc, или нажав клавишу 0 на нумпаде (по умолчанию).', 'You can open the in-game Guide through the menu on the Esc key, or by pressing 0 on the numpad (by default).'),
    ('Некоторые внутриигровые объекты имеют связанные с ними записи в Руководстве. Осмотрев объект и нажав на иконку с вопросительным знаком вы можете прочитать эти записи.', 'Some in-game objects have associated entries in the Guide. By examining an object and clicking the question mark icon you can read these entries.'),
    ('Вы можете приблизительно оценить состояние чьего-либо здоровья осмотрев его и нажав на иконку сердца.', 'You can roughly assess someone\'s health status by examining them and clicking the heart icon.'),
    ('Артефакты могут приобретать постоянные эффекты от некоторых активированных узлов, например, становиться интеркомом или чрезвычайно эффективным генератором.', 'Artifacts can acquire permanent effects from certain activated nodes, such as becoming an intercom or extremely efficient generator.'),
    ('Вы можете избежать поскальзывания на большинстве луж, если будете идти шагом. Однако некоторые сильные вещества, такие как космическая смазка, все равно заставят вас поскользнуться.', 'You can avoid slipping on most puddles if you walk slowly. However, some strong substances, such as space lube, will still cause you to slip.'),
    ('Некоторые растения, такие как галакточертополох, можно измельчить для получения чрезвычайно полезных и сильнодействующих лекарств.', 'Some plants, such as galaxythistles, can be ground up to obtain extremely useful and potent medicines.'),
    ('Убирайте лужи и выжимайте их в другие ёмкости, чтобы собрать вещества находившиеся в луже.', 'Clean up puddles and squeeze them into other containers to collect the substances in the puddle.'),
    ('Дренажи, обычно находящиеся в морозильной камере повара или в каморке уборщика, быстро поглощают лужи вокруг себя — в том числе и кровь.', 'Drains, usually located in the cook\'s freezer or the janitor\'s closet, quickly absorb puddles around them — including blood.'),
    ('Когнизин, сложное в изготовлении химическое вещество, делает животных, в которых его вводят, разумными.', 'Cognizine, a complex chemical compound to manufacture, makes animals injected with it sentient.'),
    ('Некоторые реагенты, например, трифторид хлора (CLF3), обладают уникальными эффектами, проявляющимися через прикосновение, например, будучи выпущенными из распылителя или в виде пены.', 'Some reagents, such as chlorine trifluoride (CLF3), have unique effects that manifest through contact, such as when sprayed from a sprayer or as foam.'),
    ('Большинство устройств в игре можно улучшить при помощи высокоуровневых компонентов, которые могут быть созданы учёными или найдены на обломках.', 'Most devices in the game can be upgraded with high-level components, which can be created by scientists or found on wrecks.'),
    ('Не забывайте хоть иногда выходить на улицу потрогать траву в перерывах между раундами Space Station 14.', 'Don\'t forget to go outside occasionally and touch grass between rounds of Space Station 14.'),
    ('Используйте кнопку Использовать предмет в мире (клавиша Е по умолчанию) чтобы взаимодействовать с объектами, если вам не хочется их брать в руки или у вас они заняты.', 'Use the Use Item in World button (E key by default) to interact with objects if you don\'t want to pick them up or if your hands are full.'),
    ('Здравый смысл помогает избегать конфликтов.', 'Common sense helps avoid conflicts.'),
    ('Другие игроки — тоже люди.', 'Other players are people too.'),
    ('Химикаты не реагируют между собой, пока находятся в буфере ХимМастера.', 'Chemicals do not react with each other while in the ChemMaster buffer.'),
    ('Зажмите ПРОБЕЛ (по умолчанию) чтобы замедлить движение шаттла во время пилотирования. Это позволит выполнять более точные маневры или даже полностью остановиться.', 'Hold SPACE (by default) to slow down the shuttle while piloting. This will allow you to perform more precise maneuvers or even stop completely.'),
    ('Противоударная броня значительно эффективнее обычной если противник не использует огнестрельное оружие.', 'Impact armor is significantly more effective than regular armor if the opponent is not using firearms.'),
    ('Будучи призраком, вы можете использовать меню взаимодействия, чтобы автоматически следовать и крутиться вокруг любого объекта в игре.', 'As a ghost, you can use the interaction menu to automatically follow and orbit around any object in the game.'),
    ('Вы можете осмотреть свою гарнитуру, чтобы узнать, какие радиоканалы вам доступны и как по ним говорить.', 'You can examine your headset to see what radio channels are available to you and how to speak on them.'),
    ('Будучи утилизатором, в крайнем случае вы можете использовать протокинетический ускоритель для передвижения в космосе. Просто знайте, что это не очень эффективно.', 'As a Salvage Technician, in a pinch you can use the Proto-Kinetic Accelerator to move through space. Just know that it\'s not very efficient.'),
    ('Будучи Барменом помните, что вы можете экспериментировать при приготовлении напитков. Вы уже пробовали сделать коктейль Кровь Демона?', 'As a Bartender remember that you can experiment when making drinks. Have you tried making a Demon\'s Blood cocktail?'),
    ('Будучи ботаником, вы можете мутировать и скрещивать растения для создания более эффективных и урожайных сортов.', 'As a Botanist, you can mutate and cross-breed plants to create more efficient and productive varieties.'),
    ('Будучи сотрудником службы безопасности, общайтесь и координируйте свои действия с коллегами при помощи радиоканала службы безопасности, чтобы избежать неразберихи.', 'As a Security Officer, communicate and coordinate your actions with colleagues using the security radio channel to avoid confusion.'),
    ('Как сотрудник службы безопасности помните — подозрений мало для обвинений. Возможно кто-то просто оказался не в том месте и не в то время!', 'As a Security Officer remember — suspicion is not enough for accusations. Someone may have just been in the wrong place at the wrong time!'),
    ('Будучи детективом, вы можете более эффективно разыскивать преступников, опираясь на данные об оставленных им отпечатках пальцев и волокнах - сканируйте предметы с которым тот мог взаимодействовать.', 'As a Detective, you can more effectively track down criminals by relying on data about fingerprints and fibers left behind - scan objects the suspect could have interacted with.'),
    ('Будучи учёным, вы можете использовать детали машин получше для повышения эффективности машин. Это может сделать некоторые машины, такие как переработчик биомассы, значительно лучше!', 'As a Scientist, you can use better machine parts to improve machine efficiency. This can make some machines, such as the biomass recycler, significantly better!'),
    ('Будучи учёным, вы можете попытаться угадать, что делает улучшение машины, исходя их того, какой компонент вы улучшаете. Ёмкости материи увеличивают возможности хранения, конденсаторы увеличивают эффективность, и манипуляторы увеличивают мощность.', 'As a Scientist, you can try to guess what a machine upgrade does based on what component you are upgrading. Matter bins increase storage capacity, capacitors increase efficiency, and manipulators increase power.'),
    ('Будучи врачом, постарайтесь быть аккуратным с передозировкой пациентов, особенно если им уже оказали первую помощь. Передозировки могут быть летальны для пациентов в критическом состоянии!', 'As a Medical Doctor, try to be careful with overdosing patients, especially if they have already received first aid. Overdoses can be fatal for patients in critical condition!'),
    ('Будучи химиком, как только вы сделали все, что вам нужно, не бойтесь делать больше глупых реагентов. Вы пробовали дезоксиэфедрин?', 'As a Chemist, once you\'ve done everything you need to do, don\'t be afraid to make more silly reagents. Have you tried deoxyephedrine?'),
    ('Ваш интерес к игре быстро угаснет, если вы будете играть ради убийств и на победу. Если вы обнаружили, что так и играете, то сделайте шаг назад и поговорите с людьми — это гораздо лучше!', 'Your interest in the game will quickly fade if you play for kills and to win. If you find yourself playing that way, take a step back and talk to people — it\'s much better!'),
    ('Пожарные костюмы и зимние куртки обеспечивают умеренную защиту от холода, позволяя вам проводить в космосе и в разгерметизированных отсеках больше времени, чем если бы на вас не было ничего.', 'Firefighter suits and winter jackets provide moderate cold protection, allowing you to spend more time in space and in decompressed compartments than if you had nothing on.'),
    ('В экстренной ситуации не забывайте, что пожарные и экстренные EVA скафандры всегда находятся в соответствующих шкафчиках. В них может быть неудобно передвигаться, но они могут легко спасти вам жизнь в плохой ситуации!', 'In an emergency, remember that firefighter and emergency EVA suits are always in their respective lockers. They may be uncomfortable to move in, but they can easily save your life in a bad situation!'),
    ('В экстренной ситуации помните, что вы можете создать импровизированное оружие! Бейсбольная бита или копьё могут легко стать решающим фактором между отпугиванием нападающего и гибелью от его рук.', 'In an emergency, remember that you can create improvised weapons! A baseball bat or spear can easily become the deciding factor between repelling an attacker and death by their hand.'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('All Russian tips translated successfully!')
