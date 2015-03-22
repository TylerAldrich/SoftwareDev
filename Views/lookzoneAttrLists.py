#!/usr/bin/python
# -*- coding: utf-8 -*-

from attributeList import AttributeListsComponent

# Widget for LookZone Data attributes view
class LookzoneAttrListsComponent(AttributeListsComponent):
  guiStateKey = 'lookzone'
  attributeType = 'LookZone Data'
  ## Mock attributes to use for now
  test_attributes = [
    'LZ attr 1',
    'LZ attr 2',
    'LZ attr 3',
    'LZ attr 4',
    'LZ attr 5',
    'LZ attr 6',
    'LZ attr 7'
    ]
  def __init__(self, window, attrs, saved_attrs):
    self.__class__.attr_list = attrs
    self.__class__.saved_attrs = saved_attrs
    AttributeListsComponent.__init__(self, window)
