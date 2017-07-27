# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor import utils
import yaml


def load_yaml(name_file):
    with open(name_file, 'r') as f:
        content_dict = yaml.safe_load(f)
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


def get_value_from_option_in_file(option_in_file, section, key):
    for _section, _key, _value in option_in_file:
        if _section == section and _key == key:
            return _value
        else:
            pass


def get_all_params(new_options, key, section=None):
    if section is None:
        for i in new_options:
            if i['name'] == key:
                return i['value'], i['template'], i['mapping']
    else:
        for i in new_options[section]:
            if i['name'] == key:
                return i['value'], i['template'], i['mapping']
