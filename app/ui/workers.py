from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
from app.core.itunes import ITunesAPI
from app.core.musicbrainz import MusicBrainzAPI
from app.core.metadata import MetadataEngine
import traceback
import sys

class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    log = pyqtSignal(str)


class SearchWorker(QRunnable):
    def __init__(self, term, source="iTunes"):
        super(SearchWorker, self).__init__()
        self.term = term
        self.source = source
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            if self.source == "MusicBrainz":
                results = MusicBrainzAPI.search_artwork(self.term)
            else:
                results = ITunesAPI.search_artwork(self.term)
            self.signals.result.emit(results)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()


class DownloadWorker(QRunnable):
    def __init__(self, url):
        super(DownloadWorker, self).__init__()
        self.url = url
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            # Re-use iTunes downloader or generic requests
            # Both APIs return a URL, so ITunesAPI.download_image (which uses requests) works for both
            data = ITunesAPI.download_image(self.url)
            if data:
                self.signals.result.emit(data)
            else:
                raise Exception("Failed to download image")
        except Exception:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()


class AutoEmbedWorker(QRunnable):
    def __init__(self, files, source="iTunes"):
        super(AutoEmbedWorker, self).__init__()
        self.files = files
        self.source = source
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        total_files = len(self.files)
        processed_count = 0
        
        # 1. Group files by Album/Artist to minimize API calls
        album_groups = {}
        self.signals.log.emit(f"Scanning {total_files} files for metadata...")
        
        for f in self.files:
            meta = MetadataEngine.get_metadata(f)
            if meta and meta['artist'] and meta['album']:
                key = (meta['artist'], meta['album'])
                if key not in album_groups:
                    album_groups[key] = []
                album_groups[key].append(f)
            else:
                self.signals.log.emit(f"Skipping {f} - Missing Artist/Album tags.")
                processed_count += 1
                self.signals.progress.emit(int((processed_count / total_files) * 100))

        # 2. Process each album
        total_albums = len(album_groups)
        current_album_idx = 0
        
        for (artist, album), file_list in album_groups.items():
            current_album_idx += 1
            query = f"{artist} - {album}" # Changed to dash format for better compatibility with search heuristics
            self.signals.log.emit(f"[{current_album_idx}/{total_albums}] Searching ({self.source}): {query}")
            
            try:
                # Search API
                if self.source == "MusicBrainz":
                    results = MusicBrainzAPI.search_artwork(query, limit=1)
                else:
                    results = ITunesAPI.search_artwork(query, limit=1)
                
                if results:
                    high_res_url = results[0]['artwork_url']
                    self.signals.log.emit(f"  Found artwork. Downloading...")
                    image_data = ITunesAPI.download_image(high_res_url)
                    
                    if image_data:
                        self.signals.log.emit(f"  Embedding into {len(file_list)} files...")
                        for f in file_list:
                            try:
                                MetadataEngine.embed_artwork(f, image_data)
                            except Exception as e:
                                self.signals.log.emit(f"  Failed to embed {f}: {e}")
                            finally:
                                processed_count += 1
                                self.signals.progress.emit(int((processed_count / total_files) * 100))
                    else:
                        self.signals.log.emit(f"  Failed to download image for {query}")
                        processed_count += len(file_list)
                else:
                    self.signals.log.emit(f"  No artwork found for {query}")
                    processed_count += len(file_list)
                    
                self.signals.progress.emit(int((processed_count / total_files) * 100))
                
            except Exception as e:
                self.signals.log.emit(f"  Error processing album {query}: {e}")
                processed_count += len(file_list)
                self.signals.progress.emit(int((processed_count / total_files) * 100))

        self.signals.result.emit("All Album Art Embedded Sucessfully.")
        self.signals.finished.emit()


class EmbedWorker(QRunnable):
    def __init__(self, files, image_data):
        super(EmbedWorker, self).__init__()
        self.files = files
        self.image_data = image_data
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        total = len(self.files)
        success_count = 0
        
        try:
            for i, file_path in enumerate(self.files):
                try:
                    self.signals.log.emit(f"Processing: {file_path}")
                    MetadataEngine.embed_artwork(file_path, self.image_data)
                    success_count += 1
                except Exception as e:
                    self.signals.log.emit(f"Error on {file_path}: {str(e)}")
                
                # Report progress
                progress_pct = int(((i + 1) / total) * 100)
                self.signals.progress.emit(progress_pct)
            
            self.signals.result.emit(f"Completed. Successfully embedded {success_count}/{total} files.")

        except Exception:
            import sys
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()
