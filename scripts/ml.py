import joblib
from tensorflow import keras

import numpy as np
import cv2

model_from_joblib = joblib.load('models/irrigation-model.pkl')

