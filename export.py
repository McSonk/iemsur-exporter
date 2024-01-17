import logging

import xml.etree.ElementTree as ET

logging.getLogger('pypandoc').addHandler(logging.NullHandler())
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

    def __str__(self):
        return f'Exam. Questions: {len(self.questions)}'

if __name__ == '__main__':
    logger.info('opening the file...')
    xml = ET.parse('preguntas-radiologia.xml')
    quiz = xml.getroot()
    exam = Exam()

    for question in quiz:
        q_obj = Question()
        q_obj.type =  question.attrib['type']
        q_obj.number = question.find('name').find('text').text

        q_text = question.find('questiontext')
        q_obj.desc = q_text.find('text').text

        q_file = q_text.find('file')

        if q_file is not None:
            q_obj.file = File()
            q_obj.file.name = q_file.attrib['name']
            q_obj.file.encoding = q_file.attrib['encoding']
            q_obj.file.content = q_file.text

        if q_obj.is_true_false():
            q_obj.tf_value = question.find('.//answer[@fraction="100"]').find('text').text == 'true'
        elif q_obj.is_multiple_choice():
            for answer in question.findall('answer'):
                opt = Option(answer.find('text').text)
                opt.correct = answer.attrib['fraction'] == '100'
                q_obj.add_option(opt)
        else:
            logger.warning(f'Unknown type: {q_obj.type}')
        exam.add_question(q_obj)

    logger.info(exam)
    logger.debug(exam.print())