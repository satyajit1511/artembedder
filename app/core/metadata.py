import os
import mimetypes
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error as ID3Error
from mutagen.flac import FLAC, Picture
from mutagen.mp4 import MP4, MP4Cover
from mutagen.easymp4 import EasyMP4

class MetadataEngine:
    
    @staticmethod
    def get_metadata(file_path: str):
        """
        Extracts 'Artist' and 'Album' metadata from the file.
        Returns a dict: {'artist': str, 'album': str} or None if failed.
        """
        details = MetadataEngine.get_details(file_path)
        if details:
            return {"artist": details.get("artist"), "album": details.get("album")}
        return None

    @staticmethod
    def get_details(file_path: str):
        """
        Extracts comprehensive metadata including Artwork.
        Returns: {'title': str, 'artist': str, 'album': str, 'artwork': bytes|None}
        """
        if not os.path.exists(file_path):
            return None

        ext = os.path.splitext(file_path)[1].lower()
        data = {'title': 'Unknown', 'artist': 'Unknown', 'album': 'Unknown', 'artwork': None}
        
        try:
            if ext == ".mp3":
                audio = MP3(file_path, ID3=ID3)
                if audio.tags:
                    data['artist'] = str(audio.tags.get("TPE1", "Unknown"))
                    data['album'] = str(audio.tags.get("TALB", "Unknown"))
                    data['title'] = str(audio.tags.get("TIT2", "Unknown"))
                    # Extract APIC (Cover)
                    apic_frames = audio.tags.getall("APIC")
                    if apic_frames:
                        data['artwork'] = apic_frames[0].data
            
            elif ext == ".flac":
                audio = FLAC(file_path)
                data['artist'] = audio.get("artist", ["Unknown"])[0]
                data['album'] = audio.get("album", ["Unknown"])[0]
                data['title'] = audio.get("title", ["Unknown"])[0]
                if audio.pictures:
                    data['artwork'] = audio.pictures[0].data
            
            elif ext in [".m4a", ".mp4", ".aac"]:
                audio = MP4(file_path)
                data['artist'] = audio.tags.get("©ART", ["Unknown"])[0]
                data['album'] = audio.tags.get("©alb", ["Unknown"])[0]
                data['title'] = audio.tags.get("©nam", ["Unknown"])[0]
                covers = audio.tags.get("covr")
                if covers:
                    data['artwork'] = bytes(covers[0])

            return data
        except Exception as e:
            print(f"Error extracting details from {file_path}: {e}")
            return None

    @staticmethod
    def embed_artwork(file_path: str, image_data: bytes, mime_type: str = "image/jpeg"):
        """
        Embeds the provided image data into the audio file at file_path.
        Supports MP3, FLAC, and M4A/MP4.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == ".mp3":
                MetadataEngine._embed_mp3(file_path, image_data, mime_type)
            elif ext == ".flac":
                MetadataEngine._embed_flac(file_path, image_data, mime_type)
            elif ext in [".m4a", ".mp4", ".aac"]:
                MetadataEngine._embed_m4a(file_path, image_data)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            return True
        except Exception as e:
            print(f"Failed to embed artwork for {file_path}: {e}")
            raise e

    @staticmethod
    def _embed_mp3(path, image_data, mime_type):
        audio = MP3(path, ID3=ID3)
        # Add ID3 tag if it doesn't exist
        try:
            audio.add_tags()
        except ID3Error:
            pass # Tags likely already exist

        # Remove existing APIC frames (covers) to avoid duplicates
        audio.tags.delall("APIC")

        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime=mime_type,
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=image_data
            )
        )
        audio.save()

    @staticmethod
    def _embed_flac(path, image_data, mime_type):
        audio = FLAC(path)
        
        # Create Picture object
        pic = Picture()
        pic.type = 3 # Cover (front)
        pic.mime = mime_type
        pic.desc = u'Cover'
        pic.data = image_data
        
        # Remove existing pictures
        audio.clear_pictures()
        
        audio.add_picture(pic)
        audio.save()

    @staticmethod
    def _embed_m4a(path, image_data):
        audio = MP4(path)
        
        # MP4Cover format depends on image format
        # Usually checking the first bytes or relying on mime type
        # Simplistic check for PNG vs JPEG
        if image_data.startswith(b'\x89PNG'):
            image_format = MP4Cover.FORMAT_PNG
        else:
            image_format = MP4Cover.FORMAT_JPEG
            
        audio['covr'] = [MP4Cover(image_data, image_format=image_format)]
        audio.save()
