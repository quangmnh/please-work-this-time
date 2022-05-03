from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import *
import numpy as np
import cv2
import numpy as np
import tensorflow as tf
import tensorrt as trt

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
    def get_boxes(self, frame, gray_frame = None):
        res = []
        if gray_frame is None:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (height, width) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104., 177., 123.))
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in range(0, detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence > self.conf_threshold:

                # Face bounding box
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                res.append(box)
                # (x, y, w, h) = box.astype('int')
                # cv2.rectangle(frame, (x, y), (w, h), (255, 255, 0), 2)
        return res

class ONNXClassifierWrapper():
    def __init__(self, file, num_classes, target_dtype = np.float32):
        
        self.target_dtype = target_dtype
        self.num_classes = num_classes
        self.load(file)
        
        self.stream = None
      
    def load(self, file):
        f = open(file, "rb")
        runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING)) 
        # trt.init_libnvinfer_plugins(None, '')
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
        self.context.execute_async_v2(self.bindings, self.stream.handle, None)
        # self.context.execute_async(1, self.bindings, self.stream.handle, None)
        # Transfer predictions back
        cuda.memcpy_dtoh_async(self.output, self.d_output, self.stream)
        # Syncronize threads
        self.stream.synchronize()
        
        return self.output
