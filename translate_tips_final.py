#!/usr/bin/env python3

file_path = r'f:\Github\nuclear-14\Resources\Prototypes\Datasets\tips.yml'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('Копья могут быть обработаны химикатами и будут вводить несколько юнитов каждый раз, когда вы бьёте кого-то напрямую.', 'Spears can be treated with chemicals and will inject several units each time you hit someone directly.'),
    ('Вы можете создать копья с осколков армированного, плазменного и уранового стекла для увеличения урона.', 'You can create spears from shards of reinforced, plasma, and uranium glass to increase damage.'),
    ('Бросайте копья для нанесения дополнительного урона! Однако, будьте осторожны, так как, если вы будете бросать их слишком часто, они могут сломаться.', 'Throw spears to deal extra damage! However, be careful as they can break if you throw them too often.'),
    ('Заточки и копья, сделанные с уранового стекла, могут наносить радиационный урон, который требует лекарства для правильного лечения.', 'Shivs and spears made from uranium glass can deal radiation damage, which requires medicine to properly treat.'),
    ('Все формы поражения токсинами довольно трудно поддаются лечению и обычно включают использование химикатов или других неудобных методов. Вы можете использовать это в своих интересах в бою.', 'All forms of toxin damage are quite difficult to treat and usually require the use of chemicals or other inconvenient methods. You can use this to your advantage in combat.'),
    ('Вы можете бросать созданные болы в людей, для того чтобы замедлить их, позволяя вам преследовать для более лёгкого убийства или для быстрого ухода.', 'You can throw created bolas at people to slow them down, allowing you to pursue them easily or make a quick escape.'),
    ('Вы можете наполнить ранцевый водяной резервуар напалмом для создания огнемёта.', 'You can fill a backpack water tank with napalm to create a flamethrower.'),
    ('Скорость - это почти самое главное в бою. Использование скафандров только для защиты - обычно ужасная идея, если только сопротивление, которое они обеспечивают, не предназначено для боя, или вы не планируете бросаться в бой очертя голову.', 'Speed is almost the most important thing in combat. Using spacesuits only for protection is usually a terrible idea unless the resistance they provide is meant for combat, or you\'re not planning to rush into battle headfirst.'),
    ('Вы можете пшикать огнетушителем, бросать вещи или стрелять из оружия, когда летаете в космосе, чтобы получить незначительное ускорение. Просто стреляйте в противоположную сторону от той, куда вам нужно попасть.', 'You can spray a fire extinguisher, throw things, or shoot weapons while flying in space to get a slight boost. Just shoot in the opposite direction from where you want to go.'),
    ('Вы можете перетаскивать других игроков на себя, чтобы открыть меню обыска, позволяющее вам снимать их снаряжение или принудительно надевать что-то. Обратите внимание, что скафандры или шлемы могут блокировать доступ к одежде под ними, и что определенные предметы требуют больше времени для снятия или надевания, чем другие..', 'You can drag other players onto yourself to open a search menu that lets you remove their equipment or force them to wear something. Note that spacesuits or helmets can block access to clothing underneath them, and certain items take longer to remove or put on than others.'),
    ('Вы можете залезть на стол, перетащив себя на него.', 'You can climb onto a table by dragging yourself onto it.'),
    ('Вы можете переместить объект в сторону, перетащив его, а затем, удерживая CTRL щелкайте правой кнопкой мыши, и двигайте мышь в нужном вам направлении.', 'You can move an object to the side by dragging it, then while holding CTRL right-click and move your mouse in the direction you want.'),
    ('Имея дело со службой безопасности, вы часто можете избежать своего приговора за счёт сотрудничества или обмана.', 'When dealing with security, you can often avoid your sentence through cooperation or deception.'),
    ('Огонь может распространятся на других игроков через прикосновения! Будьте осторожны с горящими телами или с большими толпами людей, находящихся в огне.', 'Fire can spread to other players through contact! Be careful with burning bodies or large crowds of people in flames.'),
    ('Пробоины в корпусе требуют несколько секунд для полной разгерметизации местности. Вы можете использовать это время, чтобы заделать дыру, если достаточно уверены в своих способностях, или просто убежать.', 'Hull breaches take several seconds to fully depressurize the area. You can use this time to patch the hole if confident in your abilities, or just run away.'),
    ('Ожоги, например, от сварочного аппарата, можно использовать для прижигания ран и остановки кровотечения.', 'Burns, such as from a welding tool, can be used to cauterize wounds and stop bleeding.'),
    ('Кровотечение не шутка! Если вас подстрелили или вы получили другую серьёзную травму, позаботьтесь о том, чтобы быстро её вылечить.', 'Bleeding is no joke! If you get shot or suffer other serious injury, make sure to treat it quickly.'),
    ('В экстренной ситуации, вы можете разрезать комбинезон острым предметом, чтобы получить ткань, которая может быть использована как менее эффективная версия бинта.', 'In an emergency, you can cut a jumpsuit with a sharp object to get fabric that can be used as a less effective version of a bandage.'),
    ('Вы можете использовать острые предметы для разделки животных или одежды в контекстном меню при нажатии ПКМ. В том числе осколки стекла.', 'You can use sharp objects to butcher animals or clothing in the context menu by right-clicking. Including glass shards.'),
    ('Большинство взрывчаток имеют таймер, который вы можете установить через ПКМ меню. В том числе пингвин гренадёр!', 'Most explosives have a timer that you can set through the right-click menu. Including grenade penguins!'),
    ('Вы можете кликнуть на имена предметов в ПКМ меню, чтобы подобрать их, вместо того, чтобы наводиться на предмет, а затем подбирать его.', 'You can click on item names in the right-click menu to pick them up, instead of hovering over the item and then picking it up.'),
    ('Космическая Станция 14 - это игра с открытым кодом! Если вы хотите что-то изменить или добавить простой предмет, попробуйте внести вклад в игру. Это не так сложно, как вы думаете.', 'Space Station 14 is an open-source game! If you want to change something or add a simple item, try contributing to the game. It\'s not as hard as you think.'),
    ('В крайнем случае вы можете бросать напитки или другие ёмкости с реагентами позади себя для создания луж, на которых поскользнутся ваши преследователи.', 'As a last resort, you can throw drinks or other containers of reagents behind you to create puddles that your pursuers will slip on.'),
    ('Некоторые оружия, такие как ножи и заточки, имеют большую скорость атаки.', 'Some weapons, such as knives and shivs, have a high attack speed.'),
    ('Челюсти жизни могут открывать запитанные двери.', 'The Jaws of Life can open powered doors.'),
    ('Если вы не Унатх, не пытайтесь пить кровь! Это отравит вас и нанесёт урон.', 'If you\'re not Unathi, don\'t try to drink blood! It will poison you and cause damage.'),
    ('Существует предел химического метаболизма, который ограничивает количество реагентов определенного типа, которые вы можете переварить за один раз. Некоторые расы имеют более высокие пределы метаболизма, например, слаймолюды.', 'There is a chemical metabolism limit that limits the amount of certain types of reagents you can digest at once. Some races have higher metabolism limits, such as slimepeople.'),
    ('Использование сварки без соответствующей защиты для глаз, вызовет нарушение зрения, которое можно вылечить окулином.', 'Using a welder without proper eye protection will cause vision impairment, which can be treated with oculine.'),
    ('Вы можете сплавить осколки стекла в стеклянные листы.', 'You can melt glass shards into glass sheets.'),
    ('Нажатием ПКМ по игроку, а затем нажатием на иконку сердца, вы можете быстро проверить наличие внешних повреждений или наличие кровотечения. Вы так же можете сделать это с собой.', 'By right-clicking on a player and then clicking the heart icon, you can quickly check for external damage or bleeding. You can also do this to yourself.'),
    ('Обезьяны имеют малый шанс быть разумными. УУК!', 'Apes have a small chance of being sentient. OOK!'),
    ('Вы можете определить, разгерметизирована ли область с пожарными шлюзами, посмотря, есть ли у пожарных замков кроме них огни.', 'You can tell if an area with fire shutters is depressurized by looking to see if the fire shutters in addition to them have lights on.'),
    ('Вместо поднятия, вы можете альт-кликнуть по еде, чтобы скушать её. Это так же работает для мышей и других существ без рук.', 'Instead of picking up, you can alt-click on food to eat it. This also works for mice and other creatures without hands.'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('All remaining Russian tips translated successfully!')
