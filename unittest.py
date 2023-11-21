import unittest
import subprocess
from unittest.mock import patch, call
from app import convert_video

class TestConvertVideo(unittest.TestCase):
    @patch('subprocess.Popen')
    def test_convert_video_4k(self, mock_popen):
        mock_popen.return_value = subprocess.CompletedProcess(args='ffmpeg', returncode=0)
        convert_video('input.mp4', 'output.mp4', '4K', '23', 'Copy Audio', '44100', '16')
        mock_popen.assert_called_once_with([
            'ffmpeg', '-y', '-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda', '-i', 'input.mp4',
            '-c:a', 'copy',
            '-vf', 'scale=3840:-1', '-c:v', 'hevc_nvenc', '-preset', 'p7', '-profile:v', 'main10',
            '-rc:v', 'vbr_hq', '-cq:v', '23', '-b:v', '25M', '-maxrate:v', '30M', '-bufsize:v', '30M',
            '-pix_fmt', 'yuv420p10le', 'output.mp4'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    @patch('subprocess.Popen')
    def test_convert_video_8k(self, mock_popen):
        mock_popen.return_value = subprocess.CompletedProcess(args='ffmpeg', returncode=0)
        convert_video('input.mp4', 'output.mp4', '8K', '23', 'FLAC Audio', '48000', '24')
        mock_popen.assert_called_once_with([
            'ffmpeg', '-y', '-hwaccel', 'cuda', '-hwaccel_output_format', 'cuda', '-i', 'input.mp4',
            '-c:a', 'flac', '-b:a', '320k', '-ar', '48000', '-sample_fmt', 's24',
            '-vf', 'scale=7680:-1', '-c:v', 'hevc_nvenc', '-preset', 'p7', '-rc:v', 'vbr_hq',
            '-cq:v', '23', '-b:v', '25M', '-maxrate:v', '30M', '-bufsize:v', '30M', 'output.mp4'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

if __name__ == '__main__':
    unittest.main()