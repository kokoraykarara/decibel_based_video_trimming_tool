import ffmpeg
from pydub import AudioSegment
import os

# FFmpeg ve ffprobe yollarını doğrudan belirt
AudioSegment.converter = r"C:\ffmpeg\ffmpeg-7.0.2-full_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\ffmpeg-7.0.2-full_build\bin\ffprobe.exe"

def remove_silence(input_video, output_video, silence_threshold=-20.0, chunk_size=1000):
    audio = AudioSegment.from_file(input_video)
    chunks = [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]
    
    # Sessiz kısımları tespit et
    non_silent_ranges = []
    start_time = 0
    for chunk in chunks:
        if chunk.dBFS > silence_threshold:
            end_time = start_time + len(chunk)
            non_silent_ranges.append((start_time, end_time))
        start_time += len(chunk)
    
    # Video ve ses segmentlerini kırpma
    input_video_stream = ffmpeg.input(input_video)
    final_video_segments = []
    final_audio_segments = []

    for start, end in non_silent_ranges:
        video_segment = input_video_stream.video.trim(start=start/1000.0, end=end/1000.0).setpts('PTS-STARTPTS')
        audio_segment = input_video_stream.audio.filter_('atrim', start=start/1000.0, end=end/1000.0).filter_('asetpts', 'PTS-STARTPTS')
        
        final_video_segments.append(video_segment)
        final_audio_segments.append(audio_segment)
    
    # Kırpılmış video ve ses parçalarını birleştir
    if final_video_segments and final_audio_segments:
        joined_video = ffmpeg.concat(*final_video_segments, v=1, a=0).node
        joined_audio = ffmpeg.concat(*final_audio_segments, v=0, a=1).node
        
        # Nihai videoyu oluşturma
        output = ffmpeg.output(joined_video[0], joined_audio[0], output_video, vcodec='h264_nvenc', acodec='aac')
        ffmpeg.run(output, overwrite_output=True)
    else:
        print("No segments above the threshold were found.")

input_video = r'D:\code\BERLINER\video_edit\videos\video1.mp4'  # Girdi video dosyanızın tam yolu
output_video = r'D:\code\BERLINER\video_edit\videos\output1.mp4'  # Çıktı video dosyanızın tam yolu

remove_silence(input_video, output_video)
