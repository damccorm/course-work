from sklearn import svm
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
        race = sheet.cell(row, 4).value
        diagnosis = sheet.cell(row, 5).value
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

        dataset.append([age, gender, apoe4, ventricles, hippocampus, whole_brain, mmse])
        diagnosis_list.append(diagnosis)

    return dataset, diagnosis_list

def build_classifier_and_test(training_data, training_diagnoses, test_data, test_diagnoses, kernel_setting, c_setting, gamma_setting):
	clf = svm.SVC(kernel = kernel_setting, C = c_setting, gamma = gamma_setting)
	clf.fit(training_data, training_diagnoses)
	tot_correct = 0
	classifications = clf.predict(test_data)	
	for i in range(len(classifications)):
		if classifications[i] == test_diagnoses[i]:
			tot_correct += 1
	return tot_correct

def run_against_self_with_validation(dataset, diagnoses, num_validation_sets):
	dataset = dataset[:101]
	diagnoses = diagnoses[:101]
	kernel_settings_to_test = ["poly", "rbf"]
	c_settings_to_test = [0.1, 1, 10]
	gamma_settings_to_test = [0.1, 1, 10]
	for kernel_setting in kernel_settings_to_test:
		for c_setting in c_settings_to_test:
			for gamma_setting in gamma_settings_to_test:
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
					correct = build_classifier_and_test(non_validation_set, non_validation_diagnoses, validation_set, validation_diagnoeses, kernel_setting, c_setting, gamma_setting)
					tot_correct += correct
					tot_tested += len(validation_set)
					print tot_correct, tot_tested
				print "Kernel:", kernel_setting, "C:", c_setting, "Gamma:", gamma_setting
				print "TOTAL:", tot_correct, "out of", tot_tested, "for", 100*float(tot_correct)/float(tot_tested), "%"

def main():
	wb = open_workbook("Training_Data.xlsx")
	sheet = wb.sheets()[0]
	training_dataset, training_diagnoses = read_alzheimers_dataset(sheet)
	print "Dataset processed"

	run_against_self_with_validation(training_dataset, training_diagnoses, 5)

if __name__ == "__main__":
    main()
