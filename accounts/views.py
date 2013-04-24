from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson


def set_show(request, show_unread):
    profile = request.user.get_profile()
    profile.showUnread = int(show_unread)
    profile.save()
    result = {
        'success' : True,
        'showUnread' : show_unread
    }
    return HttpResponse(simplejson.dumps(result))