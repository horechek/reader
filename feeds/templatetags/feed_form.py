from django import template
from feeds.forms import *


register = template.Library()


def add_feed_form(parser, token):
    return FeedFormNode()


class FeedFormNode(template.Node):
    def render(self, context):
        form = FeedForm()
        t = template.loader.get_template('feeds/widgets/feed_popup.html')
        return t.render(template.Context({'form': form},
                        autoescape=context.autoescape))

register.tag('feed_form', add_feed_form)
