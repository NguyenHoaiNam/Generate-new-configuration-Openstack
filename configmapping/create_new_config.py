# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

import load_yaml
import utils


def receive_old_config(namespace, CONF):
    """
    :param namespace: the namespace of a project like nova, keystone,
    oslo_messaging.
    :param CONF: the CONF object of old configuration.
    :return:
    """

    if namespace == 'nova.conf':
        template_yaml = 'nova.yaml'
    elif namespace == 'keystone':
        template_yaml = 'keystone.yaml'
    elif namespace == 'oslo_messaging':
        template_yaml = 'oslo_messing'
    else:
        raise Exception
    template_path_name = utils.get_root_path('templates', template_yaml)
    template_dict = load_yaml.load_yaml(template_path_name)
    option_depricate = template_dict['deprecated_options']

    # Start for
    for i in option_depricate:
        pass
    getattr()



