# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from oslo_config import cfg
from oslo_config import generator as gn

__all__ = ['get_conf']


def get_conf(conf_file=None, config_file=None):
    conf_file = '/opt/stack/barbican/etc/oslo-config-generator/barbican.conf'
    config_file = '/etc/barbican/barbican.conf'

    conf = cfg.ConfigOpts()
    gn.register_cli_opts(conf)
    oslo_args = ['--config-file', conf_file]
    conf(oslo_args)
    groups = gn._get_groups(gn._list_opts(conf.namespace))

    # Make new CONF
    new_conf = cfg.ConfigOpts()
    all_namespaces = []
    for k, v in groups.items():
        group = cfg.OptGroup(k)
        namespaces = v.get('namespaces', [])
        list_opts = []
        for namespace in namespaces:
            all_namespaces.append(namespace[0])
            list_opts.extend(namespace[1])
        new_conf.register_group(group)
        if k == 'DEFAULT':
            new_conf.register_opts(list_opts)
        new_conf.register_opts(list_opts, group=group)

    nova_args = ['--config-file', config_file]
    new_conf(nova_args)

    # A bad hacking thing.
    projects = []
    for namespace in all_namespaces:
        sp = namespace.split('.')
        if 'oslo' in namespace:
            projects.append(".".join(sp[:2]))
        else:
            projects.append(sp[0])

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
        for name, section in conf._namespace._parsed[0].items():
            for option in section:
                _list.append((name, option))
    return _list


if __name__ == '__main__':
    conf, projects = get_conf()
    print get_config_file(conf)
