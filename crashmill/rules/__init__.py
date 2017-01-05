# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from importlib import import_module


'''Currently this is a list of modules, but it should actually be a list
of rule sets. A rule set is simply a named list of rules. The important
feature will be to be able to easily run only a specific rule set, without
having to write down the list of rules in a different place.
'''
RULES_LIST = (
    # Raw Crash transform rules.
    # Various improvements and transformations on the raw crash data.
    'crashmill.rules.raw_transforms.SomeRule',
    # Raw to Processed transform rules.
    # Create the processed crash from the raw crash and the dumps.
    'crashmill.rules.processed_init.Foo',
    # Processed Crash transform rules.
    # Various improvements and transformations on the processed crash data.
    'crashmill.rules.processed_transform.Bar',
    # Signature generation rules.
    # Generate a signature for the crash.
    'crashmill.rules.signature.Baz',
)


def get_all_rules(config):
    all_rules = []
    for module in RULES_LIST:
        rule = import_module(module)
        all_rules.append(rule(config))
    return all_rules
