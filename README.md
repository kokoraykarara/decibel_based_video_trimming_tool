# decibel_based_video_trimming_tool
This is a Non AI tool designed to automatically detect and remove sections of a video where the audio level falls below a specified decibel threshold. This method is particularly useful for eliminating silent or low-volume parts of a video, ensuring that the final output contains only the relevant content with sufficient audio levels.

### English Explanation of the Code

This code is designed to process a video file by detecting and removing silent segments. The output is a new video file that excludes these silent portions. Below is a step-by-step explanation, especially for beginners.

#### 1. Importing Necessary Libraries
```python
import ffmpeg
from pydub import AudioSegment
import os
```
- **ffmpeg**: Used for video and audio processing.
- **pydub**: Handles audio file manipulation.
- **os**: Used for file and directory operations (not utilized in this specific script).

#### 2. Silence Removal Function
```python
def remove_silence(input_video, output_video, silence_threshold, chunk_size=1000):
```
This function removes silence from the video and creates a new file:
- **input_video**: The path to the input video file.
- **output_video**: The path to the output video file.
- **silence_threshold**: The threshold in decibels below which the audio is considered silent.
- **chunk_size**: The size of audio chunks (in milliseconds) used for analysis.

#### 3. Loading the Audio File and Splitting into Chunks
```python
audio = AudioSegment.from_file(input_video)
chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]
```
- **AudioSegment.from_file**: Loads the audio track from the video file.
- **chunks**: Splits the audio into small chunks based on the specified chunk size (e.g., 1000 ms).

#### 4. Detecting Silent Parts
```python
non_silent_ranges = []
start_time = 0
for chunk in chunks:
    if chunk.dBFS > silence_threshold:
        end_time = start_time + len(chunk)
        non_silent_ranges.append((start_time, end_time))
    start_time += len(chunk)
```
- **dBFS**: Decibels Full Scale, measures the loudness of each audio chunk.
- **non_silent_ranges**: Stores the start and end times of chunks that are above the silence threshold.

#### 5. Trimming Video and Audio Segments
```python
input_video_stream = ffmpeg.input(input_video)
final_video_segments = []
final_audio_segments = []
```
- **input_video_stream**: Loads the input video file using ffmpeg.
- **final_video_segments**: Holds the trimmed video segments that are not silent.
- **final_audio_segments**: Holds the trimmed audio segments that are not silent.

```python
for start, end in non_silent_ranges:
    video_segment = input_video_stream.video.trim(start=start/1000.0, end=end/1000.0).setpts('PTS-STARTPTS')
    audio_segment = input_video_stream.audio.filter_('atrim', start=start/1000.0, end=end/1000.0).filter_('asetpts', 'PTS-STARTPTS')
    
    final_video_segments.append(video_segment)
    final_audio_segments.append(audio_segment)
```
- **trim**: Trims the video and audio segments to the specified time intervals.
- **PTS-STARTPTS**: Resets the timestamps to create a new starting point for the trimmed segments.

#### 6. Concatenating Trimmed Segments and Creating the Output Video
```python
if final_video_segments and final_audio_segments:
    joined_video = ffmpeg.concat(*final_video_segments, v=1, a=0).node
    joined_audio = ffmpeg.concat(*final_audio_segments, v=0, a=1).node
    
    output = ffmpeg.output(joined_video[0], joined_audio[0], output_video, vcodec='libx264', acodec='aac')
    ffmpeg.run(output, overwrite_output=True)
else:
    print("No segments above the threshold were found.")
```
- **concat**: Joins all the video and audio segments together.
- **output**: Creates the final video file.
- **ffmpeg.run**: Processes the video and generates the output file.

#### 7. Main Function
```python
def main():
    input_video = "/Users/koraykara/Desktop/CODE/BERLINER/videos/video_edited_5min.mp4"  # Fixed input video path
    output_video = "/Users/koraykara/Desktop/CODE/BERLINER/videos/video_edited_5min_processed.mp4"  # Fixed output video path
    
    try:
        silence_threshold = float(input("Enter silence threshold (in dB, e.g., -15): "))
    except ValueError:
        print("Invalid value, please enter a number.")
        return

    remove_silence(input_video, output_video, silence_threshold)

if __name__ == "__main__":
    main()
```
- **main**: The main function of the program. It prompts the user for a silence threshold and calls the `remove_silence` function.
- **input_video** and **output_video**: The fixed paths for the input and output files.
- **silence_threshold**: The silence threshold provided by the user.

 
--------


This script is useful for anyone looking to remove unnecessary silent parts from a video, making it shorter and more concise. Initially, you might want to experiment with the silence threshold and chunk size to achieve the best results.

## How It Works

The script uses `ffmpeg` and `pydub` libraries to:
1. Load the audio track from the input video.
2. Split the audio into chunks of a specified size.
3. Detect silent parts by comparing each chunk's loudness against a user-defined threshold.
4. Trim the video and audio segments that are not silent.
5. Concatenate the trimmed segments and generate the final video.

## Requirements

Make sure to install the necessary libraries before running the script:

import ffmpeg
from pydub import AudioSegment
import os

The script will prompt you to enter the silence threshold (in dB). Adjust the threshold based on your video's audio characteristics.

Thanks to me and ChatGPT.

kokoraykarara
