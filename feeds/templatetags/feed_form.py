from django import template
from django.middleware.csrf import get_token
from feeds.forms import *


register = template.Library()


def add_feed_form(parser, token):
    return FeedFormNode()


class FeedFormNode(template.Node):
    def render(self, context):
        form = FeedForm()
        t = template.loader.get_template('feeds/widgets/feed_popup.html')
        csrf_token = str(get_token(context['request']))

        return t.render(template.Context({'form': form, 'csrf_token': csrf_token},
                        autoescape=context.autoescape))

register.tag('feed_form', add_feed_form)
