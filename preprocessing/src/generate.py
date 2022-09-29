from collections import namedtuple
from udapi.block.read.conllu import Conllu
from io import StringIO
import deeppavlov
import pymorphy2
import itertools
morph = pymorphy2.MorphAnalyzer()

def morph_parse(word, tags=()):
    parse = morph.parse(word)
    parse.sort(key = lambda x: x.score, reverse=True)
    def filter_func(x):
        f = 1
        for tag in tags:
            if tag not in x.tag:
                f = 0
                break
        return f
    parse = list(filter(filter_func, parse))
    return parse

Instance = namedtuple('Instance', ['question', 'question_tree', 'answer', 'answer_tree'])

cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
class LongAnswerGenerator:

    def __init__(self, download=True, parser=None):
        if parser is not None:
            self.parser = parser
        else:
            self.parser = deeppavlov.build_model("ru_syntagrus_joint_parsing", download=download)

    def get_tree(self, conllu_output):
        tree = Conllu(filehandle=StringIO(conllu_output)).read_tree()
        return tree

    def generate(self, qa_pairs):
        return [self.generate_one(q, a) for q, a in qa_pairs]

    def preprocess_question(self, question):
        question = question.strip()
        if question[-1] != '?':
            question += '?'

        question = question[:-1].strip() + '?'

        return question

    def preprocess_answer(self, answer):
        answer = answer.strip()
        if answer[-1] == '.':
            answer = answer[:-1]
        return answer

    def preprocess_with_tree(self, answer, answer_tree):
        first_word = answer_tree.descendants[0]
        if first_word.upos == 'PROPN' and answer[0].upper() != answer[0] and len(first_word.form) > 1:
            answer = answer[0].upper() + answer[1:]
            x = answer_tree.descendants[0].form
            answer_tree.descendants[0].form = x[0].upper() + x[1:]
            return answer, answer_tree 
        elif first_word.upos != 'PROPN' and answer[0].lower() != answer[0]:
            answer = answer[0].lower() + answer[1:]
            x = answer_tree.descendants[0].form
            answer_tree.descendants[0].form = x[0].lower() + x[1:]
            return answer, answer_tree 
        return answer, answer_tree 

    def generate_long_answer(self, question, question_tree, answer, answer_tree):
        return CommonGenerator().generate(question, question_tree, answer, answer_tree)

    def postprocess(self, answer):
        if answer[0].upper() != answer[0] and (answer[1] != ' ' or answer[0] in cyrillic_alphabet):
            answer = answer[0].upper() + answer[1:]
        if answer[-1] != '.':
            answer += '.'
        answer = answer.replace(' ,', ',').replace(' .', '.').replace('„ ', '„').replace(' “', '“').replace(' :', ':').replace('( ', '(').replace(' )', ')')
        return answer

    def generate_one(self, question, answer):
        question = self.preprocess_question(question)
        answer = self.preprocess_answer(answer)
        question_tree = self.get_tree(*self.parser([question]))
        question_tree.descendants[-1].remove()
        answer_tree = self.get_tree(*self.parser([answer]))
        answer, answer_tree = self.preprocess_with_tree(answer, answer_tree)
        question, question_tree = self.preprocess_with_tree(question, question_tree)
        long_answer = self.generate_long_answer(question, question_tree, answer, answer_tree)
        long_answer = self.postprocess(long_answer)
        return long_answer


case_handlers = []


def handler(class_handler):
    case_handlers.append(class_handler())
    return class_handler


class CommonGenerator:
    def generate(self, question, question_tree, answer, answer_tree):
        for handler in case_handlers:
            result, long_answer = handler.generate(question, question_tree, answer, answer_tree)
            if result:
                return long_answer
        return answer


def get_root(tree):
    if tree.udeprel == 'root':
        return tree
    return tree.children[0]

def get_children(node, udeprel):
    res = []
    for child in node.children:
        if child.udeprel == udeprel:
            res.append(child)
    return res


