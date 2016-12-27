# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from crashmill.crash import Crash

from tests.unittest.rules import EmptyRule, IdentityRule
from tests.unittest.stores import FakeDestStore, FakeSourceStore


class TestCrash:
    def test_fetch(self):
        crash_id = 'abcdefgh-ijkl-mnop-qrst-uvwxyz012345'
        source = FakeSourceStore()

        crash = Crash(crash_id, source=source, destination=None)
        res = crash.fetch()

        assert res == crash
        assert 'Foo' in crash.raw_crash
        assert crash.raw_crash['Foo'] == 'bar'

    def test_save(self):
        crash_id = 'abcdefgh-ijkl-mnop-qrst-uvwxyz012345'
        destination = FakeDestStore()

        crash = Crash(crash_id, source=None, destination=destination)
        crash._internal_data['raw_crash'] = {
            'Foo': 'bar',
        }
        crash._internal_data['processed_crash'] = {
            'answer': 42,
        }

        res = crash.save()
        assert res == crash

        assert crash_id in destination._stored

        store = destination._stored[crash_id]
        assert 'Foo' in store['raw_crash']
        assert store['raw_crash']['Foo'] == 'bar'

        assert store['dumps'] == {}

        assert 'answer' in store['processed_crash']
        assert store['processed_crash']['answer'] == 42

    def test_transform_several_rules(self):
        crash_id = 'abcdefgh-ijkl-mnop-qrst-uvwxyz012345'
        crash = Crash(crash_id, source=None, destination=None)

        crash._internal_data['raw_crash'] = {
            'Foo': 'bar',
        }

        rules = [
            EmptyRule(),
            IdentityRule(),
        ]

        res = crash.transform(rules)
        assert res == crash

        assert 'Foo' in crash.raw_crash
        assert crash.raw_crash['Foo'] == 'bar'

        assert 'Foo' in crash.processed_crash
        assert crash.processed_crash['Foo'] == 'bar'

    def test_transform_one_rule(self):
        crash_id = 'abcdefgh-ijkl-mnop-qrst-uvwxyz012345'
        crash = Crash(crash_id, source=None, destination=None)

        crash._internal_data['raw_crash'] = {
            'Foo': 'bar',
        }

        res = crash.transform(IdentityRule())
        assert res == crash

        assert 'Foo' in crash.raw_crash
        assert crash.raw_crash['Foo'] == 'bar'

        assert 'Foo' in crash.processed_crash
        assert crash.processed_crash['Foo'] == 'bar'
