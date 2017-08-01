[![Build Status](https://travis-ci.org/NguyenHoaiNam/Jump-Over-Release.svg?branch=master)](https://travis-ci.org/NguyenHoaiNam/Jump-Over-Release)
# Generate-new-configuration-Openstack
This project is to generate new configuration for Openstack new release

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

*TODO*(namnh, daidv): We will update this step after finishing this project.


### Scope of this project

#### Solved:

- Config mapping 1:1: Change section, key, value.
- Config mapping n:1. From some old options to a new options with a template.
- Dynamic section: It can solve the change of option in dynamic section for Cinder.

#### Don't still solve:
- Change config with Neutron. Because Neutron can read all ini config-file from neutron.conf.
- All option that were removed anymore.