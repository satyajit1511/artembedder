# ArtEmbedder 🎵

**ArtEmbedder** is a modern, cross-platform desktop application designed to easily find and embed high-resolution album artwork into your music collection. Built with Python and PyQt5, it supports batch processing, automatic metadata matching, and integration with both **iTunes** and **MusicBrainz** APIs.

![ArtEmbedder Icon](assets/music.png)

## ✨ Features

*   **High-Quality Artwork**: Automatically fetches images up to **1000x1000px** (or higher) from iTunes or Cover Art Archive (MusicBrainz).
*   **Format Support**: Native embedding for **MP3 (ID3)**, **FLAC (Vorbis)**, and **M4A/AAC (MP4 Atoms)**.
*   **Batch Processing**: Drag and drop entire folders. The "⚡ Auto-Match" feature groups files by album and processes thousands of tracks in the background.
*   **Dual API Support**: Choose between **iTunes** (faster, mainstream) or **MusicBrainz** (open data, precise releases) for sourcing artwork.
*   **Modern UI**:
    *   **Dark Mode** / Light Mode toggle.
    *   Responsive layout with drag-and-drop support.
    *   Integrated preview pane to see current and new artwork.
    *   Detailed progress logging.
*   **Cross-Platform**: Runs on Windows, Linux, and macOS.

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.8 or higher.
*   `pip` (Python package manager).

### 1. Clone the Repository
```bash
git clone https://github.com/HARAJIT05/ArtEmbedder.git
cd ArtEmbedder
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application

**Windows:**
```bash
python main.py
```

**Linux / macOS:**
```bash
chmod +x app.sh
./app.sh
```

## 📦 Building a Standalone Executable

You can package ArtEmbedder into a single `.exe` file using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable (Windows)
python -m PyInstaller --noconsole --onefile --icon=assets/music.png --name "ArtEmbedder" --add-data "assets;assets" main.py
```
*The executable will be generated in the `dist/` folder.*

## 🛠 Usage Guide

1.  **Import Music**:
    *   Click **Open Folder** or drag-and-drop files/folders into the left panel.
    *   Use **Select All** to manage the list.
2.  **Get Artwork**:
    *   **Manual**: Select a file, type "Artist - Album" in the search bar, and select a source (iTunes/MusicBrainz). Click a result to preview.
    *   **Automatic**: Click **⚡ Auto-Match & Embed All**. The app will group files by album, search automatically, and apply the best match.
3.  **Embed**:
    *   Click **Embed Selected Image** to write the artwork to the file tags.
    *   Double-click any file in the list to view its current embedded metadata.

## 🤝 Credits

*   **Developer**: [HARAJIT05](https://github.com/HARAJIT05)
*   **GUI Framework**: [PyQt5](https://riverbankcomputing.com/software/pyqt/)
*   **Audio Metadata**: [Mutagen](https://mutagen.readthedocs.io/)
*   **Network**: [Requests](https://requests.readthedocs.io/)
*   **APIs**:
    *   [Apple iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html)
    *   [MusicBrainz & Cover Art Archive](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2)
*   **Icons**: Material Design Icons & GitHub Logos.

## 📄 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 HARAJIT05

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
