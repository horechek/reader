from django import template
from django.middleware.csrf import get_token
from feeds.forms import *
from feeds.models import *


register = template.Library()


def add_feed_form(parser, token):
    try:
        tag_name, feed = token.split_contents()
        return FeedFormNode(feed)
    except ValueError:
        return FeedFormNode()


class FeedFormNode(template.Node):
    def __init__(self, feed=False):
        self.feed = False
        if feed:
            self.feed = template.Variable(feed)

    def render(self, context):
        if not self.feed:
            form = FeedForm()
            t = template.loader.get_template('feeds/widgets/feed_popup.html')
            action = '/feeds/add/'
        else:
            feed = self.feed.resolve(context)
            # feed = Feed.objects.get(id=feed_id)
            form = FeedForm(instance=feed)
            t = template.loader.get_template('feeds/feed_form.html')
            action = '/feeds/edit/'+str(feed.id)+'/'
        csrf_token = str(get_token(context['request']))
        return t.render(template.Context({'form': form, 'csrf_token': csrf_token, 'action': action},
                        autoescape=context.autoescape))

register.tag('feed_form', add_feed_form)
