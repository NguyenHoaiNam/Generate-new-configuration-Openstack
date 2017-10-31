[![Build Status](https://travis-ci.org/NguyenHoaiNam/Jump-Over-Release.svg?branch=master)](https://travis-ci.org/NguyenHoaiNam/Jump-Over-Release)
# Generate-new-configuration-Openstack
This project is to generate new configuration automatically for Openstack new release

### How to install

Step 1: Clone this project

```
git clone https://github.com/NguyenHoaiNam/Jump-Over-Release.git
```

Step 2: Install packages dependency

```
cd Jump-Over-Release
sudo -E pip install -r requirements.txt
```

Step 3: Generate config

*TODO*: We will update fully this step after finishing this project.
```
python run.py --namespace-file /opt/stack/barbican/etc/oslo-config-generator/barbican.conf --old-config-file /etc/barbican/barbican.conf --new-config-file barbican.conf
```


### Scope of this project

#### Solved:

- Config mapping 1:1: Change section, key, value.
- Config mapping n:1. From some old options to a new options with a template.
- Dynamic section: It can solve the change of option in dynamic section for Cinder.

#### Don't still solve:
- All options that were removed anymore.


### Our plan

#### Phase 1:
- Creating Poc code: Done
- Config mapping 1:1 and n:1: Done

#### Phase 2: Doing
- Dynamic section in case of Cinder: Done
- Dynamic section in case of Neutron: Done
- Creating yaml file for Keystone, Glance, Neutron, Cinder, Nova.

#### Phase 3: Pending
- Using this project generate a new config at Ocata from Mitaka then creating a tool is to upgrade Openstack from Mitaka to Ocata automatically including Keystone, Glance, Nova, Neutron, Cinder.
This tool will use all config file from this project.

