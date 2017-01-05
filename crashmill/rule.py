# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from everett.component import RequiredConfigMixin


class Rule(RequiredConfigMixin):
    '''A callable transformation for manipulating crash state.

    For ease of testing, this base class is implemented with predicate
    and action methods. Consumers are expected to call the object directly
    in practice.
    '''
    def __init__(self, config):
        self.config = config.with_options(self)

    def __call__(self, **kwargs):
        if self.predicate(**kwargs):
            return self.action(**kwargs)
        return False

    def predicate(self, **kwargs):
        """A test function to determine if the transformation should
        proceed. Supplied as a convenience method for testing and backwards
        compatibility. Defaults to True.

        :returns Bool: should the transformation proceed
        """
        return True

    def action(self, **kwargs):
        """The transformation to apply over the crash data. Supplied as a
        convenience method for testing and backwards compatability.
        """
        raise NotImplemented()


# TODO: define a base Rule class with a Postgres connexion.
