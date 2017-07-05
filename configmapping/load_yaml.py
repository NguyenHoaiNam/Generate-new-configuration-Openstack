# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

import yaml


def load_yaml(name_file):
    f = open(name_file)
    content_dict = yaml.safe_load(f)
    f.close()
    return content_dict


a = load_yaml('/home/stack/my_git/'
              'Generate-new-configuration-Openstack/'
              'templates/oslo_messaging.yaml')

print a
