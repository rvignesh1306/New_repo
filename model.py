import tensorflow as tf

class ImageClassifier:
    def __init__(self):
        self.model = tf.keras.applications.MobileNetV2(weights='imagenet')
    
    def classify_image(self, img):
        img = tf.image.resize(img, (224, 224))
        img = tf.expand_dims(img, axis=0)
        predictions = self.model.predict(img)
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        return decoded_predictions
