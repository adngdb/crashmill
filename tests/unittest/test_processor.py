# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittest import mock

from crashmill.processor import Processor

from tests.unittest.rules import IdentityRule
from tests.unittest.stores import FakeDestStore, FakeSourceStore


class TestProcessor:
    def _get_processor(self, queue=None, rules=None):
        queue = queue or []
        rules = rules or []

        source = FakeSourceStore()
        destination = FakeDestStore()

        processor = Processor(queue, source, destination, rules)
        return processor

    @mock.patch('crashmill.processor.Crash')
    def test_transform(self, m_crash):
        mocked_crash = mock.Mock()
        mocked_crash.fetch.return_value = mocked_crash
        mocked_crash.transform.return_value = mocked_crash
        mocked_crash.save.return_value = mocked_crash

        m_crash.return_value = mocked_crash

        rules = [IdentityRule()]
        processor = self._get_processor(rules=rules)
        processor.transform('abcdefgh-ijkl-mnop-qrst-uvwxyz012345')

        mocked_crash.fetch.assert_called_once_with()
        mocked_crash.save.assert_called_once_with()

        mocked_crash.transform.assert_called_once_with(rules)

    @mock.patch('crashmill.processor.Crash')
    def test_run(self, m_crash):
        calls = []

        def save_calls(*args, **kwargs):
            calls.append(args[0])
            return mock.Mock()
        m_crash.side_effect = save_calls

        queue = ('a', 'b', 'c')
        processor = self._get_processor(queue=queue)

        processor.run()

        assert calls == list(queue)
