import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model,Sequential
from keras.preprocessing import image
from keras.optimizers import SGD
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import pydot
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
# from kt_utils import *
import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from numpyArrayBuildup import *


X_train_orig, Y_train_orig=loadDataset()
X_test_orig, Y_test_orig=testDataSet()
X_train = X_train_orig.reshape(X_train_orig.shape[0],-1)
Y_train=Y_train_orig.reshape(Y_train_orig.shape[0],-1)
X_test = X_test_orig.reshape(X_test_orig.shape[0],-1)
Y_test=Y_test_orig.reshape(Y_test_orig.shape[0],-1)
print ("number of training examples = " + str(X_train.shape[0]))
print ("X_train shape: " + str(X_train.shape))
print ("Y_train shape: " + str(Y_train.shape))

print ("number of test examples = " + str(X_test.shape[0]))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))
# GRADED FUNCTION: HappyModel

# def HappyModel(input_shape):
#     """
#     Implementation of the HappyModel.
#
#     Arguments:
#     input_shape -- shape of the images of the dataset
#
#     Returns:
#     model -- a Model() instance in Keras
#     """
#
#     ### START CODE HERE ###
#     # Feel free to use the suggested outline in the text above to get started, and run through the whole
#     # exercise (including the later portions of this notebook) once. The come back also try out other
#     # network architectures as well.
#     X_input = Input(input_shape)
#
#     X=Dense(1040, activation='relu', name='HL0')(X_input)
#
#     X=Dense(1040, activation='relu', name='HL1')(X)
#
#     X=Dense(520, activation='relu', name='HL2')(X)
#
#     X=Dense(520, activation='relu', name='HL3')(X)
#
#     X=Dense(260, activation='relu', name='HL4')(X)
#
#     X=Dense(104, activation='relu', name='HL5')(X)
#
#     X=Dense(104, activation='sigmoid', name='HL6')(X)
#
#
#
#     # model=Sequential()
#     # model.add(Dense(units=, activation='relu', input_dim=100))
#     # model.add(Dense(units=10, activation='softmax'))
#     # Zero-Padding: pads the border of X_input with zeroes
#     # X = ZeroPadding2D((2, 2))(X_input)
#
#     # # CONV -> BN -> RELU Block applied to X
#     # X = Conv2D(320, (7, 7), strides = (1, 1), name = 'conv0')(X)
#     # X = BatchNormalization(axis = 1, name = 'bn0')(X)
#     # X = Activation('relu')(X)
#     #
#     # # CONV -> BN -> RELU Block applied to X
#     # X = Conv2D(32, (7, 7), strides = (1, 1), name = 'conv1')(X)
#     # X = BatchNormalization(axis = 1, name = 'bn1')(X)
#     # X = Activation('relu')(X)
#     #
#     # # MAXPOOL
#     # X = MaxPooling2D((2, 2), name='max_pool')(X)
#     #
#     # # FLATTEN X (means convert it to a vector) + FULLYCONNECTED
#     # X = Flatten()(X)
#     # X = Dense(104, activation='sigmoid', name='fc')(X)
#
#     # Create model. This creates your Keras model instance, you'll use this instance to train/test the model.
#     model = Model(inputs = X_input, outputs = X, name='HappyModel')
#
#     ### END CODE HERE ###
#
#     return model


### START CODE HERE ### (1 line)
# happyModel = HappyModel((1040,))
happyModel = Sequential()
happyModel.add(Dense(1040, activation='relu', input_dim=X_train.shape[1]))
happyModel.add(Dropout(0.1))
happyModel.add(Dense(1040, activation='relu'))
happyModel.add(Dropout(0.1))
happyModel.add(Dense(520, activation='relu'))
happyModel.add(Dropout(0.1))
happyModel.add(Dense(520, activation='relu'))
happyModel.add(Dropout(0.1))
happyModel.add(Dense(260, activation='relu'))
happyModel.add(Dropout(0.1))
happyModel.add(Dense(104, activation='relu'))
happyModel.add(Dropout(0.1))
happyModel.add(Dense(Y_train.shape[1], activation='sigmoid'))

### END CODE HERE ###
### START CODE HERE ### (1 line)
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
happyModel.compile(optimizer = 'adam',loss = "binary_crossentropy",metrics = ["accuracy"])
# happyModel.compile(optimizer = sgd,loss = "binary_crossentropy")

### END CODE HERE ###
### START CODE HERE ### (1 line)
happyModel.fit(X_train, Y_train,epochs =30 ,batch_size = 32 )
### END CODE HERE ###
### START CODE HERE ### (1 line)
preds = happyModel.evaluate(X_train, Y_train)
predsTest = happyModel.evaluate(X_test,Y_test)
### END CODE HERE ###
classes=happyModel.predict(X_test)
print("%%%%%%%%%%%%%%%")
print(classes.shape, type(classes))
effectiveBitsPredicted=[]
effectiveBitsOriginal=[]
for i in range (classes.shape[0]):
    effectiveBits=[]
    for j in range(classes.shape[1]):
        if classes[i][j]<0.5:
            classes[i][j]=int(0)
        elif classes[i][j]>=0.5:
            classes[i][j]=int(1)
            effectiveBits.append(j)
    effectiveBitsPredicted.append(effectiveBits)

for i in range (Y_test.shape[0]):
    effectiveBits=[]
    for j in range(Y_test.shape[1]):
        if Y_test[i][j]<0.5:
            Y_test[i][j]=int(0)
        elif Y_test[i][j]>=0.5:
            Y_test[i][j]=int(1)
            effectiveBits.append(j)
    effectiveBitsOriginal.append(effectiveBits)

print(type(classes[0][100]),classes.shape)
# for i in range (classes.shape[0]):
#     effectiveBits=[]
#     for j in range(classes.shape[1]):
#         if classes[i][j]==int(1):
#             effectiveBits.append(j)
#     effectiveBitsPredicted.append(effectiveBits)

classes=np.transpose(classes)

# print(type(classes[1][100]),classes.shape)

fwrite=open('effectiveBitsSetsPredicted','w')
for k in effectiveBitsPredicted:
    fwrite.write(str(k)+'\n')
fwrite.close()

fwrite=open('effectiveBitsSetsOriginal','w')
for k in effectiveBitsOriginal:
    fwrite.write(str(k)+'\n')
fwrite.close()

np.savetxt("testPredictions.csv",classes, delimiter=',')
print()
print ("Loss Training = " + str(preds[0]))
print ("Training Accuracy = " + str(preds[1]))
print ("Loss Test = " + str(predsTest[0]))
print ("Test Accuracy = " + str(predsTest[1]))
happyModel.summary()
plot_model(happyModel, to_file='HappyModel.png')
# SVG(model_to_dot(happyModel).create(prog='dot', format='svg'))
