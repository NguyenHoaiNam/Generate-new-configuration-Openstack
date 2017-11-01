# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

import importlib

from oslo_config import cfg
from oslo_config import generator as gn

from jor import utils

__all__ = ['get_conf', 'get_config_file']

LOG = utils.get_log(__name__)

DYNAMIC_SECTION_PROJECTS = {
    'cinder': 'jor.getconf.dynamic_section.cinder'
}


def get_conf(conf_file=None, config_file=None):
    """Get CONF object for specific project.
    """
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
            LOG.info("Force register DEFAULT group to easier access "
                    "configuration values in DEFAULT group.")
            try:
                new_conf.register_opts(list_opts)
            except cfg.DuplicateOptError:
<<<<<<< HEAD
                continue
        LOG.info("Register group %s into new_conf.", group.name)
=======
                pass
>>>>>>> 90a4cce... Update source-code
        new_conf.register_opts(list_opts, group=group)
    projects = []
    for namespace in all_namespaces:
        sp = namespace.split('.')
        LOG.info("Get project name from namespaces.")
        if 'oslo' in namespace:
            LOG.info("Support getting project name for Oslo projects.")
            projects.append(".".join(sp[:2]))
        else:
            projects.append(sp[0])

    for project in projects:
        LOG.info("Autoload all dynamic section.")
        try:
            get_name_module = DYNAMIC_SECTION_PROJECTS[project]
        except KeyError:
            LOG.info("%s project does not have dynamic section or "
                    "not is not supported now.")
            continue
        dynamic = importlib.import_module(get_name_module)
        dynamic.register_dynamic_section(new_conf)

    return new_conf, set(projects)


def get_ne_default(conf=None):
    """Get not equal default value option.
    """
    ne_dict = []
    if isinstance(conf, cfg.ConfigOpts):
        for name, group in conf._groups.items():
            for option, opt in group._opts.items():
                if conf[name][option] != opt['opt'].default:
                    ne_dict.append((name, option))
    return ne_dict


def get_config_file(conf=None):
    """Parsing config file following ini format.
    """
    _list = []
    if conf:
        section_options = conf._namespace._parsed[0]
        for name, section in section_options.items():
            for option, value in section.items():
                _list.append((name, option, value[0]))
    return _list
