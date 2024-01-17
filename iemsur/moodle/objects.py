class File:
    def __init__(self):
        self.name = None
        self.encoding = None
        self.content = None

    def __str__(self):
        return f'File[name={self.name}, encoding={self.encoding}]'

class Option:
    def __init__(self, option, correct=False):
        self.option = option
        self.correct = correct

    def __str__(self):
        return f'Option[option={self.option}, correct={self.correct}]'

class Question:
    def __init__(self):
        self.number = None
        self.desc = None
        self.type = None
        self.options = []
        self.file = None
        '''For true/false options'''
        self.tf_value = None

    def is_true_false(self):
        return self.type == 'truefalse'

    def is_multiple_choice(self):
        return self.type == 'multichoice'

    def add_option(self, option):
        self.options.append(option)

    def __str__(self):
        return f'Question[type: {self.type}, File: {self.file}, {self.number} - {self.desc}]'

class Exam:
    def __init__(self):
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def print(self):
        content = ''
        for question in self.questions:
            content += str(question)
            content += '\n***\n'
        return content
    
    def sort(self):
        if self.questions[0].number is not None:
            self.questions.sort(key=lambda x: x.number)

    def __str__(self):
        return f'Exam. Questions: {len(self.questions)}'