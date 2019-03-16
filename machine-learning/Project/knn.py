from xlrd import open_workbook

class Datapoint:
	def __init__(self, age, apoe, ventricles, hippocampus, brain, mmse, classification):
		self.age = age
		self.apoe = apoe
		self.ventricles = ventricles
		self.hippocampus = hippocampus
		self.brain = brain
		self.mmse = mmse
		self.classification = classification

def calculate_distance(point1, point2):
	weighted = False
	euclidean = False

	age_divisor = float(1)
	apoe_divisor = float(1)
	vent_divisor = float(1)
	hip_divisor = float(1)
	brain_divisor = float(1)
	mmse_divisor = float(1)
	if weighted:
		# These are all the ranges of the variables
		age_divisor = 35.2
		apoe_divisor = float(2)
		vent_divisor = float(137314)
		hip_divisor = float(7488)
		brain_divisor = float(695325)
		mmse_divisor = float(12)

	distance = 0
	"""
	distance += abs(point1.age - point2.age)
	distance += abs(point1.apoe - point2.apoe)
	distance += abs(point1.ventricles - point2.ventricles)
	distance += abs(point1.hippocampus - point2.hippocampus)
	distance += abs(point1.brain - point2.brain)
	distance += abs(point1.mmse - point2.mmse)
	"""
	if euclidean:
		distance += float((point1.age - point2.age)*(point1.age - point2.age))/age_divisor
		distance += float((point1.apoe - point2.apoe)*(point1.apoe - point2.apoe))/apoe_divisor
		distance += float((point1.ventricles - point2.ventricles)*(point1.ventricles - point2.ventricles))/vent_divisor
		distance += float((point1.hippocampus - point2.hippocampus)*(point1.hippocampus - point2.hippocampus))/hip_divisor
		distance += float((point1.brain - point2.brain)*(point1.brain - point2.brain))/brain_divisor
		distance += float((point1.mmse - point2.mmse)*(point1.mmse - point2.mmse))/mmse_divisor
	else:
		distance += abs(point1.age - point2.age)/age_divisor
		distance += abs(point1.apoe - point2.apoe)/apoe_divisor
		distance += abs(point1.ventricles - point2.ventricles)/vent_divisor
		distance += abs(point1.hippocampus - point2.hippocampus)/hip_divisor
		distance += abs(point1.brain - point2.brain)/brain_divisor
		distance += abs(point1.mmse - point2.mmse)/mmse_divisor
	return distance

def find_k_nearest_neighbors(test_point, training_points, k):
	nearest_neighbors = []
	for training_point in training_points:
		dist = calculate_distance(test_point, training_point)
		if len(nearest_neighbors) < k:
			nearest_neighbors.append([training_point, dist])
		min_dist = dist
		min_index = -1
		for i in range(len(nearest_neighbors)):
			if nearest_neighbors[i][1] > min_dist:
				min_dist = nearest_neighbors[i][1]
				min_index = i
		if min_index != -1:
			nearest_neighbors[min_index] = [training_point, dist]
	return nearest_neighbors

def classify_from_nearest_neighbors(nearest_neighbors):
	classifications = {}
	for neighbor in nearest_neighbors:
		classification = neighbor[0].classification
		if classification in classifications:
			classifications[classification] = classifications[classification] + 1
		else:
			classifications[classification] = 1
	cur_class = None
	max_appearances = 0
	for key in classifications:
		if classifications[key] > max_appearances:
			cur_class = key
			max_appearances = classifications[key]
	return cur_class

def perform_knn(training_points, test_points, k):
	correct = 0
	for i in range(len(test_points)):
		nearest_neighbors = find_k_nearest_neighbors(test_points[i], training_points, k)
		classification = classify_from_nearest_neighbors(nearest_neighbors)
		if classification == test_points[i].classification:
			correct += 1
		else:
			print "Classified as", classification, "was actually", test_points[i].classification
	return correct

def leave_one_out_validation(training_points, k):
	correct = 0
	for i in range(len(training_points)):
		correct += perform_knn([x for index,x in enumerate(training_points) if index!=i], [training_points[i]], k)
	return correct


training_workbook = open_workbook("Training_Data.xlsx")
training_sheet = training_workbook.sheets()[0]
test_workbook = open_workbook("Test_Data.xlsx")
test_sheet = test_workbook.sheets()[0]

avg_for_missing_values = True

training_points = []

for row in range(1, training_sheet.nrows):
	age = float(training_sheet.cell(row, 2).value)
	apoe = int(training_sheet.cell(row, 6).value)
	vent_string = training_sheet.cell(row, 7).value
	if vent_string == "NA":
		vent_string = "0"
		if avg_for_missing_values:
			# 43600 = average value of ventricle mass
			vent_string = "43600"
	ventricles = int(vent_string)
	hippo_string = training_sheet.cell(row, 8).value
	if hippo_string == "NA":
		hippo_string = "0"
		if avg_for_missing_values:
			# 6498 = average value of hippocampus mass
			hippo_string = "6498"
	hippocampus = int(hippo_string)
	brain_string = training_sheet.cell(row, 9).value
	if brain_string == "NA":
		brain_string = "0"
		if avg_for_missing_values:
			# 993050 = average value of brain mass
			brain_string = "993050"
	brain = int(brain_string)
	mmse = int(training_sheet.cell(row, 10).value)
	classification = training_sheet.cell(row, 5).value
	if classification != "Alzheimer's":
		classification = "Not"

	new_point = Datapoint(age, apoe, ventricles, hippocampus, brain, mmse, classification)
	training_points.append(new_point)

test_points = []

for row in range(1, test_sheet.nrows):
	age = float(test_sheet.cell(row, 2).value)
	apoe = int(test_sheet.cell(row, 6).value)
	vent_string = test_sheet.cell(row, 7).value
	if vent_string == "NA":
		vent_string = "0"
		if avg_for_missing_values:
			# 43600 = average value of ventricle mass
			vent_string = "43600"
	ventricles = int(vent_string)
	hippo_string = test_sheet.cell(row, 8).value
	if hippo_string == "NA":
		hippo_string = "0"
		if avg_for_missing_values:
			# 6498 = average value of hippocampus mass
			hippo_string = "6498"
	hippocampus = int(hippo_string)
	brain_string = test_sheet.cell(row, 9).value
	if brain_string == "NA":
		brain_string = "0"
		if avg_for_missing_values:
			# 993050 = average value of brain mass
			brain_string = "993050"
	brain = int(brain_string)
	mmse = int(test_sheet.cell(row, 10).value)
	classification = test_sheet.cell(row, 5).value
	if classification != "Alzheimer's":
		classification = "Not"

	new_point = Datapoint(age, apoe, ventricles, hippocampus, brain, mmse, classification)
	test_points.append(new_point)

k = 20
correct = perform_knn(training_points, test_points, k)
print correct, "out of", len(test_points), "percentage", float(correct)/float(len(test_points))