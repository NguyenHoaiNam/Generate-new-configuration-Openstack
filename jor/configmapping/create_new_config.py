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
    template_yaml = namespace + '.yaml'
    template_path_name = utils.get_root_path('templates', template_yaml)
    return load_yaml.load_yaml(template_path_name)


def make_global_option(namespace):
    global DEPRECATED_OPTIONS, NEW_OPTIONS
    template_dict = get_template(namespace)
    DEPRECATED_OPTIONS = template_dict['deprecated_options']
    NEW_OPTIONS = template_dict['new_options']


def check_value(new_options, session, key):
    for option in new_options[session]:
        if option['name'] == key:
            return option['value']


def delete_option_deprecate(change_default_option, option):
    try:
        return change_default_option.remove(option)
    except ValueError:
        return None


# 1
def change_old_config_to_new(name_new_file, CONF):
    # Start for with deprecated options
    global CHANGE_DEFAULT_OPTION
    CHANGE_DEFAULT_OPTION = oldconf.get_ne_default(CONF)
    for session, values in DEPRECATED_OPTIONS.items():
        for value in values:
            old_key_config = value['name']
            try:
                old_value_config = CONF[session][old_key_config]
            except Exception:
                continue
            tuple_option_deprecate = (session, old_key_config)
            new_name_config = value['replacement_name']
            new_group_config = value['replacement_group']
            new_change_value = check_value(NEW_OPTIONS,
                                           session=new_group_config,
                                           key=new_name_config)
            if new_change_value == 'None':
                new_value_config = old_value_config
            else:
                # TODO(namnh):
                pass
            # Create a new file for new release
            cru.set_option_file(name_file=name_new_file,
                                session=new_group_config,
                                key=new_name_config,
                                value=new_value_config)
            # Delete the option in the list of option changed
            delete_option_deprecate(CHANGE_DEFAULT_OPTION,
                                    tuple_option_deprecate)


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
                            value=value)


CONF = oldconf.get_conf()
make_global_option('barbican')
change_old_config_to_new(NAME_NEW_FILE, CONF)
move_option_changed(NAME_NEW_FILE, CONF)
