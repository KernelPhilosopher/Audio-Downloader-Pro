# 🎵 Audio Downloader Pro

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-important)](https://ffmpeg.org/)

A professional YouTube audio downloading application developed with Python using the MVC architecture.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Requirements](#-technical-requirements)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Legal Considerations](#-legal-considerations)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🌟 Features

- ✅ **Batch Processing**: Download multiple audio files simultaneously
- 🎨 **Modern UI**: Clean interface with dark mode support
- 🔄 **Real-time Updates**: Live progress tracking
- 🛡️ **System Verification**: Automatic dependency and requirement checks
- 📋 **Activity Logging**: Detailed download history
- ⚙️ **Customizable Output**: Multiple audio format options:
  - MP3 (192/320 kbps)
  - WAV (Lossless)
  - M4A (AAC)
  - OGG (Vorbis)

## 📥 Installation

### Windows Executable

1. **Install FFmpeg** (required):
   - [Official installation guide](https://ffmpeg.org/download.html)
   - [Video tutorial](https://youtu.be/JR36oH35Fgg)
2. Download the latest release from the [Releases Section](https://github.com/KernelPhilosopher/Audio-Downloader-Pro/tree/main/YT_Audio_Downloader/dist)

3. Run `YT_Audio_Downloader.exe`

### From Source Code

```bash
# Clone repository
git clone https://github.com/KernelPhilosopher/Audio-Downloader-Pro.git

# Navigate to project directory
cd YT_Audio_Downloader

# Install dependencies
pip install -r requirements.txt

# Launch application
python -m YT_Audio_Downloader.src.main
```

## 📚 Technical Requirements

- **Python**: 3.9 or newer
- **FFmpeg**: v5.0+ (external dependency)
- **Required Libraries**:
  ```
  yt-dlp>=2023.12.30
  customtkinter>=5.2.1
  Pillow>=10.1.0
  ffmpeg-python>=0.2.0
  ```

## 🏗️ Project Structure

```
YT_Audio_Downloader/
├── src/
│   ├── controllers/    # Business logic and application flow
│   ├── models/         # Download management and data handling
│   ├── views/          # GUI components and layouts
│   ├── utils/          # Helper functions and themes
│   └── services/       # External services
├── dist/               # Compiled executable file
```

## 🚀 Usage Guide

1. **Enter YouTube URLs** (one per line)
2. **Select output format** and quality settings
3. **Choose destination folder** for downloaded files
4. **Accept legal terms** regarding content usage
5. **Start download process**
6. **Monitor progress** with the real-time tracking system

## ⚠️ Legal Considerations

This software is intended for educational purposes only. Please only download content that:

- Is in the public domain
- Has a Creative Commons license
- You have explicit permission to download
- You own the copyright for

The developer assumes no responsibility for improper use of this application.

## 🛠️ Troubleshooting

If you encounter any issues:

1. **Verify FFmpeg installation**:

   ```bash
   ffmpeg -version
   ```

2. **Check for Python updates**:

   ```bash
   python --version
   ```

3. **Common solutions**:
   - Ensure you have a stable internet connection
   - Try downloading a single file at a time
   - Temporarily disable antivirus software
   - Check for firewall blocking

## 📞 Support

**Developer Contact**:  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black)](https://github.com/KernelPhilosopher)  
✉️ kernelphilosopher@outlook.com

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Made with ❤️ by Kernel Philosopher
