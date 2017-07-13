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
    for k, v in groups.items():
        group = cfg.OptGroup(k)
        namespaces = v.get('namespaces', [])
        list_opts = []
        for namespace in namespaces:
            list_opts.extend(namespace[1])
        new_conf.register_group(group)
        if k == 'DEFAULT':
            new_conf.register_opts(list_opts)
        new_conf.register_opts(list_opts, group=group)

    nova_args = ['--config-file', config_file]
    new_conf(nova_args)
    return new_conf


def get_ne_default(conf=None):
    ne_dict = []
    if isinstance(conf, cfg.ConfigOpts):
        for name, group in conf._groups.items():
            for option, opt in group._opts.items():
                if conf[name][option] != opt['opt'].default:
                    ne_dict.append((name, option))
    return ne_dict


if __name__ == '__main__':
    conf = get_conf()
    get_ne_default(conf)
