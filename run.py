# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

from jor.getconf import oldconf
from jor.mapconf import gen_conf
from jor import utils


if __name__ == '__main__':
    CONF, namespaces = oldconf.get_conf()
    path_new_config = utils.get_root_path('newconf', 'cinder.conf')
    gen_conf.mapping_config(path_new_config, CONF, namespaces)
    gen_conf.add_options_ne_default(path_new_config, CONF)
