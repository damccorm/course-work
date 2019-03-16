import csv
import numpy as np
import matplotlib.pyplot as plt

# open csv file to write logged data to
datafile = open("dataset_from_logs.csv",'w')
# write category names at beginning of file
datafile.write("Cores,Iterations,Regularization Parameter,MSE,Seconds\n")

# initialize dictionary for later use
dataset = {}

cores = [2, 4, 8, 12, 16]
iterations = [1,5,10,20]
reg_par = [0.01,0.1,1.0,10.0]
for corenum in cores:
	# initialize core number in dataset with a dictionary to hold data
	dataset[str(corenum)] = {}
	dataset[str(corenum)]["iterations"] = []
	dataset[str(corenum)]["mse"] = []
	dataset[str(corenum)]["seconds"] = []
	
	# open log file associated to corenum
	f = open("logs/pyspark%i.log" % (corenum))
	for line in f.readlines():
		tokens = line.split()
		if tokens[0] == "Iterations:":
			datafile.write("%i,%s,%s,%s," % (corenum,tokens[1],tokens[4],tokens[6]))
		elif tokens[0] == "Took":
			datafile.write("%s\n" % (tokens[1]))
# close csv file
datafile.close()

# creating a dictionary of values to plot
with open("dataset_from_logs.csv") as f:
	reader = csv.DictReader(f)
	for entry in reader:
		numcores = entry["Cores"]
		dataset[numcores]["iterations"].append(int(entry["Iterations"]))
		dataset[numcores]["mse"].append(float(entry["MSE"]))
		dataset[numcores]["seconds"].append(float(entry["Seconds"]))

# plotting desired values
iterVtime2 = plt.figure().add_subplot(111)
iterVtime4 = plt.figure().add_subplot(111)
iterVtime8 = plt.figure().add_subplot(111)
iterVtime12 = plt.figure().add_subplot(111)
iterVtime16 = plt.figure().add_subplot(111)
regVtime1 = plt.figure().add_subplot(111)
regVtime5 = plt.figure().add_subplot(111)
regVtime10 = plt.figure().add_subplot(111)
regVtime20 = plt.figure().add_subplot(111)
iterVmse2 = plt.figure().add_subplot(111)
iterVmse16 = plt.figure().add_subplot(111)

iterVtime2.plot(iterations,dataset["2"]["seconds"][0::4], label="0.01 reg param")
iterVtime2.plot(iterations,dataset["2"]["seconds"][1::4], label="0.1 reg param")
iterVtime2.plot(iterations,dataset["2"]["seconds"][2::4], label="1.0 reg param")
iterVtime2.plot(iterations,dataset["2"]["seconds"][3::4], label="10.0 reg param")
legend = iterVtime2.legend(loc='upper left', shadow=True, fontsize='x-large')
iterVtime2.set_ylabel('Time to complete (s)')
iterVtime2.set_xlabel('Iterations')
iterVtime2.set_title('Iterations vs. Time (2 cores)')

iterVtime4.plot(iterations,dataset["4"]["seconds"][0::4], label="0.01 reg param")
iterVtime4.plot(iterations,dataset["4"]["seconds"][1::4], label="0.1 reg param")
iterVtime4.plot(iterations,dataset["4"]["seconds"][2::4], label="1.0 reg param")
iterVtime4.plot(iterations,dataset["4"]["seconds"][3::4], label="10.0 reg param")
legend = iterVtime4.legend(loc='upper left', shadow=True, fontsize='x-large')
iterVtime4.set_ylabel('Time to complete (s)')
iterVtime4.set_xlabel('Iterations')
iterVtime4.set_title('Iterations vs. Time (4 cores)')

iterVtime8.plot(iterations,dataset["8"]["seconds"][0::4], label="0.01 reg param")
iterVtime8.plot(iterations,dataset["8"]["seconds"][1::4], label="0.1 reg param")
iterVtime8.plot(iterations,dataset["8"]["seconds"][2::4], label="1.0 reg param")
iterVtime8.plot(iterations,dataset["8"]["seconds"][3::4], label="10.0 reg param")
legend = iterVtime8.legend(loc='upper left', shadow=True, fontsize='x-large')
iterVtime8.set_ylabel('Time to complete (s)')
iterVtime8.set_xlabel('Iterations')
iterVtime8.set_title('Iterations vs. Time (8 cores)')

iterVtime12.plot(iterations,dataset["12"]["seconds"][0::4], label="0.01 reg param")
iterVtime12.plot(iterations,dataset["12"]["seconds"][1::4], label="0.1 reg param")
iterVtime12.plot(iterations,dataset["12"]["seconds"][2::4], label="1.0 reg param")
iterVtime12.plot(iterations,dataset["12"]["seconds"][3::4], label="10.0 reg param")
legend = iterVtime12.legend(loc='upper left', shadow=True, fontsize='x-large')
iterVtime12.set_ylabel('Time to complete (s)')
iterVtime12.set_xlabel('Iterations')
iterVtime12.set_title('Iterations vs. Time (12 cores)')

