#!/usr/bin/python
# -*- coding: utf-8 -*-

from attributeList import AttributeListsComponent

# Widget for Slide Metrics attributes view
class SlideMetricsAttrListsComponent(AttributeListsComponent):
  guiStateKey = 'slideMetrics'
  attributeType = 'Slide Metrics'
  ## Mock attributes to use for now
  test_attributes = [
    'Total time tracked',
    'Total time shown',
    'Total tracking lost',
    'Pupil x diameter std dev',
    'Pupil y diameter std dev',
    'Average pupil x diameter'
    ]
  def __init__(self, window, attrs, saved_attrs):
    self.__class__.attr_list = attrs
    self.__class__.saved_attrs = saved_attrs
    AttributeListsComponent.__init__(self, window)
