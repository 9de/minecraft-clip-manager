# Minecraft Clip Manager

An automated tool for processing, trimming, and sharing Minecraft gameplay recordings. This utility watches specified directories for new video files and provides quick options for trimming, renaming, and uploading clips to Streamable.

## Features

- 🎮 Automatic detection of new gameplay recordings
- ✂️ Quick 15-second clip trimming from the end of videos
- 📝 Custom video trimming with flexible start/end times
- 📤 Direct upload to Streamable
- 📁 Automatic organization into dedicated folders
- 🔄 Batch processing capabilities
- 🎯 Multiple directory monitoring

## Requirements

- Python 3.6+
- Required Python packages:
  - watchdog
  - moviepy
  - requests
  - pathlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/minecraft-clip-manager.git
cd minecraft-clip-manager
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure the settings in the script:
```python
WATCH_PATHS = [
    r"C:\Users\YourUsername\Videos\Minecraft",
]
DESTINATION_PATH = r"PATH_TO_YOUR_BLOCKS_MC_FOLDER"
STREAMABLE_EMAIL = "YOUR_EMAIL"
STREAMABLE_PASSWORD = "YOUR_PASSWORD"
```

## Usage

Run the script:
```bash
python clip_manager.py
```

### Available Options

0. Quick Clip last 15s to folder
1. Save clip with new name
2. Save clip to BlocksMC folder
3. Share clip on Streamable (with trim options)
4. Quick upload last 15s to Streamable
5. Skip this clip
6. Open folders
7. Play video
9909. Remove clip

## Features in Detail

### Quick Clip (Option 0)
- Automatically trims the last 15 seconds of a video
- Saves to your specified BlocksMC folder
- Adds "+cuttedauto" suffix to filename

### Custom Trimming (Option 3)
- Choose between keeping last N seconds or custom start/end times
- Preview video duration before trimming
- Optional custom naming for trimmed clips

### Streamable Integration
- Direct upload to Streamable
- Automatic shortcode generation
- Returns shareable link upon successful upload

### File Management
- Automatic file organization
- Built-in file explorer integration
- Batch processing capabilities

## Configuration

Update the following variables in the script:

```python
WATCH_PATHS = [
    r"C:\Users\YourUsername\Videos\Minecraft",  # Add more paths as needed
]
DESTINATION_PATH = r"PATH"
STREAMABLE_EMAIL = "YOUR_EMAIL"
STREAMABLE_PASSWORD = "YOUR_PASSWORD"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using the watchdog library for file system monitoring
- Uses moviepy for video processing
- Integrates with Streamable's API for sharing
