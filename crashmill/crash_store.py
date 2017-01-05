# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from everett.component import RequiredConfigMixin


class CrashStore(RequiredConfigMixin):
    '''The API of the crash stores changes a bit from Socorro and Antenna. The
    goal is to make it more consistent and easier to understand.

    Notable differences:
        * save_raw_and_processed -> save_crash
        * {get/save}_processed -> {get/save}_processed_crash
        * save_raw_crash and save_dumps are separated
          (used to be all done in save_raw_crash but that didn't make sense)
        * antenna uses `load` for `save`, but I find that really unclear
          (to me "load" doesn't convey a direction, up or down)
    '''
    def __init__(self, config):
        self.config = config.with_options(self)

    def save_crash(
        self,
        crash_id='',
        raw_crash=None,
        dumps=None,
        processed_crash=None,
        **kwargs
    ):
        self.save_raw_crash(crash_id, raw_crash)
        self.save_dumps(crash_id, dumps)
        self.save_processed_crash(crash_id, processed_crash)

        return True

    def save_raw_crash(self, crash_id, raw_crash):
        pass

    def save_dumps(self, crash_id, dumps):
        pass

    def save_processed_crash(self, crash_id, processed_crash):
        pass

    def get_raw_crash(self, crash_id):
        pass

    def get_dumps(self, crash_id):
        pass

    def get_processed_crash(self, crash_id):
        pass


class NoOpCrashStore(CrashStore):
    '''A CrashStore that does nothing on `save` and returns
    empty dicts on `get`. '''
    def get_raw_crash(self, crash_id):
        return {}

    def get_dumps(self, crash_id):
        return {}

    def get_processed_crash(self, crash_id):
        return {}
