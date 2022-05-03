import cv2
import numpy as np
import tensorflow as tf
import tensorrt as trt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import *

import pycuda.driver as cuda
import pycuda.autoinit

class KerasEmotionClassificationModel():
    __class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
    def __init__(self, model_path, display = False, GPU = True):
        self.model = load_model(model_path)
        self.display = display
    def predict(self, roi):
        predict = self.model.predict(roi)[0]
        label = self.__class_labels[predict.argmax()]
        return label
class SSDCaffeModel():
    def __init__(self, confidence_threshold = 0.5, modelFile = 'res10_300x300_ssd_iter_140000.caffemodel', configFile = 'deploy.prototxt.txt', display = False):
        self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
        self.conf_threshold = confidence_threshold
    def get_boxes(self, blob, frame):
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in range(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]
            (height, width) = frame.shape[:2]
            if confidence > self.conf_threshold:
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                return box
        return None


class ONNXClassifierWrapper():
    __class_labels = ['Angry', 'Happy', 'Neutral', 'Sad', 'Surprise']
    def __init__(self, file, num_classes, target_dtype = np.float32):
        
        self.target_dtype = target_dtype
        self.num_classes = num_classes
        self.load(file)
        
        self.stream = None
      
    def load(self, file):
        f = open(file, "rb")
        runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING)) 
        trt.init_libnvinfer_plugins(None, '')
        engine = runtime.deserialize_cuda_engine(f.read())
        self.context = engine.create_execution_context()
        
    def allocate_memory(self, batch):
        self.output = np.empty(self.num_classes, dtype = self.target_dtype) # Need to set both input and output precisions to FP16 to fully enable FP16

        # Allocate device memory
        self.d_input = cuda.mem_alloc(1 * batch.nbytes)
        self.d_output = cuda.mem_alloc(1 * self.output.nbytes)

        self.bindings = [int(self.d_input), int(self.d_output)]

        self.stream = cuda.Stream()
        
    def predict(self, batch): # result gets copied into output
        if self.stream is None:
            self.allocate_memory(batch)
            
        # Transfer input data to device
        cuda.memcpy_htod_async(self.d_input, batch, self.stream)
        # Execute model
        # self.context.execute_async_v2(self.bindings, self.stream.handle, None)
        self.context.execute_async(1, self.bindings, self.stream.handle, None)
        # Transfer predictions back
        cuda.memcpy_dtoh_async(self.output, self.d_output, self.stream)
        # Syncronize threads
        self.stream.synchronize()
        
        label = self.__class_labels[self.output.argmax()]
        return label

class ONNXClassifierWrapper2():
    def __init__(self, file, num_classes, conf_threshold = 0.5, target_dtype = np.float32):
        
        self.target_dtype = target_dtype
        self.num_classes = num_classes
        self.load(file)
        self.conf_threshold = conf_threshold
        self.stream = None
      
    def load(self, file):
        f = open(file, "rb")
        runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING)) 
        trt.init_libnvinfer_plugins(None, '')
        engine = runtime.deserialize_cuda_engine(f.read())
        self.context = engine.create_execution_context()
        
    def allocate_memory(self, batch):
        self.output = np.empty(self.num_classes, dtype = self.target_dtype) # Need to set both input and output precisions to FP16 to fully enable FP16

        # Allocate device memory
        self.d_input = cuda.mem_alloc(1 * batch.nbytes)
        self.d_output = cuda.mem_alloc(1 * self.output.nbytes)

        self.bindings = [int(self.d_input), int(self.d_output)]

        self.stream = cuda.Stream()
        
    def predict(self, batch): # result gets copied into output
        if self.stream is None:
            self.allocate_memory(batch)
            
        # Transfer input data to device
        cuda.memcpy_htod_async(self.d_input, batch, self.stream)
        # Execute model
        # self.context.execute_async_v2(self.bindings, self.stream.handle, None)
        self.context.execute_async(1, self.bindings, self.stream.handle, None)
        # Transfer predictions back
        cuda.memcpy_dtoh_async(self.output, self.d_output, self.stream)
        # Syncronize threads
        self.stream.synchronize()

        for i in range(0, self.output.shape[2]):
            confidence = self.output[0, 0, i, 2]

            if confidence > 0.5:
                return self.output[0, 0, i, 3:7] 
        return None

class CameraManagement():
    def __init__(self):
        self.video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    def get_frame(self):
        ret_val, frame = self.video_capture.read()
        return frame
    def get_blob(self, frame = None):
        if frame is None:
            frame = self.get_frame()
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104., 177., 123.))
        return blob
    def get_roi(self,box, frame = None):
        (x, y, w, h) = box.astype('int')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_roi = gray[y:h, x:w]
        if gray_roi.shape[0] == 0 or gray_roi.shape[1] == 0:
            return None
        else:
            gray_roi = cv2.resize(gray_roi, (48, 48), interpolation=cv2.INTER_AREA)
        if np.sum([gray_roi]) != 0:
            roi = gray_roi.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            return roi
        return None
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
def get_blob( frame):
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104., 177., 123.))
    return blob
def get_roi(box, frame):
    (x, y, w, h) = box.astype('int')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_roi = gray[y:h, x:w]
    if gray_roi.shape[0] == 0 or gray_roi.shape[1] == 0:
        return None
    else:
        gray_roi = cv2.resize(gray_roi, (48, 48), interpolation=cv2.INTER_AREA)
    if np.sum([gray_roi]) != 0:
        roi = gray_roi.astype('float') / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        return roi
    return None