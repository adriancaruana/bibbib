import dataclasses
from typing import List, Dict

from ._errors import FieldError, Error
from ._types import EntryType, FieldType


FIELD_LUT = {e.name.lower(): e for e in FieldType}


@dataclasses.dataclass(frozen=True)
class Entry:
    key: str
    bibtex_entry: Dict
    entry_type: EntryType = dataclasses.field(init=False)
    fields_included: List[FieldType] = dataclasses.field(default_factory=list)
    fields_required: List[FieldType] = dataclasses.field(init=False)
    fields_optional: List[FieldType] = dataclasses.field(init=False)
    field_errors: List[Error] = dataclasses.field(init=False, default_factory=list)

    def __post_init__(self):
        for fname, fval in self.bibtex_entry.items():
            self.fields_included.append(FIELD_LUT.get(fname.lower(), FieldType.OTHER))
        missing_fields = []
        for f in self.fields_required:
            missing_field = None
            if isinstance(f, list):
                if not any(i in self.fields_included for i in f):
                    missing_fields.append(f)
            if f not in self.fields_included:
                missing_fields.append(f)

        for f in missing_fields:
            f_str = (
                " or ".join(map(lambda x: x.name, f)) if isinstance(f, list) else f.name
            )
            self.field_errors.append(
                FieldError(
                    f"Required field={f_str} missing from Entry={self.entry_type.name} with key={self.key}."
                )
            )


@dataclasses.dataclass(frozen=True)
class Article(Entry):
    entry_type = EntryType.ARTICLE
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.JOURNAL,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.VOLUME,
        FieldType.NUMBER,
        FieldType.PAGES,
        FieldType.MONTH,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class Book(Entry):
    entry_type = EntryType.BOOK
    fields_required = [
        [FieldType.AUTHOR, FieldType.EDITOR],
        FieldType.TITLE,
        FieldType.PUBLISHER,
        FieldType.YEAR,
    ]
    fields_optional = [
        [FieldType.VOLUME, FieldType.NUMBER],
        FieldType.SERIES,
    ]


@dataclasses.dataclass(frozen=True)
class Booklet(Entry):
    entry_type = EntryType.BOOK
    fields_required = [
        FieldType.TITLE,
    ]
    fields_optional = [
        FieldType.AUTHOR,
        FieldType.HOWPUBLISHED,
        FieldType.ADDRESS,
        FieldType.MONTH,
        FieldType.YEAR,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class Conference(Entry):
    entry_type = EntryType.CONFERENCE
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.BOOKTITLE,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.EDITOR,
        [FieldType.VOLUME, FieldType.NUMBER],
        FieldType.SERIES,
        FieldType.PAGES,
        FieldType.ADDRESS,
        FieldType.MONTH,
        FieldType.ORGANIZATION,
        FieldType.PUBLISHER,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class InBook(Entry):
    entry_type = EntryType.INBOOK
    fields_required = [
        [FieldType.AUTHOR, FieldType.EDITOR],
        FieldType.TITLE,
        [FieldType.CHAPTER, FieldType.PAGES],
        FieldType.PUBLISHER,
        FieldType.YEAR,
    ]
    fields_optional = [
        [FieldType.VOLUME, FieldType.NUMBER],
        FieldType.SERIES,
        FieldType.TYPE,
        FieldType.ADDRESS,
        FieldType.EDITION,
        FieldType.MONTH,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class InCollection(Entry):
    entry_type = EntryType.INCOLLECTION
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.BOOKTITLE,
        FieldType.PUBLISHER,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.EDITOR,
        [FieldType.VOLUME, FieldType.NUMBER],
        FieldType.SERIES,
        FieldType.TYPE,
        FieldType.CHAPTER,
        FieldType.PAGES,
        FieldType.ADDRESS,
        FieldType.EDITION,
        FieldType.MONTH,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class InProceedings(Entry):
    entry_type = EntryType.INPROCEEDINGS
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.BOOKTITLE,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.EDITOR,
        [FieldType.VOLUME, FieldType.NUMBER],
        FieldType.SERIES,
        FieldType.PAGES,
        FieldType.ADDRESS,
        FieldType.MONTH,
        FieldType.ORGANIZATION,
        FieldType.PUBLISHER,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class Manual(Entry):
    entry_type = EntryType.MANUAL
    fields_required = [
        FieldType.TITLE,
    ]
    fields_optional = [
        FieldType.AUTHOR,
        FieldType.ORGANIZATION,
        FieldType.ADDRESS,
        FieldType.EDITION,
        FieldType.MONTH,
        FieldType.YEAR,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class MastersThesis(Entry):
    entry_type = EntryType.MASTERSTHESIS
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.SCHOOL,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.TYPE,
        FieldType.ADDRESS,
        FieldType.MONTH,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class Misc(Entry):
    entry_type = EntryType.MISC
    fields_required = []
    fields_optional = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.HOWPUBLISHED,
        FieldType.MONTH,
        FieldType.YEAR,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class PhdThesis(Entry):
    entry_type = EntryType.PHDTHESIS
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.SCHOOL,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.TYPE,
        FieldType.ADDRESS,
        FieldType.MONTH,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class Proceedings(Entry):
    entry_type = EntryType.PROCEEDINGS
    fields_required = [
        FieldType.TITLE,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.EDITOR,
        [FieldType.VOLUME, FieldType.NUMBER],
        FieldType.SERIES,
        FieldType.ADDRESS,
        FieldType.MONTH,
        FieldType.ORGANIZATION,
        FieldType.PUBLISHER,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class TechReport(Entry):
    entry_type = EntryType.TECHREPORT
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.INSTITUTION,
        FieldType.YEAR,
    ]
    fields_optional = [
        FieldType.TYPE,
        FieldType.NUMBER,
        FieldType.ADDRESS,
        FieldType.MONTH,
        FieldType.NOTE,
    ]


@dataclasses.dataclass(frozen=True)
class Unpublished(Entry):
    entry_type = EntryType.UNPUBLISHED
    fields_required = [
        FieldType.AUTHOR,
        FieldType.TITLE,
        FieldType.NOTE,
    ]
    fields_optional = [
        FieldType.MONTH,
        FieldType.YEAR,
    ]
