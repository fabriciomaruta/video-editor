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
    Receives the file path and cut video
    filepath: path to video
    start: video start point in seconds
    duration: video total duration in seconds
    '''
    stream = ffmpeg.input(filepath, ss=start, t=duration)
    return stream


if __name__ == '__main__':
    stream = ffmpeg.input('input.mp4', ss=240, t=15)
    # probe = ffmpeg.probe('input.mp4')
    # # print(probe['streams'])

    # # print(eval(probe['streams'][0]['r_frame_rate']))
    # fps = get_fps(probe)
    # start_time = convert_seconds_to_fps(4 * 60, fps)
    # end_time = convert_seconds_to_fps((4 * 60) + 15, fps)

    # print(start_time)
    # print(end_time)

    # # TODO: Use fps instead timestamp
    # output = stream.filter('trim', start=240, end=255)
    output = ffmpeg.output(stream, 'output.mp4')
    ffmpeg.run(output)
