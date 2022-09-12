import video

if __name__ == '__main__':
    video1 = video.cut_video('videos/GOPR6128.MP4', 610, 720)
    video2 = video.load_complete_media('videos/GP016128.MP4')
    video3 = video.cut_video('videos/GP026128.MP4', 0, 51)
    merged_video, merged_audio = video.concat_video_streams([video1, video2, video3])
    output = video.generate_output_stream(merged_video, merged_audio, 'jogo_wander.mp4')
    video.run(output)
