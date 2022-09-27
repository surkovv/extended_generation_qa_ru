from collections import namedtuple
from udapi.block.read.conllu import Conllu
from io import StringIO
import deeppavlov

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
            return answer, self.get_tree(*self.parser([answer]))
        elif first_word.upos != 'PROPN' and answer[0].lower() != answer[0]:
            answer = answer[0].lower() + answer[1:]
            return answer, self.get_tree(*self.parser([answer]))
        return answer, answer_tree 

    def generate_long_answer(self, question, question_tree, answer, answer_tree):
        return CommonGenerator().generate(question, question_tree, answer, answer_tree)

    def postprocess(self, answer):
        if answer[0].upper() != answer[0] and (answer[1] != ' ' or answer[0] in cyrillic_alphabet):
            answer = answer[0].upper() + answer[1:]
        if answer[-1] != '.':
            answer += '.'
        return answer

    def generate_one(self, question, answer):
        question = self.preprocess_question(question)
        answer = self.preprocess_answer(answer)
        question_tree = self.get_tree(*self.parser([question]))
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
    return tree.children[0]

@handler
class Case1Handler:
    def check(self, question, question_tree):
        root = question_tree.children[0]
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

        if idx == -1:
            return answer, answer_tree

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
        question_tree.descendants[-1].remove()
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
