# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor.getconf import oldconf
from jor.configmapping import create_new_config


if __name__ == '__main__':
    CONF = oldconf.get_conf()
    # create_new_config.make_global_option('barbican')
    create_new_config.change_old_config_to_new(create_new_config.NAME_NEW_FILE,
                                               CONF, ['barbican'])
    create_new_config.move_option_changed(create_new_config.NAME_NEW_FILE,
                                          CONF)
