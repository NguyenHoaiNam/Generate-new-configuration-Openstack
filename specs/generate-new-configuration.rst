..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================
Generate new configuration
==========================

OpenStack users would like to have a method to generate a new configuration
for new release from old configuration. This spec outlines this method.

Problem description:
===================

When users upgrade their OpenStack system to new release. Users have to update 
a new configuration for new release, so it takes a lot of time and makes users
difficult sometime.

Scenario:
=========

Imagine, this feature is implemented to `oslo.config`. Users can run this
feature on old release to generate new configuration for new release and the
configuration will be able to use for new enviroment.

                               namespace file
                                     +
                                     |
                                     |
                               +-----v--------+
    Old configuration +-------->              |
                               |  Gen config  |
                               |              +-------> New configuration
         Mapping-file +-------->              |
                               +--------------+

                          Running on old environment



Proposed change:
================
Currently, there are some problems which need to be archived for this feature.

Problem 1: How to get old values from old config file via `oslo.config`?
---------------------------

Now, we have a way to generate an sample configuration file for any project, so
we can base on that to get a ConfigOpts instance (CONF object) with full list
of options from not only main project but also other projects which are listed
in namespace file. At this time, we can parsing old config file with our CONF
object that we just archived which mean we can read all of values in config
file with right format.

One more important thing that we should have a way to understand all of values
in dynamic section[1]. This can be solved by defination plugin for each project
that are using dynamic section.

Problem 2: How to map/convert old values into new configuration file?

- Did all configuration changes been described in codebase?
- How many ways did developers use for configuration changes? Does `oslo.config`
support for all of changes that mean we can define all of them in codebase?

And the answers: not all configuration option changes are defined in codebase
or even showed up in release notes. Moreover, `oslo.config` does not support
us to define some configuration changes in somecase following:
- Mapping multi config values into one new values
- The value of an option should be change as a compatible with new source code

Example: #TODO

All of them will be solved by an config mapping file which is automatically
generated from `oslo.config` during filter all of changes indications that are
defined for each option in each project.

To do this, we need to implement three more attributes for each option:
- values: list of values will be put to templates
- templates: an simple template format to defined new value from a list of
old value
- mapping: in case of the value of an option should be change as a compatible
with new source code, we need to convert old value to new value one by one.

With three new things, all of projects can define almost of change cases of
config options and operators will generate mapping file by `oslo.config`.


Implementation
==============

Assignee(s)
----------

Primary assignee:

  Dai Dang Van <daidv@vn.fujitsu.com>

  Nam Nguyen Hoai <namnh@vn.fujitsu.com>

Work Items
==========
None.

[1] What is dynamic section?