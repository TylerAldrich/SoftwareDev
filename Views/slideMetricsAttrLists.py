#!/usr/bin/python
# -*- coding: utf-8 -*-

from attributeList import AttributeListsComponent

# Widget for Slide Metrics attributes view
class SlideMetricsAttrListsComponent(AttributeListsComponent):
  guiStateKey = 'slideMetrics'
  attributeType = 'Slide Metrics'
  
  def __init__(self, window, attrs, saved_attrs):
    self.__class__.attr_list = attrs
    self.__class__.saved_attrs = saved_attrs
    AttributeListsComponent.__init__(self, window)
