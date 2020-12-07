import csv
from abc import abstractmethod, ABCMeta
from tempfile import SpooledTemporaryFile
from typing import Iterable


class FileParser(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def parse(file: SpooledTemporaryFile) -> Iterable:
        pass


class CSVFileParser(FileParser):
    @staticmethod
    def parse(file: SpooledTemporaryFile) -> Iterable:
        lines = [line.decode('utf-8') for line in file.readlines()]
        reader = csv.DictReader(lines)
        return reader
