from django.shortcuts import render,redirect
from django.conf import settings
import requests
import json
from isodate import parse_duration

def index(request):
	if request.method == 'POST':
		query = request.POST.get('search')
		search_url = 'https://www.googleapis.com/youtube/v3/search'
		video_url = 'https://www.googleapis.com/youtube/v3/videos'
		search_parms ={
			'key':settings.YOUTUBE_DATA_API_KEY,
			'q': query,
			'part':'snippet',
			'maxResults':9,
			'type':'video'
		}
		viedo_id = []
		r = requests.get(search_url,params=search_parms)
		
		results = r.json()['items']
		for result in results:
			viedo_id.append(result['id']['videoId'])

		if request.POST['submit'] == 'lucky':
			return redirect(f'https://www.youtube.com/watch?v={video_id[0]}')
		

		viedo_params = {
			'key':settings.YOUTUBE_DATA_API_KEY,
			'part':'snippet,contentDetails',
			'id': ','.join(viedo_id)

		}
		re = requests.get(video_url,params=viedo_params)
		# print(re.text)

		results = re.json()['items']
		video = []
		for result in results:
			# print(result['id'])
			# print(result['snippet']['title'])
			# print(result['snippet']['thumbnails']['high']['url'])
			# print(parse_duration(result['contentDetails']['duration']).total_seconds())

			video_detaile ={
				'id':result['id'],
				'url':f'https://www.youtube.com/watch?v={result["id"]}',
				'title':result['snippet']['title'],
				'thumbnail':result['snippet']['thumbnails']['high']['url'],
				'duration':int(parse_duration(result['contentDetails']['duration']).total_seconds())
			}
			video.append(video_detaile)

		context = {
			'videos':video
		}
		return render(request,'search/index.html',context)
	return render(request,'search/index.html')
