from typing import Any

import ffmpeg


def convert_seconds_to_fps(input_seconds: int, framerate: float) -> int:
    '''
    Function to output desired frame number
    '''
    frame = input_seconds * framerate
    return int(frame)


def get_fps(probe: dict) -> float:
    '''
    Expects ffmpeg probe output and return FPS in float
    '''
    fps = probe['streams'][0]['r_frame_rate']
    return eval(fps)


def cut_video(filepath: str, start: int, duration: int) -> Any:
    '''
    Receives the file path and cut video, returning a stream
    (cutted video)
    filepath: path to video
    start: video start point in seconds
    duration: video total duration in seconds
    '''
    stream = ffmpeg.input(filepath, ss=start, t=duration)
    return stream


def concat_video_streams(streams: list) -> Any:
    '''
    Receives a stream list and concat them in list order
    Output is a tuple with audio and video demuxed
    '''
    resulting_stream = None
    try:
        for stream in streams:
            if resulting_stream is None:
                resulting_stream = ffmpeg.concat(stream['v'],
                                                 stream['a'],
                                                 v=1, a=1, unsafe=True).node
            else:
                resulting_stream = ffmpeg.concat(
                    resulting_stream[0],
                    resulting_stream[1],
                    stream['v'],
                    stream['a'],
                    v=1, a=1, unsafe=True).node
    except Exception as e:
        raise e
    if resulting_stream is not None:
        return resulting_stream[0], resulting_stream[1]
    else:
        raise 'Unexpected error'


def merge_audios(streams: list) -> Any:
    '''
    Receives an audio list and merge them into one single track
    '''
    return ffmpeg.filter(streams, 'amix')


def mix_audio_video(video_track: Any, audio_track: Any) -> Any:
    '''
    Receives an audio track and a video track and merge them
    Return video and audio separatedly
    '''
    try:
        resulting_stream = ffmpeg.concat(video_track.video, audio_track).node
        return resulting_stream[0], resulting_stream[1]
    except Exception as e:
        raise e


def normalize_audio(audio_track: Any, volume: float)->Any:
    '''
    Receives an audio track and normalize audio, 0 is muted 1 is the
    current level
    '''
    try:
        normalized = ffmpeg.filter(audio_track,
                                   'volume', volume=str(volume))
        return normalized
    except Exception as e:
        raise e


if __name__ == '__main__':
    audio1 = cut_video('sample4.mp3', 0, 15)
    video1 = cut_video('input.mp4', 0, 15)
    normalized_audios = ffmpeg.filter(video1.audio, 'volume', volume='0.3')
    merge_audios = ffmpeg.filter([audio1, normalized_audios], 'amix')

    out = ffmpeg.concat(
        video1.video,
        merge_audios,
        a=1, v=1
    ).output('output.mp4').run(overwrite_output=True)
    # out = ffmpeg.output(out, 'output.mp4')
    # ffmpeg.run(out)
