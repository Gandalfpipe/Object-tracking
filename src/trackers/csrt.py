import cv2
from src.config import Config

def create(config: Config):
    params = cv2.TrackerCSRT_Params()
    #params.psr_threshold = 0.1
    tracker =  cv2.TrackerCSRT_create(params)
    return tracker