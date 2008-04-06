# Administration
from tagging import admin

# Template Tags
from django import template
template.add_to_builtins('tagging.templatetags.tagging_tags')
