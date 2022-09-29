from collections import defaultdict
from termcolor import colored
cases = defaultdict()

class Tester:
    def __init__(self, long_answer_generator):
        self.long_answer_generator = long_answer_generator

    def test_all(self):
        for case_name in cases.keys():
            self.test_case(case_name)

    def test_case(self, case_name):
        assert case_name in cases.keys()
        print(colored("CASE:", 'red'), case_name)
        print(colored("DESC:", 'red'), cases[case_name]['desc'])
        
        for question, answer, long_answer in cases[case_name]['qal_triples']:
            self.test_one(question, answer, long_answer)

        print()

    def test_one(self, question, answer, long_answer):
        print(colored("TEST:", 'red'), question, answer)
        gen = self.long_answer_generator.generate_one(question, answer)
        if gen == long_answer:
            print('ok')
            return True
        else:
            print('GENERATED', gen, '!=', "TRUE", long_answer)
            return False


def add_case(name, desc):
    cases[name] = {'desc': desc,
                   'qal_triples': []}


def add_test(test_case, question, answer, long_answer):
    assert test_case in cases
    cases[test_case]['qal_triples'].append((question, answer, long_answer))


add_case('case1', 'Кто, что is root')
add_test('case1', 'Что такое инкубационный период?',
               'в течение которого не проявляется никаких симптомов инфекции',
               'Инкубационный период - это в течение которого не проявляется никаких симптомов инфекции.')
add_test('case1', 'Кто автор статьи Творчество Прокофьева в советском теоретическом музыкознании ?', ' Ю. Н. Холопов', 'Ю. Н. Холопов - это автор статьи Творчество Прокофьева в советском теоретическом музыкознании.')
add_test('case1', 'Кто такой фасилитатор?', ' человек, обеспечивающий успешную групповую коммуникацию ', 'Фасилитатор - это человек, обеспечивающий успешную групповую коммуникацию.')
add_test('case1', 'Кто такие Polyergus?', 'Муравьи-амазонки', 'Polyergus - это муравьи-амазонки.')
add_test('case1', 'Что такое ω?', ' ω — угловая скорость вращения Земли', 'ω - это угловая скорость вращения Земли.')
add_test('case1', 'Кто был Лафайет по политическим убеждениям', 'Либерал', 'Лафайет был либерал по политическим убеждениям.')
add_test('case1', 'кто был отец Карла Линнея?', 'сельский лютеранский пастор', 'Отец Карла Линнея был сельский лютеранский пастор.')
add_test('case1', 'Кредитное товарищество что это?', 'вид кооперативного учреждения мелкого кредита, существовавший в Российской империи  ', 'Кредитное товарищество - это вид кооперативного учреждения мелкого кредита, существовавший в Российской империи.')

add_case('case2', 'Кто, что, and their other forms')
add_test('case2', 'Чем заболел Байрон в Миссолонги?', 'лихорадкой', 'Байрон заболел лихорадкой в Миссолонги.')
add_test('case2', 'Кто считал что русская публицистическая литература восходит к „Слову о Законе и Благодати“ Илариона?', ' Игорь Дедков.', 'Игорь Дедков считал что русская публицистическая литература восходит к „Слову о Законе и Благодати“ Илариона.')
add_test('case2', 'Кто увидел вражеский аэроплан во время розведки?', 'лётчики', 'Лётчики увидели вражеский аэроплан во время розведки.')
add_test('case2', 'На что укладывается верхнее строение пути?', 'земляное полотно', 'Верхнее строение пути укладывается на земляное полотно.')
add_test('case2', 'Что сообщал Моцарт о Констанции в письме 15 декабря 1781 года ее отцу?', 'Что собирается жениться на ней.', 'Моцарт сообщал о Констанции в письме 15 декабря 1781 года ее отцу что собирается жениться на ней.')
add_test('case2', 'С чем связывается образ крысы?', ' с порчей, разрушением, смертью', 'Образ крысы связывается с порчей, разрушением, смертью.')
add_test('case2', 'Кому передали Озерки родители Бунина?', ' сыну Евгению', 'Родители Бунина передали Озерки сыну Евгению.')
add_test('case2', 'К чему привели ошибочные данные разветки Британии?', 'британская авиация нанесла бомбовые удары', 'Британская авиация нанесла бомбовые удары.')
add_test('case2', 'Что описывает Манну в романе', 'Манн описывает историю упадка и вырождения купеческой династии из Любека', 'Манн описывает историю упадка и вырождения купеческой династии из Любека.')
add_test('case2', 'Кем писаны многие произведения средневековых поэтов?', 'Писаны под их диктовку женщинами.', 'Многие произведения средневековых поэтов писаны под их диктовку женщинами.')
add_test('case2', 'К чему в последующие этапы своего развития неоднократно возвращалась философия?', 'к релятивизму', 'Философия неоднократно возвращалась к релятивизму в последующие этапы своего развития.')
add_test('case2', 'Кто развил философию в направлении абсолютного идеализма?', 'Фихте, Шеллинг и Гегель', 'Фихте, Шеллинг и Гегель развили философию в направлении абсолютного идеализма.')
add_test('case2', 'В виде чего могут использоваться такие графики?', ' Как самостоятельные модели технического анализа.', 'Такие графики могут использоваться как самостоятельные модели технического анализа.')
add_test('case2', 'В отличии от чего в болгарском и македонском языках, при наличии определяемых слов перед существительным, определённый артикль ставится только в конце первого слова?', 'падежных форм русского языка', 'В отличии от падежных форм русского языка в болгарском и македонском языках, при наличии определяемых слов перед существительным, определённый артикль ставится только в конце первого слова.')
add_test('case2', 'Чем характеризуется бегство вкладчиков ?', 'наплыв в банк требований о возвращении вкладов', 'Бегство вкладчиков характеризуется наплывом в банк требований о возвращении вкладов.')
add_test('case2', 'Что означает выражение: страна может осуществлять производство определенного товара с меньшими издержками?', 'используя меньшее количество ресурсов', 'Выражение: страна может осуществлять производство определенного товара с меньшими издержками означает используя меньшее количество ресурсов.')
add_test('case2', 'Что вызвало всплеск общественного интереса к этому направлению?', ' Публикация ряда результатов в открытой печати', 'Публикация ряда результатов в открытой печати вызвало всплеск общественного интереса к этому направлению.')
add_test('case2', 'Кого несомненно возбудит занятие Порт-Артура или Да-лянь-вана? ', ' Китай', 'Занятие Порт-Артура или Да-лянь-вана несомненно возбудит китай.')
