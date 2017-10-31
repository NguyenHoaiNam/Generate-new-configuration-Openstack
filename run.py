#!/usr/bin/python
# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

import argparse
import os
import sys

from jor.getconf import oldconf
from jor.mapconf import gen_conf

path = os.path.dirname(os.path.abspath(__file__))


class JorShell(object):

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            prog='jor',
            add_help=True,
        )

        # Global arguments
        parser.add_argument('--namespace-file',
                            help="Config file contain namespaces.",
                            required=True)

        parser.add_argument('--old-config-file',
                            help="Old config file for your ENV",
                            required=True)

        parser.add_argument('--new-config-file',
                            help="New config file for your ENV. For example:"
                                 "neutron.conf",
                            required=True)

        parser.add_argument('--release-target',
                            help='Release target which you want to generate',
                            required=True)

        return parser

    def main(self, argv):
        # Parse args once to find version
        parser = self.get_base_parser()
        # NOTE(daidv): we will pass unknown inputs instead of use parse_args.
        all_options, _ = parser.parse_known_args(argv)
        return all_options


if __name__ == '__main__':
    shell = JorShell()
    options = shell.main(sys.argv[1:])
    CONF, namespaces = oldconf.get_conf(
        options.namespace_file, options.old_config_file)
    path_new_config = os.path.join(path, options.new_config_file)
    gen_conf.mapping_config(path_new_config, CONF, namespaces,
                            options.release_target)
    gen_conf.add_options_ne_default(path_new_config, CONF)
