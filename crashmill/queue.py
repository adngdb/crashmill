# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from everett.component import RequiredConfigMixin


class Queue(RequiredConfigMixin):
    '''An iterable that returns crash ids.
    '''
    def __init__(self, config):
        self.config = config.with_options(self)

    def __iter__(self):
        pass


class NoOpQueue(Queue):
    def __iter__(self):
        return None
