# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

import importlib

from oslo_config import cfg
from oslo_config import generator as gn

__all__ = ['get_conf', 'get_config_file']


DYNAMIC_SECTION_PROJECTS = {
    'cinder': 'jor.getconf.dynamic_section.cinder'
}


def get_conf(conf_file=None, config_file=None):
    conf = cfg.ConfigOpts()
    gn.register_cli_opts(conf)
    oslo_args = ['--config-file', conf_file]
    conf(oslo_args)
    groups = gn._get_groups(gn._list_opts(conf.namespace))

    # Make new CONF
    new_conf = cfg.ConfigOpts()
    project_args = ['--config-file', config_file]
    new_conf(project_args)
    all_namespaces = []
    for k, v in groups.items():
        group = cfg.OptGroup(k)
        try:
            namespaces = v.get('namespaces', [])
        except Exception:
            namespaces = v
        list_opts = []
        for namespace in namespaces:
            all_namespaces.append(namespace[0])
            list_opts.extend(namespace[1])
        new_conf.register_group(group)
        if k == 'DEFAULT':
            try:
                new_conf.register_opts(list_opts)
            except cfg.DuplicateOptError:
                continue
        new_conf.register_opts(list_opts, group=group)
    projects = []
    for namespace in all_namespaces:
        sp = namespace.split('.')
        if 'oslo' in namespace:
            projects.append(".".join(sp[:2]))
        else:
            projects.append(sp[0])

    for project in projects:
        try:
            get_name_module = DYNAMIC_SECTION_PROJECTS[project]
        except KeyError:
            # This project does not have dynamic section
            continue
        dynamic = importlib.import_module(get_name_module)
        dynamic.register_dynamic_section(new_conf)

    return new_conf, set(projects)


def get_ne_default(conf=None):
    ne_dict = []
    if isinstance(conf, cfg.ConfigOpts):
        for name, group in conf._groups.items():
            for option, opt in group._opts.items():
                if conf[name][option] != opt['opt'].default:
                    ne_dict.append((name, option))
    return ne_dict


def get_config_file(conf=None):
    _list = []
    if conf:
        section_options = conf._namespace._parsed[0]
        for name, section in section_options.items():
            for option, value in section.items():
                _list.append((name, option, value[0]))
    return _list
