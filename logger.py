import json
import logging
import pprint
from logging import Formatter


class JsonFormatter(Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record):
        json_record = {"level": str.replace(str.replace(record.levelname, "WARNING", "WARN"), "CRITICAL", "FATAL"),
                       "message": record.getMessage(),
                       "filename": (record.filename,), "funcName": (record.funcName,), "lineno": record.lineno}
        return json.dumps(json_record)


class TextFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        super(TextFormatter, self).__init__(fmt, datefmt)

    def format(self, record):
        # Добавляем время (asctime) к записи
        record.asctime = self.formatTime(record, self.datefmt)
        res = f'[{record.levelname} {record.asctime}] {record.getMessage()}'
        if record.exc_text:
            res += f'\n{record.exc_text}'
        return res


logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(logging.DEBUG)

event_logger = logging.getLogger('event_logger')
event_logger.setLevel(logging.DEBUG)
event_logger.propagate = False
event_handler = logging.FileHandler('bot.log')
event_handler.setFormatter(TextFormatter(datefmt='%Y-%m-%d %H:%M:%S'))
event_logger.addHandler(event_handler)