iterVtime16.plot(iterations,dataset["16"]["seconds"][0::4], label="0.01 reg param")
iterVtime16.plot(iterations,dataset["16"]["seconds"][1::4], label="0.1 reg param")
iterVtime16.plot(iterations,dataset["16"]["seconds"][2::4], label="1.0 reg param")
iterVtime16.plot(iterations,dataset["16"]["seconds"][3::4], label="10.0 reg param")
legend = iterVtime16.legend(loc='upper left', shadow=True, fontsize='x-large')
iterVtime16.set_ylabel('Time to complete (s)')
iterVtime16.set_xlabel('Iterations')
iterVtime16.set_title('Iterations vs. Time (16 cores)')

regVtime1.semilogx(reg_par,dataset["2"]["seconds"][0:4], label="2 cores")
regVtime1.semilogx(reg_par,dataset["4"]["seconds"][0:4], label="4 cores")
regVtime1.semilogx(reg_par,dataset["8"]["seconds"][0:4], label="8 cores")
regVtime1.semilogx(reg_par,dataset["12"]["seconds"][0:4], label="12 cores")
regVtime1.semilogx(reg_par,dataset["16"]["seconds"][0:4], label="16 cores")
regVtime1.set_ylabel('Time to complete (s)')
regVtime1.set_xlabel('Regularization Parameter')
regVtime1.set_title('Regularization Parameter vs. Time (1 iteration)')

regVtime5.semilogx(reg_par,dataset["2"]["seconds"][4:8], label="2 cores")
regVtime5.semilogx(reg_par,dataset["4"]["seconds"][4:8], label="4 cores")
regVtime5.semilogx(reg_par,dataset["8"]["seconds"][4:8], label="8 cores")
regVtime5.semilogx(reg_par,dataset["12"]["seconds"][4:8], label="12 cores")
regVtime5.semilogx(reg_par,dataset["16"]["seconds"][4:8], label="16 cores")
regVtime5.set_ylabel('Time to complete (s)')
regVtime5.set_xlabel('Regularization Parameter')
regVtime5.set_title('Regularization Parameter vs. Time (5 iterations)')

regVtime10.semilogx(reg_par,dataset["2"]["seconds"][8:12], label="2 cores")
regVtime10.semilogx(reg_par,dataset["4"]["seconds"][8:12], label="4 cores")
regVtime10.semilogx(reg_par,dataset["8"]["seconds"][8:12], label="8 cores")
regVtime10.semilogx(reg_par,dataset["12"]["seconds"][8:12], label="12 cores")
regVtime10.semilogx(reg_par,dataset["16"]["seconds"][8:12], label="16 cores")
regVtime10.set_ylabel('Time to complete (s)')
regVtime10.set_xlabel('Regularization Parameter')
regVtime10.set_title('Regularization Parameter vs. Time (10 iterations)')

regVtime20.semilogx(reg_par,dataset["2"]["seconds"][12:16], label="2 cores")
regVtime20.semilogx(reg_par,dataset["4"]["seconds"][12:16], label="4 cores")
regVtime20.semilogx(reg_par,dataset["8"]["seconds"][12:16], label="8 cores")
regVtime20.semilogx(reg_par,dataset["12"]["seconds"][12:16], label="12 cores")
regVtime20.semilogx(reg_par,dataset["16"]["seconds"][12:16], label="16 cores")
regVtime20.set_ylabel('Time to complete (s)')
regVtime20.set_xlabel('Regularization Parameter')
regVtime20.set_title('Regularization Parameter vs. Time (20 iterations)')

iterVmse2.plot(iterations,dataset["2"]["mse"][0::4], label="0.01 reg param")
iterVmse2.plot(iterations,dataset["2"]["mse"][1::4], label="0.1 reg param")
iterVmse2.plot(iterations,dataset["2"]["mse"][2::4], label="1.0 reg param")
iterVmse2.plot(iterations,dataset["2"]["mse"][3::4], label="10.0 reg param")
legend = iterVmse2.legend(loc='best', shadow=True, fontsize='x-large')
iterVmse2.set_ylabel('Mean Squared Error')
iterVmse2.set_xlabel('Iterations')
iterVmse2.set_title('Iterations vs. MSE (2 cores)')

iterVmse16.plot(iterations,dataset["2"]["mse"][0::4], label="0.01 reg param")
iterVmse16.plot(iterations,dataset["2"]["mse"][1::4], label="0.1 reg param")
iterVmse16.plot(iterations,dataset["2"]["mse"][2::4], label="1.0 reg param")
iterVmse16.plot(iterations,dataset["2"]["mse"][3::4], label="10.0 reg param")
legend = iterVmse16.legend(loc='best', shadow=True, fontsize='x-large')
iterVmse16.set_ylabel('Mean Squared Error')
iterVmse16.set_xlabel('Iterations')
iterVmse16.set_title('Iterations vs. MSE (16 cores)')

plt.show()
