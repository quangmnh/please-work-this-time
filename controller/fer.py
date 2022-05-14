from model_manager import *
from time import time
import sys

if __name__ == "__main__":
    # TODO: PLease use the true label var for choosing and playing the right playlist
    camera = CameraManagement()
    face_recognition = ONNXClassifierWrapper2(
        "controller/new_caffe.trt", [1, 1, 200, 7], 0.5, target_dtype=np.float32)
    emotion_recognition = ONNXClassifierWrapper(
        "controller/new_model.trt", [1, 5], target_dtype=np.float32)
    temp = {
        "Angry": 0,
        "Happy": 0,
        "Neutral": 0,
        "Sad": 0,
        "Surprise": 0,
    }
    for line in sys.stdin:
        start = time()
        while time() - start < 4:
            frame = camera.get_frame()
            if frame is None:
                # print("frame is none")
                continue
            else:
                box = face_recognition.predict(
                    camera.get_blob(frame))
                if box is None:
                    continue
                else:
                    # print(box)
                    # print(frame.shape)
                    (height, width) = frame.shape[:2]
                    box = box * np.array([width, height, width, height])
                    # (x, y, w, h) = box.astype('int')
                    roi = camera.get_roi(box, frame)
                    if roi is None:
                        continue
                    else:
                        label = emotion_recognition.predict(roi)
                        temp[label] += 1
        true_label = max(temp, key=temp.get)
        print(true_label)
