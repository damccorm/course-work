import random
from xlrd import open_workbook

wb = open_workbook("Data.xlsx")
sheet = wb.sheets()[0]
num_rows = sheet.nrows
correct_with_alzheimers = 0
correct_without_alzheimers = 0
total_with_alzheimers = 0
total_without_alzheimers = 0
for row in range(1, num_rows):
	cell = sheet.cell(row, 5).value
	rand = random.random()
	if cell == "AD":
		total_with_alzheimers += 1
		if rand < 0.139:
			correct_with_alzheimers += 1
	else:
		total_without_alzheimers += 1
		if rand >= 0.139:
			correct_without_alzheimers += 1

print "Correctly classified", correct_with_alzheimers, "instances out of", total_with_alzheimers, "instances with Alzheimer's"
print "Correctly classified", correct_without_alzheimers, "instances out of", total_without_alzheimers, "instances without Alzheimer's"