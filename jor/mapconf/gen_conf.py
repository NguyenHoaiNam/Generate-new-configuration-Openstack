# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor.getconf import oldconf
from jor.getconf import crudini as cru
from jor.mapconf import load_yaml as load

CHANGE_DEFAULT_OPTION = None


def mapping_config(path_new_file, CONF, namespaces):
    global CHANGE_DEFAULT_OPTION
    CHANGE_DEFAULT_OPTION = oldconf.get_ne_default(CONF)
    for namespace in namespaces:
        try:
            template_dict = load.get_template(namespace)
            deprecation_options = template_dict['deprecated_options']
            new_options = template_dict['new_options']
        except (IOError, TypeError):
            continue
        for session, values in deprecation_options.items():
            for value in values:
                old_key = value['name']
                try:
                    old_value = CONF[session][old_key]
                except Exception:
                    continue
                old_key_group = (session, old_key)
                if old_key_group not in CHANGE_DEFAULT_OPTION:
                    continue
                new_key = value['replacement_name']
                new_group = value['replacement_group']
                new_key_group = (new_group, new_key)
                change_value = load.get_param(CONF=new_options, param='value',
                                              session=new_group, key=new_key)
                template = load.get_param(CONF=new_options, session=new_group,
                                          key=new_key, param='template')
                mapping = load.get_param(CONF=new_options, session=new_group,
                                         key=new_key, param='mapping')
                if change_value.upper() == 'NONE':
                    new_value = old_value
                else:
                    if template.upper() != 'NONE':
                        change_value_no_space = change_value.replace(" ", "")
                        change_value_list = change_value_no_space.split(',')
                        change_value_real = [CONF[session][n] for
                                             n in change_value_list]

                        new_value = template.format(*change_value_real)
                    else:
                        pass
                # Adding new option to the new file
                cru.set_option_file(name_file=path_new_file,
                                    session=new_group,
                                    key=new_key,
                                    value=load.list_to_string(new_value))
                # Delete the option in the list of option changed
                load.delete_option_deprecate(CHANGE_DEFAULT_OPTION,
                                             old_key_group)
                load.delete_option_deprecate(CHANGE_DEFAULT_OPTION,
                                             new_key_group)


def add_options_ne_default(path_new_file, CONF):
    """
    This function will move options that is not equal with default and is not
    deprecated.
    """
    for session, key in CHANGE_DEFAULT_OPTION:
        value = CONF[session][key]
        cru.set_option_file(name_file=path_new_file, session=session, key=key,
                            value=load.list_to_string(value))
