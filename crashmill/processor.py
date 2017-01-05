# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from crashmill.crash import Crash


class Processor:
    '''A processor with just the basic behavior.

    Consumes a queue of crash ids until it's done, and for each id,
    create a Crash object, fetch -> transform -> save.

    It handles all the needed dependencies:
        * queue
        * source store
        * destination store
        * list of rules to apply

    Note that all dependencies are passed as arguments rather than through
    configuration. I _think_ this is better, because it makes each part
    easier to unit test, and it means we can very easily use them for other
    things. For example, in this case, the only restriction on the `queue`
    argument is that it must be iterable. You can thus pass it a python list
    if you so desire.

    Basically, my idea for this class is to be responsible of the main
    process (algorithm) and the error handling. Everything related to data
    should be put into rules. For example, Socorro's processor creates a
    bunch of meta data around processing (called `processed_notes` or
    `processor_meta`). That can, and should, be done in a rule instead. Same
    for the various data about the job, like the starting and ending times.
    '''
    def __init__(self, queue, source, destination, rules):
        self.queue = queue
        self.source = source
        self.destination = destination
        self.rules = rules

    def run(self):
        '''Consume the queue until it is over.

        Note that it is the responsibility of the caller to ensure the queue
        never runs out, or to enclose this `run()` call into another loop,
        to make this a never-ending process.
        '''
        for crash_id in self.queue:
            self.transform(crash_id)

    def transform(self, crash_id):
        crash = Crash(crash_id, self.source, self.destination)
        crash.fetch().transform(self.rules).save()
