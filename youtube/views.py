from django.shortcuts import render
from django.http import HttpResponse

from oauth2client.contrib.django_util import decorators
from datetime import datetime, timedelta
from . import libraries



@decorators.oauth_required
def index(request):
	now = datetime.now()
	one_day_ago = (now - timedelta(days=1)).strftime("%Y-%m-%d")
	one_week_ago = (now - timedelta(days=700)).strftime("%Y-%m-%d")

	options = {}
	options["metrics"]="views,comments,likes,dislikes,estimatedMinutesWatched,averageViewDuration"
	options["dimensions"]="video"
	options["start_date"]=one_week_ago
	options["end_date"]=one_day_ago
	options["max_results"]=10
	options["sort"]="-views"

	top10 = libraries.retrieve_top10_videos_by_view_count(options, request.oauth.http)

	context = {"top10": top10,}
	return render(request, 'youtube/index.html', context)


@decorators.oauth_required
def get_profile_required(request):
    resp, content = request.oauth.http.request('https://www.googleapis.com/plus/v1/people/me')
    return HttpResponse(content)

@decorators.oauth_enabled
def get_profile_optional(request):
    if request.oauth.has_credentials():
        # this could be passed into a view
        # request.oauth.http is also initialized
        return HttpResponse('User email: {}'.format(request.oauth.credentials.id_token['email']))
    else:
        return HttpResponse(
            'Here is an OAuth Authorize link:<a href="{}">Authorize</a>'
            .format(request.oauth.get_authorize_redirect()))

