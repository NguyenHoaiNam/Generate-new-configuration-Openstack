# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor.getconf import oldconf
from jor.getconf import crudini as cru
from jor.mapconf import load_yaml as load
from oslo_config import cfg

OPTION_IN_FILE = None


def mapping_config(path_new_file, CONF, namespaces):
    global OPTION_IN_FILE
    OPTION_IN_FILE = oldconf.get_config_file(CONF)
    for namespace in namespaces:
        try:
            template_dict = load.get_template(namespace)
            deprecation_options = template_dict['deprecated_options']
            new_options = template_dict['new_options']
        except (IOError, TypeError):
            # There is no yaml file or the file is be wrong format.
            # So we will continue with other namespace.
            continue
        for section, values in deprecation_options.items():
            # If the yaml file has dynamic section then we need to invoke
            # a function to solve this section.
            if section == 'dynamic_section':
                old_dynamic_section = deprecation_options['dynamic_section']
                new_dynamic_section = new_options['dynamic_section']
                key_dynamic = template_dict['option_enable_dynamic']['name']
                group_key_dynamic = \
                    template_dict['option_enable_dynamic']['group']
                value_dynamic = CONF[group_key_dynamic][key_dynamic]
                solve_dynamic_section(path_new_file=path_new_file,
                                      old_dynamic_section=old_dynamic_section,
                                      new_dynamic_section=new_dynamic_section,
                                      value_dynamic=value_dynamic,
                                      CONF=CONF)
            else:
                for value in values:
                    old_key = value['name']
                    try:
                        old_value = CONF[section][old_key]
                    except cfg.NoSuchOptError:
                        # There is no value with this key so we will continue
                        # with other value.
                        continue
                    old_key_group = (section, old_key, old_value)
                    if old_key_group not in OPTION_IN_FILE:
                        # We only solve options that have in the config file
                        continue
                    new_key = value['replacement_name']
                    new_group = value['replacement_group']
                    change_value, template, mapping = \
                        load.get_all_params(new_options=new_options,
                                            section=new_group, key=new_key)
                    if (change_value.upper() == 'NONE') and (
                                mapping.upper() == 'NONE'):
                        new_value = old_value
                    else:
                        if template.upper() != 'NONE':
                            change_value_no_space = change_value.replace(" ",
                                                                         "")
                            change_value_list = \
                                change_value_no_space.split(',')
                            change_value_real = [CONF[section][n] for
                                                 n in change_value_list]

                            new_value = template.format(*change_value_real)
                        elif mapping.upper() != 'NONE':
                            mapping_dict = load.string_to_dict(mapping)
                            new_value = mapping_dict[old_value]
                        else:
                            pass
                    # Adding new option to the new file
                    cru.set_option_file(name_file=path_new_file,
                                        section=new_group,
                                        key=new_key,
                                        value=load.list_to_string(new_value))
                    # Delete the option in the list of option changed
                    load.delete_option_deprecate(OPTION_IN_FILE,
                                                 old_key_group)


def solve_dynamic_section(path_new_file, old_dynamic_section,
                          new_dynamic_section, value_dynamic, CONF):
    for section_dynamic in value_dynamic:
        for value in old_dynamic_section:
            old_key = value['name']
            old_value = CONF[section_dynamic][old_key]
            old_value_string = load.list_to_string(old_value)
            group_dynamic = (section_dynamic, old_key, old_value_string)
            if group_dynamic not in OPTION_IN_FILE:
                # Don't need to solve
                continue
            new_key = value['replacement_name']
            change_value, template, mapping = \
                load.get_all_params(new_options=new_dynamic_section,
                                    key=new_key)
            if change_value.upper() == 'NONE' and mapping.upper() == 'NONE':
                new_value = old_value
            else:
                if template.upper() != 'NONE':
                    change_value_no_space = change_value.replace(" ", "")
                    change_value_list = change_value_no_space.split(',')
                    change_value_real = \
                        [load.get_value_from_option_in_file(OPTION_IN_FILE,
                                                            section_dynamic, n)
                         for n in change_value_list]
                    new_value = template.format(*change_value_real)
                elif mapping.upper() != 'NONE':
                    mapping_dict = load.string_to_dict(mapping)
                    try:
                        new_value = mapping_dict[old_value]
                    except KeyError:
                        # In case, there is no result in mapping then we will
                        # use old value
                        new_value = old_value
            cru.set_option_file(name_file=path_new_file,
                                section=section_dynamic,
                                key=new_key,
                                value=load.list_to_string(new_value))
            old_key_group = (section_dynamic, old_key, old_value)
            load.delete_option_deprecate(OPTION_IN_FILE,
                                         old_key_group)


def add_options_ne_default(path_new_file, CONF):
    """
    This function will move options that is not equal with default and is not
    deprecated.
    """
    for section, key, _value in OPTION_IN_FILE:
        try:
            value = CONF[section][key]
        except cfg.NoSuchOptError:
            value = _value
        cru.set_option_file(name_file=path_new_file, section=section, key=key,
                            value=load.list_to_string(value))
