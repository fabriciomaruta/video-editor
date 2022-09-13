import config_loader
import video

if __name__ == '__main__':
    configs = config_loader.load_configs('video_config.yaml')
    output = configs.output_name
    print(output)
    streams = []
    for vfile in configs.files:
        print(vfile)
        if vfile.complete:
            streams.append(video.load_complete_media(vfile.fpath))
        else:
            start = int(vfile.start_at)
            end = int(vfile.end_at)
            duration = end - start
            streams.append(video.cut_video(vfile.fpath, start, duration))
    merged_video, merged_audio = video.concat_video_streams(streams)
    output = video.generate_output_stream(merged_video, merged_audio, output)
    video.run(output)
