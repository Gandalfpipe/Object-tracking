import cv2
from src.config import Config

def create(config: Config):
    return cv2.legacy.TrackerBoosting_create()