import streamlit as st
from googleapiclient.discovery import build
import requests as r
mediawiki_api_url = "https://en.wikipedia.org/w/api.php"


st.image("redfavmusic.png")
st.text("")
st.header("Search info, about your favourite artist")
def fetchdata(artist_name):
  params = {
    "action": "query",
    "format": "json",
    "prop": "extracts|images",
    "exintro": "",
    "explaintext": "",
    "redirects": 1,
    "titles": artist_name
    }
  response = r.get(mediawiki_api_url, params=params)
  if response.status_code == 200:
         data = response.json()
         return data
  else:
         return None



st.write("")
st.write("")
#this code is for search bar
searchbar = st.text_input("Search:", value="")

#this code is for running the next step

if st.button("Search"):
  artist_data = fetchdata(searchbar)
  if artist_data:
        page_id = next(iter(artist_data["query"]["pages"].values())).get("pageid")
        title = next(iter(artist_data["query"]["pages"].values())).get("title")
        extract = next(iter(artist_data["query"]["pages"].values())).get("extract")
        thumbnail = None
        info_box_style = """<style>.info-box { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; }</style>"""

        st.write(f"Artist: {title}")
       
  if thumbnail:
        st.write(thumbnail)
  if extract:
        st.write(info_box_style, unsafe_allow_html=True)
        st.write(f"<div class='info-box'>", unsafe_allow_html=True)
        st.write(extract)
  else:
        st.write("Artist not found ")
        st.write("</div>", unsafe_allow_html=True)
else:
      st.write("Click 'Search' to find artist information ")


# Replace "YOUR_API_KEY" with your actual YouTube Data API v3 key
API_KEY = "YOUR_API_KEY"

def get_youtube_search_results(search_query):
  youtube = build("youtube", "v3", developerKey=API_KEY)

  # Search request parameters
  request = youtube.search().list(
      part="snippet",
      q=search_query,
      maxResults=10  # Adjust the number of results to return
  )
  response = request.execute()

  # Extract video information from search results
  videos = []
  for item in response["items"]:
    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]
    description = item["snippet"]["description"]
    thumbnail_url = item["snippet"]["thumbnails"]["default"]["url"]
    videos.append({"video_id": video_id, "title": title, "description": description, "thumbnail_url": thumbnail_url})

  return videos

st.header("For songs enter!")

search_query=""
if st.button("enter"):
  if searchbar != "":
    search_query = f"{searchbar} songs"
  else:
    st.error("enter artist name in search bar")

if search_query:
  # Call function to get search results
  video_data = get_youtube_search_results(search_query)

  if video_data:
    st.subheader("Search Results:")
    for video in video_data:
      st.write(f"*Title:* {video['title']}")
      st.write(f"*Description:* {video['description']}")
      st.image(video["thumbnail_url"], width=200)
      st.write(f"[Watch on YouTube](https://www.youtube.com/watch?v={video['video_id']})")  # Link to video
  else:
    st.write("No search results found for this term.")
