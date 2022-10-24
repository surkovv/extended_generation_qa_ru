import deeppavlov
model = deeppavlov.build_model("inference.json")
question1 = 'Who played Sheldon Cooper in The Big Bang Theory'
contexts1 = ['Sheldon Lee Cooper is a fictional character in the CBS television series The Big Bang Theory and its spinoff series Young Sheldon, portrayed by actors Jim Parsons']
question2 = 'How many people live in Moscow?'
question3 = 'What is the capital of Russia?'
question4 = 'river in Moscow'
question5 = 'area of Moscow'
question6 = 'When did simplified Chinese characters appeared?'
contexts2 = ["Moscow is the capital and largest city of Russia. The city stands on the Moskva River in Central Russia, with a population estimated at 12.4 million residents within the city limits, over 17 million residents in the urban area, and over 20 million residents in the metropolitan area. The city covers an area of 2,511 square kilometers (970 sq mi), while the urban area covers 5,891 square kilometers (2,275 sq mi), and the metropolitan area covers over 26,000 square kilometers (10,000 sq mi). Moscow is among the world's largest cities; being the most populous city entirely in Europe, the largest urban and metropolitan area in Europe, and the largest city by land area on the European continent."]
contexts3 = ["Standard Chinese (Standard Mandarin), based on the Beijing dialect of Mandarin, was adopted in the 1930s and is now an official language of both the People's Republic of China and the Republic of China (Taiwan), one of the four official languages of Singapore, and one of the six official languages of the United Nations. The written form, using the logograms known as Chinese characters, is shared by literate speakers of mutually unintelligible dialects. Since the 1950s, simplified Chinese characters have been promoted for use by the government of the People's Republic of China, while Singapore officially adopted simplified characters in 1976. Traditional characters remain in use in Taiwan, Hong Kong, Macau, and other countries with significant overseas Chinese speaking communities such as Malaysia (which although adopted simplified characters as the de facto standard in the 1980s, traditional characters still remain in widespread use)."]
print(model([question1], [contexts1]))
print(model([question2], [contexts2]))
print(model([question3], [contexts2]))
print(model([question4], [contexts2]))
print(model([question5], [contexts2]))
print(model([question6], [contexts3]))

question1 = 'Кто играет Шелдона Купера?'
question2 = 'В каком сериале снимался Джим Парсонс?'
question21 = 'Персонажем каких сериалов является Шелдон Купер?'
contexts1 = ['Шелдон Ли Купер — вымышленный персонаж, один из главных героев телесериала «Теория Большого взрыва» и его спин-оффа «Детство Шелдона». Роль Шелдона Купера в «Теории Большого взрыва» исполняет Джим Парсонс, получивший за неё премии «Эмми»']

question3 = 'Где родился Лев Толстой?'
question4 = 'Из-за чего умерла мать Толстого?'
question5 = 'Когда умерла мать Толстого?'
contexts2 = ['Лев Николаевич Толстой родился 28 августа 1828 года в Крапивенском уезде Тульской губернии, в наследственном имении матери — Ясной Поляне. Был четвёртым ребёнком в семье. Мать умерла в 1830 году от «родовой горячки», как тогда говорили, через полгода после рождения дочери, когда Льву не было ещё и трёх лет.']

question6 = 'Какова площадь Москвы?'
contexts3 = ['Москва находится в центре Восточно-Европейской равнины, в междуречье Оки и Волги, на стыке Смоленско-Московской возвышенности (на западе), Москворецко-Окской равнины (на востоке) и Мещёрской низменности (на юго-востоке). Город располагается на Русской плите, входящей в состав Восточно-Европейской платформы; к северу и северо-востоку от Москвы находится московская синеклиза — крупнейшая депрессия центральной части Восточно-Европейской платформы. Территория города по состоянию на 1 января 2014 года составляет 2561,5 км², примерно треть этой площади (878,7 км²) находится внутри кольцевой автомагистрали (МКАД)']
print(model([question1], [contexts1]))
print(model([question2], [contexts1]))
print(model([question21], [contexts1]))
print(model([question3], [contexts2]))
print(model([question4], [contexts2]))
print(model([question5], [contexts2]))
print(model([question6], [contexts3]))
