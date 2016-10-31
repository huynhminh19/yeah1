import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
YOUTUBE_ANALYTICS_API_VERSION = "v1"


def get_channel_id(youtube):
	channels_list_response = youtube.channels().list(
		mine=True,
		part="id"
	).execute()
	return channels_list_response["items"][0]["id"]

def run_analytics_report(youtube_analytics, channel_id, options):
	# Call the Analytics API to retrieve a report. For a list of available
	# reports, see:
	# https://developers.google.com/youtube/analytics/v1/channel_reports
	analytics_query_response = youtube_analytics.reports().query(
		ids="channel==%s" % channel_id,
		metrics=options["metrics"],
		dimensions=options["dimensions"],
		start_date=options["start_date"],
		end_date=options["end_date"],
		max_results=options["max_results"],
		sort=options["sort"]
	).execute()

	print "Analytics Data for Channel %s" % channel_id

	return {"header": analytics_query_response.get("columnHeaders", []), "rows": analytics_query_response.get("rows", [])}


def retrieve_top10_videos_by_view_count(options, http):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=http)
	youtube_analytics = build(YOUTUBE_ANALYTICS_API_SERVICE_NAME, YOUTUBE_ANALYTICS_API_VERSION, http=http)
	try:
		channel_id = get_channel_id(youtube)
		return run_analytics_report(youtube_analytics, channel_id, options)
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


