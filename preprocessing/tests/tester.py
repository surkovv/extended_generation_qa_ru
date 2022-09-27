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
