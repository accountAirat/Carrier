import os
import zipfile
from src.settings import LOGGING
from logging.handlers import TimedRotatingFileHandler
import logging.config


class ZipTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='D', interval=7, backupCount=7,
                 encoding=None, delay=True, utc=False, atTime=None):
        super().__init__(filename=filename, when=when, interval=interval, backupCount=backupCount, encoding=encoding,
                         delay=delay, utc=utc, atTime=atTime)

    def make_zip(self):
        dir_path, base_filename = os.path.split(self.baseFilename)
        logs_list = [f for f in os.listdir(dir_path)
                     if all([f.startswith(base_filename), f != base_filename, not f.endswith('.zip')])]
        if len(logs_list) >= self.backupCount:
            arc_name = f'archive_{logs_list[0]}.zip',
            with zipfile.ZipFile(f'archive_{arc_name}.zip', 'w') as zip_file:
                for f in logs_list:
                    file = os.path.join(dir_path, f)
                    zip_file.write(file, compress_type=zipfile.ZIP_DEFLATED)
                    os.remove(file)

    def doRollover(self):
        if self.backupCount > 0:
            self.make_zip()
        super().doRollover()

    def getFilesToDelete(self):
        return []


# Можно установить уровень журнала для остальных логеров на ERROR
# logging.basicConfig(level=logging.ERROR)


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('logger')
