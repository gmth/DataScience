#### Plan B file ####

from sklearn import svm
import random
import scipy
import getOrderFromBinaryClass as binEval
import numpy as np
from matplotlib import pyplot as plt

import lutorpy as lua
# setup runtime and use zero-based index(optional, enabled by default)
lua.LuaRuntime(zero_based_index=True)

# parameters and flags
TRAININGSIZE = 60 # parameter that indicates the number of set to be used for training the SVM
BINARY = True # Flag to indicate if we should use a binary scheme (-1, +1) or 8-class scheme (-4, -3, -2, -1, +1, +2, +3, +4)
USE_WEIGHTS = False # Flag to indicate if the SVM should use non-uniform class_weights



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

# C_individual_performance = []
# C_ranking_performance = []
# C = np.arange(0.5, 5.5, 0.5)
# for c in C:
######################	SPLITTING DATASETS, TRAINING AND PREDICTION 	####################
individual_prediction_scores = []
overall_scores = []
# k-fold cross-validation
for k in range(0, 1):
	print("k = " + str(k))

	######################	SPLITTING DATASETS	####################
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
                        with open('logs/testsets.log', 'a') as f:
                            f.write(str(key)+"\n")
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

	######################	TRAINING	####################
	print("Training SVM...")
	if (not BINARY) and USE_WEIGHTS:
		clf = svm.LinearSVC(class_weight = {-4: 4, -3: 3, -2: 2, -1: 1, 1: 1, 2: 2, 3: 3, 4: 4})
	else:
		clf = svm.LinearSVC(loss = 'squared_hinge')

	clf.fit(trainingdata, trainingclasses)
	print("...Training done!\n")

	######################	CLASSIFICATION 	####################
	print("Classifying testset...")
	prediction = clf.predict(testdata)

	confidence_scores = clf.decision_function(testdata)
	#print("Decision function: ", confidence_scores)

	print("...Classification done!\n")

	overall_scores.append(binEval.find_orders(prediction))
	individual_prediction_scores.append(clf.score(testdata, testclasses))

	# C_individual_performance.append(scipy.mean(individual_prediction_scores))
	# C_ranking_performance.append(scipy.mean(overall_scores))

######################	RESULTS OVERVIEW 	####################
print("prediction scores: " + str(individual_prediction_scores))
average_prediction_score = scipy.mean(individual_prediction_scores)
prediction_score_variance = scipy.var(individual_prediction_scores)

print("average individual prediction score: " + str(average_prediction_score * 100) + "%")
print("prediction score variance: " + str(prediction_score_variance) + "\n")

print("overall_scores: " + str(overall_scores))
print("Average overall score: " + str(scipy.mean(overall_scores)) + "\n")
print("----------------------------------------------\n")

# plt.figure(1)
# plt.subplot(211)
# plt.plot(C, C_individual_performance)
# plt.xlabel('C')
# plt.ylabel('indidual classification performance')

# plt.subplot(212)
# plt.plot(C, C_ranking_performance)
# plt.xlabel('C')
# plt.ylabel('ranking performance')

# plt.savefig('C_results.png')
