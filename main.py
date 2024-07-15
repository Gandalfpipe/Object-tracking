#!/usr/bin/env python3
import os
import cv2
import logging
import sys
from src.config import loadcfg
from src.trackers import createTracker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main(cfgfile: str):
    config = loadcfg(cfgfile)
    cap = cv2.VideoCapture(config.video)

    o2frames = {}
    for o in config.objects:
        frame = o.frame
        lst = o2frames.get(frame)
        if not lst:
            o2frames[frame] = [o]
        else:
            lst.append(o)
  
    assert cap.isOpened(), "Error opening video stream or file"
  
    hasdebug = None
    frameno = 0
    objects = []
    trackers = []
    
    writer = cv2.VideoCapture(config.out) if config.out else None
    ret, frame = cap.read()
    if ret and config.out:
        fps = cap.get(cv2.CAP_PROP_FPS)
        video_FourCC = cv2.VideoWriter_fourcc(*"mp4v")
        h, w = frame.shape[0], frame.shape[1]
        _, ext = os.path.splitext(config.out)
        if ext != ".mp4":
            config.out += ".mp4"
        writer = cv2.VideoWriter(config.out, video_FourCC, fps, (w,h))
    else:
        writer = None
    while ret:
        showframe = frame.copy()
        if ret == False:
            break
        objs = o2frames.get(frameno)
        if objs:
            objects.extend(objs)
            trackers.extend([None] * len(objs))
            
        for i, o in enumerate(objects):
            if o is None:
                continue
            tracker = trackers[i]
            if tracker is None:
                l, t, w, h = o.rect
                box = (l, t, w, h)
                tracker = createTracker(config.tracker)
                tracker.init(frame, box)
                trackers[i] = tracker
                if hasdebug is None:
                    hasdebug = hasattr(tracker, "debug_draw")
                ok = True
            else:
                ok, box = tracker.update(frame)
                box = [int(b) for b in box]
            
            if ok:
            # rect draw
                thickness = 1
                color = o.color
                name = o.name
                cv2.rectangle(showframe, box, color=color, thickness=thickness)
                if name:
                    cv2.putText(showframe, name, (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

                if hasdebug:
                    tracker.debug_draw(showframe, name, color)
            else:
                objects[i] = None
                trackers[i] = None
        
        if writer is None:
            cv2.imshow('Frame', showframe)
            key = cv2.waitKey(config.timeout) & 0xFF
            if config.timeout > 0 and key == ord(' '):
                key = cv2.waitKey() & 0xFF
            if key == ord('q'):
                break
        else:
            writer.write(showframe)
        frameno+=1
        ret, frame = cap.read() # next frame
    
    if not writer is None:
        writer.release()
    cap.release()
  
    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
  if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} CONFIG")
    exit(1)
  main(sys.argv[1])