from typing import List, Optional, Union
import yaml
from pydantic import BaseModel
from yaml.loader import SafeLoader

class SingleVideoConfig(BaseModel):
    fpath: str
    complete: bool
    start_at: Optional[Union[str, int]]
    end_at: Optional[Union[str, int]]
    volume: int

class ConfigModel(BaseModel):
    output_name: str
    files: List[SingleVideoConfig]

def check_video(video: dict) -> None:
    '''
    Check if configs is ok, if don't, raise error
    '''
    if 'complete' not in video:
        raise 'Missing complete field'
    if not video['complete']:
        if 'start_at' not in video:
            raise 'Missing start_at'
        if 'end_at' not in video:
            raise 'Missing end_at'

def parse_configs(config_dict: dict) -> ConfigModel:
    output_name = config_dict['output_name']
    videos = config_dict['inputs']
    videos_list = []
    for video in videos:
        check_video(video['input'])
        if video['input']['complete']:
            model = SingleVideoConfig(
                fpath=video['input']['file'],
                complete=True,
                volume=video['input']['volume']
            )
        else:
            model = SingleVideoConfig(
                fpath=video['input']['file'],
                complete=True,
                volume=video['input']['volume'],
                start_at=video['input']['start_at'],
                end_at=video['input']['end_at']
            )

        videos_list.append(model)
    return ConfigModel(
        output_name=output_name,
        files=videos_list
    )


def load_configs(config_path: str) -> ConfigModel:
    '''
    Receives config path and return Model
    '''
    with open(config_path) as f:
        data = yaml.load(f, Loader=SafeLoader)
        return parse_configs(data)


if __name__ == '__main__':
    print(load_configs('video_config.yaml'))

