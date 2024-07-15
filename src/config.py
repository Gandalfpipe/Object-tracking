import os
import jstyleson
from dataclasses import dataclass
from typing import Tuple

Point = Tuple[int, int]
Box = Tuple[int, int, int, int]
Color = Tuple[int, int, int]

@dataclass
class Detection:
    name:str = ""
    rect:Box = (0,0,0,0)
    frame:int = 0
    color: Color = (0,0,0)

@dataclass
class Config:
    timeout:int = 25
    tracker:str = "mosse"
    video:str = ""
    objects: list[Detection] | None = None
    out:str|None = None

CONFIG = []

def loadcfg(cfgfile:str) -> Config:
    with open(cfgfile, "r") as fio:
        config = jstyleson.load(fio)
    video = os.path.join(os.path.dirname(cfgfile), config["video"])
    assert os.path.exists(video), f"File not exists: {video}"
    config["video"] = video
    config["objects"] = [Detection(**obj) for obj in config.get("objects", [])]
    
    CONFIG.clear()
    CONFIG.append(Config(**config))
    return CONFIG[0]

def conf() -> Config:
    return CONFIG[0] if len(CONFIG) > 0 else Config()
