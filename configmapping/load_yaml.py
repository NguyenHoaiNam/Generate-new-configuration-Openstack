# Author: Nam Nguyen Hoai
# Author: Dai Dang Van

import yaml

import utils


def load_yaml(name_file):
    f = open(name_file)
    content_dict = yaml.safe_load(f)
    f.close()
    return content_dict

if __name__ == '__main__':
    full_path = utils.get_root_path('templates', 'oslo_messaging.yaml')
    a = load_yaml(full_path)
    print a
