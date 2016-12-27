# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class FakeSourceStore:
    def get_raw_crash(self, crash_id):
        return {
            'Foo': 'bar',
        }

    def get_raw_dumps(self, crash_id):
        return {}

    def get_processed_crash(self, crash_id):
        return {}


class FakeDestStore:
    def __init__(self):
        self._stored = {}

    def _make_crash_document(self, crash_id):
        if crash_id not in self._stored:
            self._stored[crash_id] = {}

    def save_raw_crash(self, crash_id, raw_crash):
        self._make_crash_document(crash_id)
        self._stored[crash_id]['raw_crash'] = raw_crash
        return True

    def save_raw_dumps(self, crash_id, dumps):
        self._make_crash_document(crash_id)
        self._stored[crash_id]['dumps'] = dumps
        return True

    def save_processed_crash(self, crash_id, processed_crash):
        self._make_crash_document(crash_id)
        self._stored[crash_id]['processed_crash'] = processed_crash
        return True