@handler
class Case1Handler:
    def check(self, question, question_tree):
        root = get_root(question_tree)
        if root.form.lower() in ['кто', 'что']:
            return True
        return False

    def trim_dash(self, answer, answer_tree):
        id1 = answer.find('-') 
        id2 = answer.find('—')
        if id1 > 0 and answer[id1 - 1] != ' ':
            id1 = -1

        if id2 > 0 and answer[id2 - 1] != ' ':
            id2 = -1

        idx = max(id1, id2)

        if idx != -1:
            answer = answer[idx+1:]
            for node in answer_tree.descendants:
                tobreak = node.form in '-—'
                node.remove(children='rehang')
                if tobreak:
                    break

        if answer_tree.descendants[0].form == 'это':
            answer_tree.descendants[0].remove(children='rehang')
            answer = answer[3:]
        return answer.strip(), answer_tree

    def find_this(self, root):
        if root.next_node and root.next_node.lemma in ['такой', 'это']:
            return root.next_node
        if root.prev_node and root.prev_node.lemma in ['такой', 'это']:
            return root.prev_node
        return None

    def generate(self, question, question_tree, answer, answer_tree):
        if not self.check(question, question_tree):
            return False, None

        answer, answer_tree = self.trim_dash(answer, answer_tree)

        long_answer = answer

        this_node = self.find_this(get_root(question_tree))
        if this_node:
            # Что такое/Кто такой
            root = get_root(question_tree)
            this_node.remove(children='rehang')
            root.remove(children='rehang')

            long_answer = question_tree.compute_text() + " - это " + answer
        elif get_root(question_tree).children[0].udeprel == 'nsubj':
            # Кто автор...
            root = get_root(question_tree)
            root.remove(children='rehang')

            long_answer = answer + " - это " + question_tree.compute_text() 
        elif get_root(question_tree).children[0].udeprel == 'cop':
            # Кто был...
            root = get_root(question_tree)
            root.form = answer
            aux = root.children[0]
            aux.shift_before_subtree(root)
            nsubj = None
            for node in root.children:
                if node.udeprel == 'nsubj':
                    nsubj = node
                    break
            nsubj.shift_before_subtree(aux)
            long_answer = question_tree.compute_text()
        return True, long_answer


class Reordable:
    def can_reorder(self, root):
        prefix = "в отличии"
        text = root.compute_text().lower() 
        if len(text) >= len(prefix) and text[:len(prefix)] == prefix:
            return False
        return True

    def reorder_node(self, root):
        # ORDER: nsubj [advmod, ...] root xcomp [obj, ...] [iobj, ...] [obl, ...]

        if (not self.can_reorder(root)):
            return

        before, after = [], []
        before.extend(get_children(root, 'nsubj'))
        before.extend(get_children(root, 'advmod'))
        after.extend(get_children(root, 'xcomp'))
        after.extend(get_children(root, 'obj'))
        after.extend(get_children(root, 'iobj'))
        after.extend(get_children(root, 'obl'))

        for node in before[::-1]:
            node.shift_before_subtree(root)

        for node in after[::-1]:
            node.shift_after_node(root)

        for xcomp in get_children(root, 'xcomp'):
            self.reorder_node(xcomp)

    def reorder_tree(self, tree):
        self.reorder_node(get_root(tree))


class RootTrimmer:
    def trim(self, question_tree, answer_tree):
        # WARN: do not harmonize after trimming
        if get_root(question_tree).form.lower() == get_root(answer_tree).form.lower():
            get_root(answer_tree).remove(children='rehang')
            return True
        return False

