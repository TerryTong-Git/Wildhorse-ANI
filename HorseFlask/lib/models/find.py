import cv2
import numpy as np
# import matplotlib.pyplot as plt
import os
import base64

net = cv2.dnn.readNetFromCaffe(os.path.dirname(__file__) + '/MobileNetSSD_deploy.prototxt.txt', os.path.dirname(__file__) + '/MobileNetSSD_deploy.caffemodel')
categories = { 0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat', 5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 
              9: 'chair', 10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse', 14: 'motorbike', 15: 'person', 
              16: 'pottedplant', 17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

# defined in list also
classes =  ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", 
            "diningtable",  "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# change image name to check different results
def detection(binary_image):
        image = cv2.imdecode(np.frombuffer(binary_image.read(), np.uint8), cv2.IMREAD_COLOR)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detections = net.forward()

        # colors = np.random.uniform(255, 0, size=(len(categories), 3))
        cropped_images_horses = []
        cropped_images_others = []
        for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                # print(confidence)
                if confidence >0.2:
                        idx = int(detections[0, 0, i, 1])
                        # print(idx)
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                #         label = "{}: {:.2f}%".format(categories[idx], confidence * 100)
                        # label = "{}: {:.2f}%".format(classes[idx], confidence * 100) 
                        # cv2.rectangle(image, (startX, startY), (endX, endY), colors[idx], 2)     
                        # y = startY - 15 if startY - 15>15 else startY + 15     
                        # cv2.putText(image, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 2)
                        if (idx==13):
                                cropped_image = image[startY:endY, startX:endX]
                                image_data = base64.b64encode(cv2.imencode('.jpg', cropped_image)[1]).decode()
                                cropped_images_horses.append([image_data,float(confidence)])
                        else:
                                cropped_image = image[startY:endY, startX:endX]
                                image_data = base64.b64encode(cv2.imencode('.jpg', cropped_image)[1]).decode()
                                cropped_images_others.append([image_data,float(confidence)])

        return {"horses": cropped_images_horses,
                "others": cropped_images_others}

# for i, cropped_image_array in enumerate(cropped_images_horses):
#     cv2.imwrite(f"Cropped_Image_{i+1}.jpg", cropped_image_array[0])
#     cv2.waitKey(0)
# for i, cropped_image_array in enumerate(cropped_images_others):
#     cv2.imwrite(f"Cropped_Image_other_{i+1}.jpg", cropped_image_array[0])
#     cv2.waitKey(0)
# cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# cv2.imwrite('./horse.jpg', image)
cv2.destroyAllWindows() 

# fig = plt.figure()
# ax1 = fig.add_axes((0.1, 0.2, 0.8, 0.7))
# # ax1.set_title('object detection')
# plt.axis("off")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# plt.show()


