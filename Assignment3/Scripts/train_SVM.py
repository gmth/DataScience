#### Plan B file ####

from sklearn import svm
import random
import scipy
import lutorpy as lua
# setup runtime and use zero-based index(optional, enabled by default)
lua.LuaRuntime(zero_based_index=True)

# parameters and flags
TRAININGSIZE = 60 # parameter that indicates the number of set to be used for training the SVM
BINARY = True # Flag to indicate if we should use a binary scheme (-1, +1) or 8-class scheme (-4, -3, -2, -1, +1, +2, +3, +4)


######################	DATA LOADING ####################
print("Loading data...")
luaFeaturesTable = torch.load('features.t7')
luaFeatures = luaFeaturesTable.features
features = luaFeatures.asNumpyArray()

luaImagesList = luaFeaturesTable.image_list
imagesList = []
for i in range(0, 350):
	if (len(luaImagesList[i]) == 34):
		imagesList.append(str(luaImagesList[i][-9:-4]))
	elif (len(luaImagesList[i]) == 33):
		imagesList.append(str(luaImagesList[i][-8:-4]))
	else:
		imagesList.append(str(luaImagesList[i][-7:-4]))

featuresDict = {}

for i in range(0, len(imagesList)):
	setnumber = imagesList[i][:-2]
	image_index = int(imagesList[i][-1:]) - 1
	if (setnumber not in featuresDict): 
		featuresDict[setnumber] = [-1] * 5
		featuresDict[setnumber][image_index] = features[i]
	else:
		featuresDict[setnumber][image_index] = features[i]

print("...loaded data.")
print(str(len(featuresDict)) + " image sets loaded. " + str(len(imagesList)) + " images in total.\n")

######################	SPLITTING DATASETS, TRAINING AND PREDICTION 	####################
prediction_errors = []
# k-fold cross-validation
for k in range(0, 1):
	print("k = " + str(k))
	print("Splitting data in trainingdata and testdata...")
	trainingsets = []
	trainingdata = []
	trainingclasses = []

	testdata = []
	testclasses = []

	counter = 0
	while counter < TRAININGSIZE:
		choice = random.choice(featuresDict.keys())
		if choice not in trainingsets:
			trainingsets.append(choice)
			counter += 1

	for key in featuresDict:
		if key in trainingsets:
			for i in range(0,4):
				for j in range(i+1, 5):
					trainingdata.append(featuresDict[key][i] - featuresDict[key][j])
					trainingdata.append(featuresDict[key][j] - featuresDict[key][i])
					if BINARY:
						trainingclasses.append(-1)
						trainingclasses.append(1)
					else:
						trainingclasses.append(i - j)
						trainingclasses.append(j - i)
			counter += 1
		else:
			for i in range(0,4):
				for j in range(i+1, 5):
					testdata.append(featuresDict[key][i] - featuresDict[key][j])
					testdata.append(featuresDict[key][j] - featuresDict[key][i])
					if BINARY:
						testclasses.append(-1)
						testclasses.append(1)
					else:
						testclasses.append(i - j)
						testclasses.append(j - i)

	print("...Split data into a trainingset with " + str(len(trainingclasses)) + " samples and a testset with " + str(len(testclasses)) + " samples.\n")


	print("Training SVM...")
	clf = svm.LinearSVC()
	clf.fit(trainingdata, trainingclasses)
	print("...Training done!\n")

	print("Classifying testset...")
	prediction = clf.predict(testdata)

	correct_counter = 0
	false_counter = 0
	exactly_correct_counter = 0
	for i in range(0, len(testclasses)):
		if ((testclasses[i] < 0) and (prediction[i] < 0)) or ((testclasses[i] > 0) and (prediction[i] > 0)):
			correct_counter += 1
			if (testclasses[i] == prediction[i]):
				exactly_correct_counter += 1
		else:
			false_counter += 1

	print("...Classification done!\n")

	# print("correct: " + str(correct_counter))
	# print("exactly correct: " + str(exactly_correct_counter))
	# print("wrong: " + str(false_counter))
	prediction_errors.append(float(false_counter)/float(len(testclasses)))
	print("prediction error: " + str(prediction_errors[k]) + "\n------------------------------\n")

######################	RESULTS OVERVIEW 	####################
print("prediction_errors: " + str(prediction_errors))
average_prediction_error = scipy.mean(prediction_errors)#sum(prediction_errors) / len(prediction_errors)
prediction_error_variance = scipy.var(prediction_errors)
print("average prediction error: " + str(average_prediction_error))
print("prediction variance: " + str(prediction_error_variance) + "\n")