# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from everett.manager import (
    ConfigManager,
    ConfigEnvFileEnv,
    ConfigOSEnv,
    parse_class
)
from everett.component import ConfigOptions, RequiredConfigMixin

from crashmill.processor import Processor
from crashmill.rules import get_all_rules


class AppConfig(RequiredConfigMixin):
    '''This class handles the main configuration of the application.

    Note that the Processor class receives all its dependencies as arguments
    rather than through config keys. This makes testing a lost easier, and
    makes the sub-parts of the app more flexible.

    For example, the Processor expects its `queue` argument to be an iterable.
    You can thus pass it a simple list instead of an instance of a class you
    had to define.
    '''
    required_config = ConfigOptions()
    required_config.add_option(
        'logging_level',
        default='DEBUG',
        doc='The logging level to use. DEBUG, INFO, WARNING, ERROR or CRITICAL'
    )
    required_config.add_option(
        'source',
        default='crashmill.crash_store.NoOpCrashStore',
        parser=parse_class,
        doc='The class from which crash data will be taken',
    )
    required_config.add_option(
        'destination',
        default='crashmill.crash_store.NoOpCrashStore',
        parser=parse_class,
        doc='The class into which transformed crash data will be put',
    )
    required_config.add_option(
        'queue',
        default='crashmill.queue.NoOpQueue',
        parser=parse_class,
        doc='The class from which new crash ids will come. Must be iterable',
    )

    def __init__(self, config):
        self.config_manager = config
        self.config = config.with_options(self)

    def __call__(self, key):
        return self.config(key)


def main(config=None):
    '''Get the Crash Mill runnin'. '''
    if config is None:
        config = ConfigManager([
            # Pull configuration from env file specified as ANTENNA_ENV
            ConfigEnvFileEnv([os.environ.get('ANTENNA_ENV')]),
            # Pull configuration from environment variables
            ConfigOSEnv()
        ])

    app_config = AppConfig(config)

    queue = app_config('queue')(config)
    source = app_config('source')(config)
    destination = app_config('destination')(config)

    rules = get_all_rules(config)

    processor = Processor(queue, source, destination, rules)
    processor.run()


if __name__ == '__main__':
    main()
