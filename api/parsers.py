import csv
import pandas as pd
from datetime import datetime
from abc import abstractmethod, ABCMeta
from contextlib import contextmanager
from tempfile import SpooledTemporaryFile, NamedTemporaryFile
from typing import Iterable


def _flat_dict(pyobj, keystring=''):
    if type(pyobj) == dict:
        keystring = keystring + '_' if keystring else keystring
        for k in pyobj:
            yield from _flat_dict(pyobj[k], keystring + str(k))
    elif type(pyobj) == list:
        keystring = keystring + '_' if keystring else keystring
        for n, obj in enumerate(pyobj):
            yield from _flat_dict(obj, keystring + str(n))
    else:
        yield keystring, pyobj


class FileParser(metaclass=ABCMeta):
    mediatype = None

    @staticmethod
    @abstractmethod
    def parse(file: SpooledTemporaryFile) -> Iterable:
        pass

    @staticmethod
    @abstractmethod
    def build(lines: Iterable) -> SpooledTemporaryFile:
        pass

    @staticmethod
    @abstractmethod
    def generate_filename() -> str:
        return

class CSVFileParser(FileParser):
    mediatype = "text/csv"

    @staticmethod
    def parse(file: SpooledTemporaryFile) -> Iterable:
        try:
            df = pd.read_csv(file._file,
                             warn_bad_lines=True,
                             error_bad_lines=False)
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(file._file,
                             encoding='ISO-8859-1',
                             sep=";",
                             warn_bad_lines=True,
                             error_bad_lines=False)
        df = df.fillna("")
        yield from df.to_dict("records")

    @staticmethod
    @contextmanager
    def build(lines: Iterable):
        f = NamedTemporaryFile('w')
        records = []

        for index, line in enumerate(lines):
            line = _flat_dict(line.dict())
            line = { key: value for key, value in line}
            records.append(line)

        df = pd.DataFrame(records)
        df.to_csv(f.name)
        f.seek(0)
        yield open(f.name, mode="rb")
        f.close()

    @staticmethod
    def generate_filename(prefix="model") -> str:
        return f"{prefix}_output_{datetime.now()}.csv"


class XLSXFileParser(FileParser):
    mediatype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    @staticmethod
    def parse(file: SpooledTemporaryFile) -> Iterable:
        df = pd.read_excel(file)
        df = df.fillna("")
        yield from df.to_dict("records")

    @staticmethod
    @contextmanager
    def build(lines: Iterable):
        f = NamedTemporaryFile('w')
        records = []

        for index, line in enumerate(lines):
            line = _flat_dict(line.dict())
            line = { key: value for key, value in line}
            records.append(line)

        df = pd.DataFrame(records)
        df.to_excel(f.name,
                    sheet_name='Model Output',
                    engine='xlsxwriter')
        f.seek(0)
        yield open(f.name, mode="rb")
        f.close()

    @staticmethod
    def generate_filename(prefix="model") -> str:
        return f"{prefix}_output_{datetime.now()}.xlsx"
