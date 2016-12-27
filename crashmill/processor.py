# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from crashmill.crash import Crash


class Processor:
    def __init__(self, queue, source, destination, rules):
        self.queue = queue
        self.source = source
        self.destination = destination
        self.rules = rules

    def run(self):
        for crash_id in self.queue:
            self.transform(crash_id)

    def transform(self, crash_id):
        crash = Crash(crash_id, self.source, self.destination)
        crash.fetch().transform(self.rules).save()
