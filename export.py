import logging
from iemsur.moodle.wrappers import ExamReader, ExamWriter

logging.getLogger('pypandoc').addHandler(logging.NullHandler())
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('opening the file...')

    reader = ExamReader()
    reader.read('preguntas-radiologia.xml')
    logger.info(reader.exam)

    writer = ExamWriter(reader.exam)
    writer.write('test.docx')