from collections import namedtuple

Instance = namedtuple('Instance', ['question', 'question_tree', 'answer', 'answer_tree'])

class LongAnswerGenerator:
    
    handlers = []

    def __init__(self, question, question_tree, answer, answer_tree):
        self.instance = Instance(question, question_tree, answer, answer_tree)

    def generate(self):
        output = ""
        for handler in self.handlers:
            success, result = handler(instance).generate()
            if success:
                output = result
                break

        return self.text_from_tree(output)


class Handler:
    def __init__(self, instance):
        self.instance = instance

    def generate(self):
        pass


class OneWordHandler(Handler):
    def generate(self):
        question_word_list = [
            "кто",
            "кого",
            "кому", 
            "кем",
            "ком"
            "что",
            "чему",
            "чего",
            "чем",
            "чем",
            "как",
            "где",
            "когда",
            "откуда",
            "куда"
        ]
