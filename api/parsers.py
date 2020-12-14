import csv
from datetime import datetime
from abc import abstractmethod, ABCMeta
from contextlib import contextmanager
from tempfile import SpooledTemporaryFile, NamedTemporaryFile
from typing import Iterable


class FileParser(metaclass=ABCMeta):
    mediatype = None

    @staticmethod
    @abstractmethod
    def parse(file: SpooledTemporaryFile) -> Iterable:
        pass

    @staticmethod
    @abstractmethod
    def build(lines: Iterable, keys: Iterable) -> SpooledTemporaryFile:
        pass
    
    @staticmethod
    @abstractmethod
    def generate_filename() -> str:
        return 

class CSVFileParser(FileParser):
    mediatype = "text/csv"

    @staticmethod
    def parse(file: SpooledTemporaryFile) -> Iterable:
        lines = [line.decode('utf-8') for line in file.readlines()]
        reader = csv.DictReader(lines)
        return reader

    @staticmethod
    @contextmanager
    def build(lines: Iterable, fieldnames: Iterable):
        f = NamedTemporaryFile('w')
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for line in lines:
            line = line.dict()
            keys = line.keys()
            for key in list(line.keys()):
                if key not in fieldnames:
                    line.pop(key)
            w.writerow(line)
        f.seek(0)
        yield open(f.name, mode="rb")
        f.close()
    
    @staticmethod
    def generate_filename(prefix="model") -> str:
        return f"{prefix}_output_{datetime.now()}.csv"