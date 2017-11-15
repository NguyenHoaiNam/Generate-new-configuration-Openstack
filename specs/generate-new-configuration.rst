..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

===========================================
Configuration change handling over releases
===========================================

OpenStack users would like to have a mechanism to handle configuration changes
over release cycles (deprecation, removed..). This spec outlines this mechanism.

Problem description:
====================

When users perform upgrade their OpenStack system to new release, normally
they are required to update configuration files for adapting changes from
old release to new release. Basically, at that time they must read release
notes or change logs or even track source code changes for doing this.
But unfortunately, there could be some misunderstanding, lack of information
in release notes that cause users confuse. There should be some helper in
oslo.config for automatically adopt new changes and help users manage their
configuration files easily.

Scenario:
=========

Below is the proposed workflow that users can perform on old system to generate
new configuration for preparing upgrading to new release::

                                +--------------+
    Old configuration  +-------->              |
                                |              |
                                |  Gen config  +-------> New configuration
          Mapping-file +-------->              |
                                |              |
                                +--------------+

                          Running on old environment

Proposed change:
================
There are some problems that need to be achieved for this feature.

Problem 1: How to get old values from old config file via ``oslo.config``?
--------------------------------------------------------------------------

We had a method to generate sample configuration file for any projects, so
we could base on this method to get a ConfigOpts instance (CONF object) with
full list of options from not only main project but also other projects which
are listed in namespace file. Then, we can get old config values in config file
with right format via CONF object.

One more important thing that there is a dynamic section. For example, Cinder
has a dynamic section named ``enabled_backends`` [1]_, if this option is
declared like  ``enabled_backends = lvmdriver-1``, then there will be a section
declared in cinder.conf like below.

.. code-block:: ini

  [lvmdriver-1]
  image_volume_cache_enabled = True
  volume_clear = zero
  lvm_type = default
  iscsi_helper = tgtadm
  volume_group = stack-volumes-lvmdriver-1
  volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
  volume_backend_name = lvmdriver-1


So how can we understand all values in dynamic section? A new feature in
oslo.config should be developed that support projects define dynamic
sections in the same way. After that, we can read values of dymanic sections
like the way that we are trying to do with Cinder dymanic section[2]_.

Problem 2: How to map/convert old values into new configuration file?
---------------------------------------------------------------------

* *Question 1*: Were all configuration changes described in codebase?

* *Question 2*: How many ways did developers use for configuration changes? 
  Does `oslo.config` support for all of changes that mean we can define all 
  of them in codebase?

Here is answers:

* *Answer 1*: Not all configuration option changes were defined in codebase
  or even never showed up in release notes.

* *Answer 2*: ``oslo.config`` does not support us to define some configuration 
  changes in somecase following:

  - Mapping multi config values into one new values.
  - The value of an option should be changed as a compatible with new source
    code.

So that we solve this problem then there must be config-mapping file for
each projects to explain all necessary information as this demo file [3]_.

When an option is changed in new release there it will be declared
as following:

.. code-block:: python

  cfg.StrOpt('new_option',
            help='This is a new option which is to replace with old_option',
            deprecated_name='old_option',
            deprecated_group='section')

In case we want to convert this new option in configuration file from
old config (eg: 'old_config = abc' --> 'new_config = def') then the above
lines of code are not enough for us to do this. As mention, we need to have
config-mapping file to explain more detail about this.

For example:

This config-mapping file is to declare ``transport_url``:

.. code-block:: yaml

  deprecated_options:
    oslo_messaging_rabbit:             <Old section in Old config file>
    - name: rabbit_host                <Old key name in Old config file>
      replacement_group: DEFAULT       <New section>
      replacement_name: transport_url  <New key name>

  new_options:
    DEFAULT:                           <New section in New config file>
    - name: transport_url              <New key name in NEW config file>
      value: rabbit_userid, rabbit_password, rabbit_host, rabbit_port
                          List of all keys whose values will be added to template>
      template: rabbit://{}:{}@{}:{}   <A template of the values in new config options>
      mapping: None                    <Old value maps to new value>


But it is not suitable to mantain the files manually, there must be a mechanism
to do the files automatically, so in order to do this we need to implement 
three more attributes for each option:

- values: list of values will be put to templates.

- template: using an simple template format to render new value from a list of
  old value.

- mapping: in case of the value of an option is changed, we need to convert old
  value to new value.
  
  For example: At newton release, we need to declare like this in neutron.conf:

  ``core_plugin = neutron.plugins.ml2.plugin.Ml2Plugin``
  **BUT** it was changed at Pike: ``core_plugin = ml2``

With three new things, all of projects can define almost of change cases of
config options and operators will generate mapping file by **oslo.config**.

Work Items:
===========

1. Implement a method to get values from configuration file.
 
  - Support to register dynamic section with oslo.config
  - Implement on each project to support oslo.config get dynamic section

2. Develop three new attributes: values, template and mapping.

3. Implement a new function to render config-mapping file from codebase.

4. Implement a mechanism to generate new configuration based on
   config-mapping file and old configuration. For example [4]_.

Documentation Impact:
=====================

We need to add a documentation to explain config-mapping file and how to
create this file.

Tool Impact:
============

It is necessary to have an utility to generate previous configuration changes
to config-mapping file. After that developers will maintain the files
manually, whenever there is a configuration change then the files must be
updated.

Test Impact:
============

There must be a method to validate the syntax of config-mapping file.

Implementation:
===============

Assignee(s)
-----------

Primary assignee:

  Dai Dang Van <daidv@vn.fujitsu.com>

  Nam Nguyen Hoai <namnh@vn.fujitsu.com>

  Hieu Le <hieulq@vn.fujitsu.com>

References:
===========

.. [1] https://github.com/openstack/cinder/blob/66b3a52794f9c2aa6652b28c0a8e67792e2f993b/cinder/common/config.py#L160

.. [2] https://github.com/NguyenHoaiNam/Jump-Over-Release/blob/spec/jor/getconf/dynamic_section/cinder.py

.. [3] https://github.com/NguyenHoaiNam/Jump-Over-Release/blob/spec/jor/templates/ocata/oslo_messaging.yaml
       https://github.com/NguyenHoaiNam/Jump-Over-Release/blob/spec/jor/templates/ocata/cinder.yaml 

.. [4] https://github.com/NguyenHoaiNam/Jump-Over-Release/blob/master/jor/mapconf/gen_conf.py#L14-L157 
