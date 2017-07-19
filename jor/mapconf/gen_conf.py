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
            continue
        for section, values in deprecation_options.items():
            if section == 'dynamic_section':
                solve_dynamic_section(path_new_file=path_new_file,
                                      new_options=new_options,
                                      deprecation_options=deprecation_options,
                                      option_enable_dynamic=template_dict,
                                      CONF=CONF)
            else:
                for value in values:
                    old_key = value['name']
                    try:
                        old_value = CONF[section][old_key]
                    except cfg.NoSuchOptError:
                        continue
                    old_key_group = (section, old_key)
                    if old_key_group not in OPTION_IN_FILE:
                        continue
                    new_key = value['replacement_name']
                    new_group = value['replacement_group']
                    change_value = load.get_param(CONF=new_options,
                                                  param='value',
                                                  section=new_group,
                                                  key=new_key)
                    template = load.get_param(CONF=new_options,
                                              section=new_group, key=new_key,
                                              param='template')
                    mapping = load.get_param(CONF=new_options,
                                             section=new_group, key=new_key,
                                             param='mapping')
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


def solve_dynamic_section(path_new_file, new_options, deprecation_options,
                          option_enable_dynamic, CONF):
    old_dynamic_section = deprecation_options['dynamic_section']
    new_dynamic_section = new_options['dynamic_section']
    key_dynamic = option_enable_dynamic['option_enable_dynamic']['name']
    value_dynamic = CONF[key_dynamic]
    for section_dynamic in value_dynamic:
        for value in old_dynamic_section:
            old_key = value['name']
            try:
                old_value = load.get_value_from_option_in_file(OPTION_IN_FILE,
                                                               section_dynamic,
                                                               old_key)
                new_key = value['replacement_name']
                change_value, template, mapping = \
                    load.get_param_dynamic_section(new_dynamic_section,
                                                   new_key)
            except Exception:
                continue
            if change_value.upper() == 'NONE' and mapping.upper() == 'NONE':
                new_value = old_value
            else:
                if template.upper() != 'NONE':
                    pass
                elif mapping.upper() != 'NONE':
                    mapping_dict = load.string_to_dict(mapping)
                    try:
                        new_value = mapping_dict[old_value]
                    except KeyError:
                        continue

            cru.set_option_file(name_file=path_new_file,
                                section=section_dynamic,
                                key=new_key,
                                value=load.list_to_string(new_value))
            old_key_group = (section_dynamic, old_key, old_value)
            load.delete_option_deprecate(OPTION_IN_FILE,
                                         old_key_group)
