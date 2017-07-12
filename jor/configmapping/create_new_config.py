# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor import utils
from jor.getconf import oldconf
from jor.getconf import crudini as cru
import load_yaml


NAME_NEW_FILE = utils.get_root_path('new_config_file', 'oslo_new.conf')


def get_template(namespace):
    """
    :param namespace: the namespace of a project like nova, keystone,
    oslo_messaging.
    :return: a dictionary.
    """

    if namespace == 'nova.conf':
        template_yaml = 'nova.yaml'
    elif namespace == 'keystone':
        template_yaml = 'keystone.yaml'
    elif namespace == 'oslo_messaging':
        template_yaml = 'oslo_messaging.yaml'
    else:
        raise Exception
    template_path_name = utils.get_root_path('templates', template_yaml)
    return load_yaml.load_yaml(template_path_name)


def change_config(namespace, name_new_file, CONF):
    template_dict = get_template(namespace)
    deprecated_options = template_dict['deprecated_options']
    new_options = template_dict['new_options']
    # Start for with deprecated options
    for session, values in deprecated_options.items():
        for value in values:
            old_key_config = value['name']
            old_value_config = CONF[session][old_key_config]
            new_name_config = value['replacement_name']
            new_group_config = value['replacement_group']
            new_change_value = check_value(new_options,
                                           session=new_group_config,
                                           key=new_name_config)
            if new_change_value == 'None':
                new_value_config = old_value_config
            else:
                pass
            # Create a new file for new release
            cru.set_option_file(name_file=name_new_file,
                                session=new_group_config,
                                key=new_name_config,
                                value=new_value_config)


def check_value(new_options, session, key):
    for option in new_options[session]:
        if option['name'] == key:
            return option['value']


CONF = oldconf.get_conf()
change_config('oslo_messaging', NAME_NEW_FILE, CONF)
