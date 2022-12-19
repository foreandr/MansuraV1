from nsfw_detector import predict
model = predict.load_model('saved_model.h5')

# Predict single image
print("WE GOT TO HERE")
print(predict.classify(model, '2.jpg'))
#

