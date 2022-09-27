class Record:
    def __init__(self, contexts, question, answer, long_answer=None):
        if isinstance(contexts, list):
            self.contexts = contexts
        else:
            self.contexts = [contexts]
        self.question = question
        self.answer = answer
        self.long_answer = long_answer

    @property
    def cqa(self):
        return [[self.contexts, self.question], self.answer]

    @property
    def cqla(self):
        assert self.long_answer is not None
        return [[self.contexts, self.question], self.long_answer]


    @property
    def micro(self):
        class Micro:
            def __init__(self, rec):
                self.question = rec.question
                self.answer = rec.answer
                self.long_answer = rec.long_answer

            def __repr__(self):
                return f'Question: {self.question}\n'+\
                   f'Answer: {self.answer}\n'+\
                   f'Long answer: {self.long_answer}\n'

        return Micro(self)

    def __repr__(self):
        return f'Question: {self.question}\n'+\
               f'Answer: {self.answer}\n'+\
               f'Long answer: {self.long_answer}\n\n'+\
               f'Contexts: {self.contexts}\n'