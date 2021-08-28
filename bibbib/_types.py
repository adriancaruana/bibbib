import enum


class EntryType(enum.Enum):
    ARTICLE = enum.auto()
    BOOK = enum.auto()
    BOOKLET = enum.auto()
    CONFERENCE = enum.auto()
    INBOOK = enum.auto()
    INCOLLECTION = enum.auto()
    INPROCEEDINGS = enum.auto()
    MANUAL = enum.auto()
    MASTERSTHESIS = enum.auto()
    MISC = enum.auto()
    PHDTHESIS = enum.auto()
    PROCEEDINGS = enum.auto()
    TECHREPORT = enum.auto()
    UNPUBLISHED = enum.auto()

    @classmethod
    def fromstr(cls, s) -> "EntryType":
        return EntryType[s.upper()]


class FieldType(enum.Enum):
    ADDRESS = enum.auto()
    AUTHOR = enum.auto()
    BOOKTITLE = enum.auto()
    CHAPTER = enum.auto()
    EDITION = enum.auto()
    EDITOR = enum.auto()
    HOWPUBLISHED = enum.auto()
    INSTITUTION = enum.auto()
    JOURNAL = enum.auto()
    MONTH = enum.auto()
    NOTE = enum.auto()
    NUMBER = enum.auto()
    ORGANIZATION = enum.auto()
    OTHER = enum.auto()
    PAGES = enum.auto()
    PUBLISHER = enum.auto()
    SCHOOL = enum.auto()
    SERIES = enum.auto()
    TITLE = enum.auto()
    TYPE = enum.auto()
    VOLUME = enum.auto()
    YEAR = enum.auto()

    @classmethod
    def fromstr(cls, s) -> "FieldType":
        return FieldType[s.upper()]