class Harmonizer:
    case_table = {
            'Nom': 'nomn',
            'Gen': 'gent',
            'Par': 'gent',
            'Dat': 'datv',
            'Acc': 'accs',
            'Loc': 'loct',
            'Ins': 'ablt',
            'Voc': 'voct',
            '': 'nomn'
            }
    number_table = {
            'Sing': 'sing',
            'Plur': 'plur',
            '': 'sing'
            }

    gender_table = {
            'Masc': 'masc',
            'Fem': 'femn',
            'Neut': 'neut'
            }
    
    def harmonize_verb(self, qword_node, question_tree, answer_tree):
        root = get_root(question_tree)
        if root.upos not in ['VERB', 'AUX'] or qword_node.feats['Case'] != 'Nom':
            return
        self.harmonize_verb_one(qword_node, question_tree, answer_tree, root)
        auxes = get_children(root, 'aux')
        for aux in auxes:
            self.harmonize_verb_one(qword_node, question_tree, answer_tree, aux)

    def harmonize_verb_one(self, qword_node, question_tree, answer_tree, root):
        number = ''
        aroot = get_root(answer_tree)
        if qword_node.lemma == 'какой':
            number = aroot.feats['Number']
        elif qword_node.lemma in ['кто', 'что', 'чем']:
            number = aroot.feats['Number']
        if len(get_children(aroot, 'conj')) > 0:
            number = 'Plur'
        if root.feats['Number'] == '':
            number = ''
        if root.feats['Number'] != number:
            params = None
            if number != '':
                params = {self.number_table[number]}
            if params is not None:
                parsers = list(itertools.chain(
                    morph_parse(root.form, ["VERB"]),
                    morph_parse(root.form, ["PRTS"])
                ))
                for p in parsers:
                    inflected = p.inflect(params)
                    if inflected is not None:
                        new_word = inflected.word
                        break
                root.form = new_word

        # Gender
        if root.feats['Tense'] == 'Past' and number == 'Sing':
            gender = ''
            if qword_node.lemma == 'какой':
                gender = qword_node.feats['Gender']
            elif qword_node.lemma in ['кто', 'что', 'чем']:
                gender = aroot.feats['Gender']
            if root.feats['Gender'] == '':
                gender = ''
            if root.feats['Gender'] != gender:
                params = None
                if gender != '':
                    params = {self.gender_table[gender]}
                if params is not None:
                    parsers = list(itertools.chain(
                        morph_parse(root.form, ["VERB"]),
                        morph_parse(root.form, ["PRTS"])
                    ))
                    new_word = parsers[0].inflect(params).word
                    root.form = new_word

    def harmonize_noun(self, qword_node, question_tree, answer_tree):
        if answer_tree.descendants[0].form.lower() in ['как']:
            return
        root = get_root(question_tree)
        aroot = get_root(answer_tree)
        if aroot.upos not in ['NOUN', 'PNOUN', 'PROPN']:
            return

        preps_qword = get_children(qword_node, 'case')
        preps = get_children(aroot, 'case')
        if len(preps_qword) > 0 and len(preps) > 0 and preps[0].form != preps_qword[0].form:
            return

        case, number = '', ''
        if qword_node.lemma == 'какой':
            case = qword_node.feats['Case']
            number = qword_node.feats['Number']
        elif qword_node.lemma in ['кто', 'что', 'чем']:
            case = qword_node.feats['Case']
            number = aroot.feats['Number']

        parsers = morph_parse(aroot.form, ['NOUN', self.case_table[qword_node.feats['Case']]])

        if (aroot.upos != 'PROPN' and len(parsers) == 0) or aroot.feats['Number'] != number:
            params = None
            if case != '' and number != '':
                params = {self.case_table[case], self.number_table[number]}
            elif number != '':
                params = {self.number_table[number]}
            elif case != '':
                params = {self.case_table[case]}
            if params is not None:
                parsers = morph_parse(aroot.form, ['NOUN'])
                if len(parsers) > 0:
                    new_word = parsers[0].inflect(params).word
                    aroot.form = new_word
                    if aroot.upos == 'PROPN':
                        aroot.form = aroot.form[0].upper() + aroot.form[1:]
                for adj in get_children(aroot, 'amod'):
                    parsers = morph_parse(adj.form, [self.case_table[aroot.feats['Case']]]) 
                    if len(parsers) > 0:
                        new_word = parsers[0].inflect(params).word
                        adj.form = new_word
                    for adj_conj in get_children(adj, 'conj'):
                        parsers = morph_parse(adj_conj.form, [self.case_table[aroot.feats['Case']]]) 
                        if len(parsers) > 0:
                            new_word = parsers[0].inflect(params).word
                            adj_conj.form = new_word

        if len(preps_qword) > 0 and len(preps) == 0:
            prep_node = aroot.create_child(deprel='case')
            prep_node.form = prep_node.lemma = preps_qword[0].form
            prep_node.upos = 'ADP'
            prep_node.shift_before_subtree(aroot)

    def harmonize(self, qword_node, question_tree, answer_tree):
        self.harmonize_verb(qword_node, question_tree, answer_tree)
        self.harmonize_noun(qword_node, question_tree, answer_tree)


@handler
class Case2Handler(RootTrimmer, Harmonizer, Reordable):
    def find_qword(self, question_tree):
        root = get_root(question_tree)
        if len(root.children) > 0:
            clause = root.children[0]
            for word in clause.descendants(add_self=True):
                if word.lemma in ['кто', 'что', 'чем']:
                    return word
        return None

    def check(self, question, question_tree):
        return self.find_qword(question_tree) != None

    def generate(self, question, question_tree, answer, answer_tree):
        if not self.check(question, question_tree):
            return False, None
        if len(answer_tree.descendants) >= 5 and \
        get_root(answer_tree).upos == 'VERB':
            return True, answer
        if not self.trim(question_tree, answer_tree):
            qword_node = self.find_qword(question_tree)
            self.harmonize(qword_node, question_tree, answer_tree)

        qword_node = self.find_qword(question_tree)
        if qword_node.form.lower() == 'что' and answer_tree.descendants[0].form.lower() == 'что':
            qword_node.form = answer_tree.compute_text()
            for c in qword_node.children: 
                c.remove()
            qword_node.shift_after_subtree(question_tree.descendants[-1])
            root = get_root(question_tree)
            nsubj = get_children(root, 'nsubj')[0]

            nsubj.shift_before_subtree(root)
            long_answer = question_tree.compute_text()
        else:
            qword_node.form = answer_tree.compute_text()
            for c in qword_node.children: 
                c.remove()
            self.reorder_tree(question_tree)
            long_answer = question_tree.compute_text()
        return True, long_answer
