import nova.conf

CONF = nova.conf.CONF
CONF(['--config-file', '/etc/nova/nova.conf'])


def get_value_and_default(name=None, group=None):
    """ Get value of option and itself default.
    :param name:
    :param group:
    :return: (value, default)
    """
    if not name:
        return None, None
    if group:
        value = CONF[group][name]
        default = CONF._groups[group]._opts[name]['opt'].default
    else:
        value = CONF[name]
        default = CONF._opts[name]['opt'].default
    return value, default


if __name__ == '__main__':
    print(get_value_and_default('api_paste_config', 'wsgi'))
    print(get_value_and_default('my_ip'))
