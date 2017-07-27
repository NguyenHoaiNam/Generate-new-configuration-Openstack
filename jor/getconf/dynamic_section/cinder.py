# Copyright 2017 Dai Dang Van and Nam Nguyen Hoai
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

__author__ = ['Dai Dang Van', 'Nam Nguyen Hoai']

"""
    Register dynamic sections and list corresponding options
"""
from oslo_config import cfg

DYNAMIC_LIST = 'enabled_backends'
DEFAULT_BACKEND = 'DEFAULT'


def register_dynamic_section(conf):
    """ Register dynamic sections and list corresponding options
    :return: dict
    """
    sections = conf[DYNAMIC_LIST]
    dict_opts = {}
    if DEFAULT_BACKEND == 'DEFAULT':
        dict_opts = conf._opts
    else:
        dict_opts = conf._groups[DEFAULT_BACKEND]._opts
    list_opts = []
    for name, option in dict_opts.items():
        list_opts.append(option['opt'])
    for section in sections:
        conf.register_opts(list_opts, group=cfg.OptGroup(section))
