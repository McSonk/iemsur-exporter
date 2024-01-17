import logging

import xml.etree.ElementTree as ET

from iemsur.moodle.objects import Exam, Question, Option, File

logging.getLogger('pypandoc').addHandler(logging.NullHandler())
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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