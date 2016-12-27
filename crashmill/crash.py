# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class Crash:
    def __init__(self, crash_id, source, destination):
        self.source = source
        self.destination = destination

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
        self._internal_data['dumps'] = self.source.get_raw_dumps(
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
            rule(**self._internal_data)

        return self

    def save(self):
        self.destination.save_raw_crash(
            self.crash_id, self.raw_crash
        )
        self.destination.save_raw_dumps(
            self.crash_id, self.dumps
        )
        self.destination.save_processed_crash(
            self.crash_id, self.processed_crash
        )
        return self
