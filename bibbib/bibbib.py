#!/usr/bin/python3
# bibbib - A bib for your BiBTeX
# Author: Adrian Caruana
from collections import Counter
import dataclasses
import inspect
from pathlib import Path
import sys
from typing import Iterable, List

import bibtexparser

import bibbib._constants
from ._errors import Error, GlobalError, EntryError, FieldError
from ._types import EntryType, FieldType


PARSER = bibtexparser.bparser.BibTexParser(common_strings=True)
ENTRY_LUT = {
    cls.__name__.lower(): cls
    for _, cls in inspect.getmembers(bibbib._constants)
    if inspect.isclass(cls)
    and issubclass(cls, bibbib._constants.Entry)
    and cls is not bibbib._constants.Entry
}


def reader(bibtex_path: Path):
    with open(bibtex_path) as f:
        bibtexdb = bibtexparser.load(f, parser=PARSER)
    return bibtexdb


@dataclasses.dataclass
class Validator:
    bibtexdb: bibtexparser.bibdatabase.BibDatabase
    _entries: List = dataclasses.field(default_factory=list, init=False)
    _errors: List = dataclasses.field(default_factory=list, init=False)

    def _get_entries(self, entries: Iterable):
        for entry in entries:
            _entry = ENTRY_LUT.get(
                entry["ENTRYTYPE"].lower(),
                EntryError(f"Unknown entry type: {entry['ENTRYTYPE']}."),
            )
            if isinstance(_entry, Error):
                self._errors.append(_entry)
                continue
            _key = entry.get(
                "ID",
                EntryError(f"Field 'key' missing from entry {entry['ENTRYTYPE']}."),
            )
            if isinstance(_key, Error):
                self._errors.append(_key)
            _entry = _entry(key=_key, bibtex_entry=entry)
            self._errors += _entry.field_errors
            self._entries.append(_entry)

    def _check_unique_keys(self):
        non_unique_keys = [
            k
            for (k, v) in Counter(
                list(map(lambda x: x.bibtex_entry.get("ID", None), self._entries))
            ).items()
            if v > 1
        ]
        for key in non_unique_keys:
            self._errors.append(GlobalError(f"Multiple entries exist with {key=}"))

    def run(self):
        self._get_entries(self.bibtexdb.entries)
        self._check_unique_keys()
        return self._errors


def bibbib(bibtex_path: Path = None, report: bool = False):
    cli = not bool(bibtex_path)
    if cli:
        if len(sys.argv[1:]) != 1:
            raise ValueError(f"Usage: bibbib /path/to/ref.bib")
        bibtex_path = Path(sys.argv[1])
    if not Path(bibtex_path).exists():
        raise ValueError(f"No bibtex file exists at: {bibtex_path=}")
    bibtexdb = reader(Path(bibtex_path))
    errors = Validator(bibtexdb=bibtexdb).run()
    if cli or report:
        if errors:
            for e in errors:
                print(e.error_msg)
            print(f"Found {len(errors)} errors in bibtex! 💥 💔 💥")
        else:
            print("No errors found in bibtex! ✨ 🍰 ✨")
    if not cli:
        return errors


if __name__ == "__main__":
    bibbib()
