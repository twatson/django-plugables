# Administration
import admin

# Core Template Tags
from django import template
template.add_to_builtins('django.contrib.markup.templatetags.markup')
template.add_to_builtins('django.contrib.humanize.templatetags.humanize')
template.add_to_builtins('django.templatetags.cache')

# 3rd Party Template Tags
template.add_to_builtins('applications.typogrify.templatetags.typogrify')
template.add_to_builtins('applications.template_utils.templatetags.comparison')
template.add_to_builtins('applications.template_utils.templatetags.feeds')
template.add_to_builtins('applications.template_utils.templatetags.generic_content')
template.add_to_builtins('applications.template_utils.templatetags.generic_markup')