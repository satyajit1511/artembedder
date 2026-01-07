import requests
import re

class ITunesAPI:
    BASE_URL = "https://itunes.apple.com/search"

    @staticmethod
    def search_artwork(term: str, entity: str = "album", limit: int = 5):
        """
        Searches iTunes for the given term and returns a list of results
        with high-resolution artwork URLs.
        """
        params = {
            "term": term,
            "entity": entity,
            "limit": limit,
            "media": "music"
        }
        
        try:
            response = requests.get(ITunesAPI.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("results", []):
                artwork_url = item.get("artworkUrl100")
                if artwork_url:
                    # Upgrade resolution to 1000x1000
                    high_res_url = ITunesAPI._upgrade_resolution(artwork_url)
                    
                    result_item = {
                        "artist": item.get("artistName"),
                        "album": item.get("collectionName"),
                        "track": item.get("trackName"), # Might be None if searching for albums
                        "artwork_url": high_res_url,
                        "thumbnail_url": artwork_url,
                        "year": item.get("releaseDate", "")[:4]
                    }
                    results.append(result_item)
            return results
            
        except requests.RequestException as e:
            print(f"Error querying iTunes API: {e}")
            return []

    @staticmethod
    def _upgrade_resolution(url: str) -> str:
        """
        Replaces the resolution part of the iTunes image URL to request a larger image.
        """
        # iTunes URLs typically look like: .../100x100bb.jpg
        # We want to change 100x100bb to 1000x1000bb
        return re.sub(r'/\d+x\d+[a-z]*\.([a-z]+)', r'/1000x1000bb.\1', url)

    @staticmethod
    def download_image(url: str) -> bytes:
        """
        Downloads the image bytes from the given URL.
        """
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None
