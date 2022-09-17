import config_loader
import video

'''
Fast-forwad/slow mo with audio
fmpeg -i output.mp4 -filter_complex "[0:v]setpts=0.25*PTS[v];[0:a]atempo=4[a]" -map "[v]" -map "[a]" ffwithaudio.mp4

Without audio
ffmpeg -i output.mp4 -filter:v "setpts=0.25*PTS" -an ffteste.mp4

'''
if __name__ == '__main__':
    # configs = config_loader.load_configs('video_config.yaml')
    # output = configs.output_name
    # print(output)
    # streams = []
    # for vfile in configs.files:
    #     print(vfile)
    #     if vfile.complete:
    #         streams.append(video.load_complete_media(vfile.fpath))
    #     else:
    #         start = int(vfile.start_at)
    #         end = int(vfile.end_at)
    #         duration = end - start
    #         streams.append(video.cut_video(vfile.fpath, start, duration))
    # merged_video, merged_audio = video.concat_video_streams(streams)
    # output = video.generate_output_stream(merged_video, merged_audio, output)
    # video.run(output)
    stream = video.load_complete_media('output.mp4')
    ffv, ffa = video.fast_forward(stream['v'], stream['a'], 0.25)
    out = video.generate_output_stream(ffv['v'], ffa, 'teste.mp4')
    video.run(out)
