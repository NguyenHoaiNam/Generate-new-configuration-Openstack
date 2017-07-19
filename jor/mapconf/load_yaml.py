# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor import utils
import yaml


def load_yaml(name_file):
    f = open(name_file)
    content_dict = yaml.safe_load(f)
    f.close()
    return content_dict


def get_template(namespace):
    """
    :param namespace: the namespace of a project like nova, keystone,
    oslo_messaging.
    :return: a dictionary.
    """
    namespace = namespace.replace(".", "_")
    template_yaml = namespace + '.yaml'
    template_path_name = utils.get_root_path('templates', template_yaml)
    return load_yaml(template_path_name)


def list_to_string(list_convert):
    if type(list_convert) is list:
        return ', '.join(list_convert)
    else:
        # The input is not a list
        return list_convert


def get_param(CONF, section, key, param):
    """
    :param CONF:
    :param section:
    :param key:
    :return: value
    """
    for option in CONF[section]:
        if option['name'] == key:
            return option[param]


def map_param(list_map, key):
    for i in list_map:
        i.key() == key
        return i.value()


def delete_option_deprecate(change_default_option, *options):
    for option in options:
        try:
            return change_default_option.remove(option)
        except ValueError:
            pass


def string_to_dict(inputs_string):
    value_dict = {}
    for input_string in inputs_string.replace(" ", "").split(','):
        key = input_string.split(':')[0]
        value = input_string.split(':')[1]
        value_dict[key] = value
    return value_dict
