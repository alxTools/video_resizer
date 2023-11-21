# Video Resizer Tool for Topaz Video Ai (post-script)
## for Nvidia GPU's only.
After using a Topaz Video Ai Enhanced Tool, (exported using any high 12-10 bit Prores) the file will size more than 75GB for 3 mins and not playable in any software players due to the format and huge size, so then you will use need this app for resizing/upscaling from *to4k,or 8k 10-bit video with the smallest file size possible and perfect quality so it will be usable for uploading to youtube (they accept 10bit). Resampling audio options for 44/48/96 sample_rate and 16/24/32 bit bit_depth. CLI (All Platforms) and GUI version (For Windows)

![image](https://github.com/alxTools/video_resizer/assets/40523587/b5dcf84d-7095-4bd6-b35f-9ed8fccf7a06)

**GUI Mode**
![image](https://github.com/alxTools/video_resizer/assets/40523587/3b18b26d-6a23-48b5-83c6-214949f7edc7)

**CLI Mode**
![image](https://github.com/alxTools/video_resizer/assets/40523587/bb229e47-1965-4215-84a5-319091d860e8)

# add-exclusion-path in windows if neccessary
Add-MpPreference -ExclusionPath "C:\Users\alx\OneDrive\Desktop\video_resizer\video_resizer\" 

# build the executable
pyinstaller --onefile --windowed .\app.py --icon=icon.png --version-file=version_info.txt --name VidResizer_v1.exe