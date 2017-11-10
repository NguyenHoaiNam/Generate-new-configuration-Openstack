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
a new configuration for new release, so it takes a lot of time and makes users difficult sometime.

Scenario:
=========

Imagine, this feature is implemented to oslo.conf. Users can run this feature on old release to generate
new configuration for new release and the configuration will be able to use for new enviroment.

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
Currently, there are two solutions for this feature.

Solution 1: Using mapping-file
---------------------------

In order to have this feature, we need to solve some problems as following:

1. ConfigOpts instance



2. Mapping-file
We need a file to declare deprecated options and new options. Currently in source-code, there are two options
to do this such as 


Solution 2: Adding new information for new options in source-code
-----------------------------------------------------------------




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
