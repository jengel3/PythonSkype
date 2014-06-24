from util.plugin import event
import re
import json
from util.http import get_url_data


api_video = "https://gdata.youtube.com/feeds/api/videos/{}?v=2&alt=json"


@event(name="youtube_link", regex="youtube\.com/watch\?.*?v=([A-Za-z0-9-_]+)|youtu\.be/([A-Za-z0-9-_]+)")
def youtube_link(chat, message, args, sender, found):
    youtube_match = re.findall("youtube\.com/watch\?.*?v=([A-Za-z0-9-_]+)", message, re.IGNORECASE)
    if not youtube_match:
        youtube_match = re.findall("youtu\.be/([A-Za-z0-9-_]+)", message, re.IGNORECASE)
    if youtube_match:
        for video in youtube_match:
            chat.SendMessage(get_video_info(video))


def get_video_info(video_id):
    final_link = api_video.format(video_id)
    json_data = json.loads(get_url_data(final_link))
    entry = json_data['entry']
    author = entry['author'][0]['name']['$t']
    views = entry['yt$statistics']['viewCount']
    likes = entry['yt$rating']['numLikes']
    dislikes = entry['yt$rating']['numDislikes']
    title = entry['title']['$t']
    final_message = u"{} - by: {} - Views: {} Likes: {} Dislikes: {}".format(title, author, views, likes, dislikes)
    return final_message

