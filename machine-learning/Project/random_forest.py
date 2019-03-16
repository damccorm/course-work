from sklearn.ensemble import RandomForestClassifier
from xlrd import open_workbook
import csv

def read_alzheimers_dataset(sheet):
    # Takes data from sheet and formats it as list of lists with following format:
    # [age, gender, race, apoe4, ventricles, hippocampus, whole brain, mmse].
    # Also returns a list of associated diagnoses as a 2nd return value
    # Assumes that columns of sheet are formatted as follows:
    # VISCODE   PTID    AGE PTGENDER    PTRACCAT    DX.bl   APOE4   Ventricles.bl   Hippocampus.bl  WholeBrain.bl   MMSE    PTMARRY
    dataset = []
    diagnosis_list = []

    for row in range(1, sheet.nrows):
        age = float(sheet.cell(row, 2).value)
        gender = None
        if sheet.cell(row, 3).value == "Male":
        	gender = 0
    	else:
    		gender = 1
        race = 1
        if sheet.cell(row, 4).value == "White":
        	race = -1
    	elif sheet.cell(row, 4).value == "Black":
    		race = 0

        diagnosis = sheet.cell(row, 5).value
        if diagnosis == "Alzheimer's" or diagnosis == "AD":
        	diagnosis = "AD"
    	else:
    		diagnosis = "NOT"
        apoe4 = int(sheet.cell(row, 6).value)
        ventricles = -1
        if sheet.cell(row, 7).value != "NA":
            ventricles = int(sheet.cell(row, 7).value)
        hippocampus = -1
        if sheet.cell(row, 8).value != "NA":
            hippocampus = int(sheet.cell(row, 8).value)
        whole_brain = -1
        if sheet.cell(row, 9).value != "NA":
            whole_brain = int(sheet.cell(row, 9).value)
        mmse = int(sheet.cell(row, 10).value)

        dataset.append([age, gender, race, apoe4, ventricles, hippocampus, whole_brain, mmse])
        diagnosis_list.append(diagnosis)

    return dataset, diagnosis_list

def build_classifier_and_test(training_data, training_diagnoses, test_data, test_diagnoses, features_per_split, depth, num_trees_per_forest):
	clf = RandomForestClassifier(n_estimators=num_trees_per_forest, max_features = features_per_split, max_depth = depth)
	clf.fit(training_data, training_diagnoses)
	tot_correct = 0
	test_data_with_alzheimers = []
	test_data_without_alzheimers = []
	for i in range(len(test_data)):
		if test_diagnoses[i] == "AD":
			test_data_with_alzheimers.append(test_data[i])
		else:
			test_data_without_alzheimers.append(test_data[i])

	with_alzheimers_classification = clf.predict(test_data_with_alzheimers)
	tot_correct_with = 0
	for classification in with_alzheimers_classification:
		if classification == "AD":
			tot_correct_with += 1

	without_alzheimers_classification = clf.predict(test_data_without_alzheimers)
	tot_correct_without = 0
	for classification in without_alzheimers_classification:
		if classification != "AD":
			tot_correct_without += 1

	print "With", tot_correct_with, "Without", tot_correct_without
	return (tot_correct_with + tot_correct_without)

def run_leave_one_out_validation(dataset, diagnoses):
	feature_setting = 4
	depth_setting = 4
	num_tree_setting = 10
	with_alzheimers_correct = 0
	without_alzheimers_correct = 0
	for i in range(len(dataset)):
		train_set = dataset[:i] + dataset[i+1:]
		training_diagnose_set = diagnoses[:i] + diagnoses[i+1:]
		correct = build_classifier_and_test(train_set, training_diagnose_set, [dataset[i]], [diagnoses[i]], feature_setting, depth_setting, num_tree_setting)
		if correct > 0:
			if diagnoses[i] == "AD" or diagnoses[i] == "Alzheimer's":
				with_alzheimers_correct += 1
			else:
				without_alzheimers_correct += 1
	print "With alzheimers correct", with_alzheimers_correct, "Without alzheimers correct", without_alzheimers_correct, "Total instances", len(dataset)

def run_against_self_with_validation(dataset, diagnoses, num_validation_sets):
	feature_settings_to_test = [2,4,6]
	depth_settings_to_test = [2,4,6]
	num_tree_settings_to_test = [5,10,50]

	for feature_setting in feature_settings_to_test:
		for depth_setting in depth_settings_to_test:
			for num_tree_setting in num_tree_settings_to_test:
				tot_correct = 0
				tot_tested = 0
				size_of_validation_sets = len(dataset)/num_validation_sets
				for i in range(num_validation_sets):
					start = i*size_of_validation_sets
					end = (i+1)*size_of_validation_sets
					if i == num_validation_sets - 1:
						end = len(dataset)
					validation_set = dataset[start:end]
					validation_diagnoeses = diagnoses[start:end]
					non_validation_set = dataset[:start] + dataset[end:]
					non_validation_diagnoses = diagnoses[:start] + diagnoses[end:]
					correct = build_classifier_and_test(non_validation_set, non_validation_diagnoses, validation_set, validation_diagnoeses, feature_setting, depth_setting, num_tree_setting)
					tot_correct += correct
					tot_tested += len(validation_set)
				print "# Features:", feature_setting, "Depth:", depth_setting, "# Trees:", num_tree_setting
				print "TOTAL:", tot_correct, "out of", tot_tested, "for", 100*float(tot_correct)/float(tot_tested), "%"

def main():
	wb = open_workbook("Training_Data.xlsx")
	sheet = wb.sheets()[0]
	training_data, training_diagnoses = read_alzheimers_dataset(sheet)
	wb = open_workbook("Test_Data.xlsx")
	sheet = wb.sheets()[0]
	test_data, test_diagnoses = read_alzheimers_dataset(sheet)
	print "Dataset processed"

	build_classifier_and_test(training_data, training_diagnoses, test_data, test_diagnoses, 4, 4, 10)

if __name__ == "__main__":
    main()
