from django import template
from django.middleware.csrf import get_token
from feeds.forms import *
from feeds.models import *


register = template.Library()


def add_tag_form(parser, token):
    try:
        tag_name, tag = token.split_contents()
        return TagFormNode(tag)
    except ValueError:
        return TagFormNode()


class TagFormNode(template.Node):
    def __init__(self, tag=False):
        self.tag = False
        if tag:
            self.tag = template.Variable(tag)

    def render(self, context):
        if not self.tag:
            form = TagForm()
            t = template.loader.get_template('feeds/widgets/tag_popup.html')
            action = '/feeds/add_tag/'
        else:
            tag = self.tag.resolve(context)
            form = TagForm(instance=tag)
            t = template.loader.get_template('feeds/tag_form.html')
            action = '/feeds/edit_tag/'+str(tag.id) + '/'
        csrf_token = str(get_token(context['request']))
        return t.render(template.Context({'form': form, 'csrf_token': csrf_token, 'action': action},
                        autoescape=context.autoescape))

register.tag('tag_form', add_tag_form)
