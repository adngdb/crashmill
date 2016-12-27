# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class EmptyRule:
    def __call__(self, crash_id, raw_crash, dumps, processed_crash):
        return True


class IdentityRule:
    def __call__(self, crash_id, raw_crash, dumps, processed_crash):
        processed_crash.update(raw_crash)
        return True
