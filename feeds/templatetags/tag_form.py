from django import template
from feeds.forms import *


register = template.Library()


def add_tag_form(parser, token):
    return TagFormNode()


class TagFormNode(template.Node):
    def render(self, context):
        form = TagForm()
        t = template.loader.get_template('feeds/widgets/tag_popup.html')
        return t.render(template.Context({'form': form},
                        autoescape=context.autoescape))

register.tag('tag_form', add_tag_form)
