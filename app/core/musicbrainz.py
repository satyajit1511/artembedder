import requests
import time
from urllib.parse import quote

class MusicBrainzAPI:
    BASE_URL = "https://musicbrainz.org/ws/2"
    CAA_BASE_URL = "https://coverartarchive.org"
    USER_AGENT = "ArtEmbedder/1.0 ( https://github.com/yourusername/artembedder )"
    
    _last_request_time = 0
    _rate_limit_delay = 1.1  # 1 request per second rule

    @classmethod
    def _enforce_rate_limit(cls):
        now = time.time()
        elapsed = now - cls._last_request_time
        if elapsed < cls._rate_limit_delay:
            time.sleep(cls._rate_limit_delay - elapsed)
        cls._last_request_time = time.time()

    @classmethod
    def _get(cls, url, params=None):
        cls._enforce_rate_limit()
        headers = {"User-Agent": cls.USER_AGENT}
        if params:
            # MusicBrainz requires json format specifier often
            if 'fmt' not in params:
                params['fmt'] = 'json'
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            # 503 means rate limit exceeded usually, or server busy
            if response.status_code == 503:
                time.sleep(2)
                response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"MusicBrainz API request failed: {e}")
            return None

    @staticmethod
    def search_artwork(term: str, limit: int = 5):
        """
        Searches MusicBrainz for releases and finds cover art.
        Term is expected to be "Artist - Album" or just "Album".
        """
        # Simple heuristic to split artist/album if possible
        artist = ""
        release = term
        if " - " in term:
            parts = term.split(" - ", 1)
            artist = parts[0]
            release = parts[1]

        # Construct Lucene query
        # query = f'release:"{release}"'
        # if artist:
        #     query += f' AND artist:"{artist}"'
        
        # Using strict query params is safer than constructing lucene string manually sometimes,
        # but the /release endpoint uses 'query' param for lucene search.
        query_parts = []
        if release:
            query_parts.append(f'release:"{release}"')
        if artist:
            query_parts.append(f'artist:"{artist}"')
        
        # Fallback if split failed or simple search wanted
        if not query_parts:
            query_parts.append(f'"{term}"')

        query_str = " AND ".join(query_parts)
        
        params = {
            "query": query_str,
            "limit": limit,
            "fmt": "json"
        }

        data = MusicBrainzAPI._get(f"{MusicBrainzAPI.BASE_URL}/release", params)
        if not data or "releases" not in data:
            return []

        results = []
        for rel in data["releases"]:
            mbid = rel.get("id")
            title = rel.get("title")
            # Artist credit
            artist_credit = "Unknown"
            if "artist-credit" in rel and len(rel["artist-credit"]) > 0:
                artist_credit = rel["artist-credit"][0].get("name", "Unknown")
            
            date = rel.get("date", "")[:4]

            # Check for cover art presence flag
            # Note: The search result might not strictly guarantee artwork exists, 
            # but usually has 'cover-art-archive' key.
            # We must fetch from CAA to get the URL.
            
            # Optimization: Only fetch CAA if 'front' is true in search result (if available)
            # The 'releases' search result usually contains 'cover-art-archive': {'front': True, ...}
            caa_info = rel.get("cover-art-archive", {})
            if caa_info.get("front"):
                image_url = MusicBrainzAPI._get_caa_front_image(mbid)
                if image_url:
                    results.append({
                        "artist": artist_credit,
                        "album": title,
                        "track": None, 
                        "artwork_url": image_url,
                        "thumbnail_url": image_url, # CAA doesn't always give strict thumbnail separate from main
                        "year": date,
                        "source": "MusicBrainz"
                    })
        
        return results

    @staticmethod
    def _get_caa_front_image(mbid):
        """
        Queries Cover Art Archive for the front image URL.
        """
        url = f"{MusicBrainzAPI.CAA_BASE_URL}/release/{mbid}"
        data = MusicBrainzAPI._get(url)
        if data and "images" in data:
            for img in data["images"]:
                if img.get("front"):
                    # Prefer high res 'image' or specific 'thumbnails'
                    # thumbnails keys: '250', '500', '1200', 'small', 'large'
                    # We want high res. 'image' is usually the original upload.
                    return img.get("image")
        return None
