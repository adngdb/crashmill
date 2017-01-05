# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class Crash:
    '''Internal representation of a crash report.

    Storing the data inside a dict allows for easier extensibility. One
    thing I do that is not in lonnen/processor is passing the data as
    `**self._internal_data` to rules. This way, when you want to add some
    data to the crash report, it will automatically be passed to all rules,
    and those that care about it will have it.

    I made the various keys accessible as properties, but I'm not actually
    sure that's going to be useful. It will if we ever use this class
    outside the context of the Processor class, I guess, but I don't know
    how likely it is that such a thing will happen.

    I don't use the `.pipeline()` concept because that's actually not very
    pythonic. We would actually just pass a list instead of several
    arguments. There is little good in supporting that.

    I'm keeping the concept of "poly crash store" from Socorro, that makes
    the code quite easier, since then this class only cares about a source and
    a destination.
    '''
    def __init__(self, crash_id, source, destination):
        self.source = source
        self.destination = destination

        self.errors = []

        self._internal_data = {
            'crash_id': crash_id,
            'raw_crash': {},
            'dumps': {},
            'processed_crash': {},
        }

    @property
    def crash_id(self):
        return self._internal_data['crash_id']

    @property
    def raw_crash(self):
        return self._internal_data['raw_crash']

    @property
    def dumps(self):
        return self._internal_data['dumps']

    @property
    def processed_crash(self):
        return self._internal_data['processed_crash']

    def fetch(self):
        self._internal_data['raw_crash'] = self.source.get_raw_crash(
            self.crash_id
        )
        self._internal_data['dumps'] = self.source.get_dumps(
            self.crash_id
        )
        self._internal_data['processed_crash'] = (
            self.source.get_processed_crash(self.crash_id)
        )
        return self

    def transform(self, rules):
        if not isinstance(rules, (tuple, list)):
            rules = [rules]

        for rule in rules:
            try:
                rule(**self._internal_data)
            except Exception as e:
                self.errors.append(str(e))
                # TODO: log the error with its stack trace.

        return self

    def save(self):
        self.destination.save_crash(**self._internal_data)
        return self
