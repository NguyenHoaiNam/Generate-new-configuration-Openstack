# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor import utils
from jor.getconf import oldconf
from jor.getconf import crudini as cru
import load_yaml


NAME_NEW_FILE = utils.get_root_path('new_config_file', 'barbican_new.conf')
DEPRECATED_OPTIONS = None
NEW_OPTIONS = None
CHANGE_DEFAULT_OPTION = None


def get_template(namespace):
    """
    :param namespace: the namespace of a project like nova, keystone,
    oslo_messaging.
    :return: a dictionary.
    """
    namespace = namespace.replace(".", "_")
    template_yaml = namespace + '.yaml'
    template_path_name = utils.get_root_path('templates', template_yaml)
    return load_yaml.load_yaml(template_path_name)


def make_global_option(namespace):
    global DEPRECATED_OPTIONS, NEW_OPTIONS
    template_dict = get_template(namespace)
    DEPRECATED_OPTIONS = template_dict['deprecated_options']
    NEW_OPTIONS = template_dict['new_options']


def list_to_string(list_convert):
    if type(list_convert) is list:
        return ', '.join(list_convert)
    else:
        # The input is not a list
        return list_convert


def get_param(new_options, session, key, param):
    """
    :param new_options:
    :param session:
    :param key:
    :return: value
    """
    for option in new_options[session]:
        if option['name'] == key:
            return option[param]


def check_template(new_options, session, key):
    """
    :param new_options:
    :param session:
    :param key:
    :return: template
    """
    for option in new_options[session]:
        if option['name'] == key:
            return option['template']


def check_mapping(new_options, session, key):
    """
    :param new_options:
    :param session:
    :param key:
    :return: mapping
    """
    for option in new_options[session]:
        if option['name'] == key:
            return option['mapping']


def delete_option_deprecate(change_default_option, option):
    try:
        return change_default_option.remove(option)
    except ValueError:
        pass


# 1
def change_old_config_to_new(name_new_file, CONF, namespaces):
    # Start for with deprecated options
    global CHANGE_DEFAULT_OPTION
    CHANGE_DEFAULT_OPTION = oldconf.get_ne_default(CONF)
    for namespace in namespaces:
        try:
            template_dict = get_template(namespace)
            deprecation_options = template_dict['deprecated_options']
            new_options = template_dict['new_options']
        except (IOError, TypeError):
            continue
        for session, values in deprecation_options.items():
            for value in values:
                old_key_config = value['name']
                try:
                    old_value_config = CONF[session][old_key_config]
                except Exception:
                    continue
                tuple_option_deprecate_1 = (session, old_key_config)
                if tuple_option_deprecate_1 not in CHANGE_DEFAULT_OPTION:
                    continue
                if tuple_option_deprecate_1 not in CHANGE_DEFAULT_OPTION:
                    continue
                new_key_name = value['replacement_name']
                new_group_name = value['replacement_group']
                tuple_option_deprecate_2 = (new_group_name, new_key_name)
                new_change_value = get_param(new_options,
                                             session=new_group_name,
                                             key=new_key_name,
                                             param='value')
                new_template = get_param(new_options=new_options,
                                         session=new_group_name,
                                         key=new_key_name,
                                         param='template')
                # new_mapping = check_mapping(new_options=new_options,
                #                             session=new_group_name,
                #                             key=new_key_name)
                if new_change_value == 'None':
                    new_value_config = old_value_config
                else:
                    if new_template != 'None':
                        new_change_value_no_space = \
                            new_change_value.replace(" ", "")
                        new_change_value_list = \
                            new_change_value_no_space.split(',')
                        new_real_change_value = [CONF[session][n]
                                                 for n in new_change_value_list]

                        new_value_config = \
                            new_template.format(*new_real_change_value)
                    else:
                        pass
                # Create a new file for new release
                cru.set_option_file(name_file=name_new_file,
                                    session=new_group_name,
                                    key=new_key_name,
                                    value=list_to_string(new_value_config))
                # Delete the option in the list of option changed
                delete_option_deprecate(CHANGE_DEFAULT_OPTION,
                                        tuple_option_deprecate_1)
                delete_option_deprecate(CHANGE_DEFAULT_OPTION,
                                        tuple_option_deprecate_2)


# 2
def move_option_changed(name_new_file, CONF):
    """
    This function will move options that is not equal with default and is not
    deprecated.
    """
    for session, key in CHANGE_DEFAULT_OPTION:
        value = CONF[session][key]
        cru.set_option_file(name_file=name_new_file,
                            session=session,
                            key=key,
                            value=list_to_string(value))
