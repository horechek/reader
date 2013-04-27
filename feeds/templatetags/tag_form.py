from django import template
from django.middleware.csrf import get_token
from feeds.forms import *


register = template.Library()


def add_tag_form(parser, token):
    return TagFormNode()


class TagFormNode(template.Node):
    def render(self, context):
        form = TagForm()
        t = template.loader.get_template('feeds/widgets/tag_popup.html')
        csrf_token = str(get_token(context['request']))
        return t.render(template.Context({'form': form, 'csrf_token': csrf_token},
                        autoescape=context.autoescape))

register.tag('tag_form', add_tag_form)
