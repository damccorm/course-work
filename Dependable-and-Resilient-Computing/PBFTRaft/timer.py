import os , time

# Application Coded By: Slink
# Tested only on Linux. If you are on Windows, find all of the "clear" and change them to cls so the command can work.
# Don't be a skid.
# If you edit any of this (not including the os.system('clear') ) , then you're a skid.
# Video and site updated before uploaded. Attempt of credit stealing this will fail as prove can easily be shown.
# http://www.YouTube.Com/ReTrOSlink
# http:///www.slinksrealm.0fees.us


##about


def about():
	os.system('clear');
	print("Thank you for using! This is my third application in Python. Global variables are indeed important not only in python, but in many languages! Thank you to all who have been supporting me in this long journey!!!");
	time.sleep(12);
	menu()



def starttimer():
	#### vars
	global hour
	global minute
	global second

	os.system('clear');
	print hour, ":", minute, ":" , second
	time.sleep(1);
	second -= 1;

	if (second == -1):
		minute -= 1;
		second = 59;

	if (minute == -1):
		hour -= 1;
		minute = 59;

	if (hour == 0) and (minute == 0) and (second == 0):
		os.system('clear');
		print("Times Up!!!");
		time.sleep(5);
		userinputtime()

	starttimer()


## Exits application.
def doexit():
	os.system('clear');
	print("Thank you for using my application!!!");
	time.sleep(5);
	exit()


## prints menu.

def menu():
	os.system('clear');
	print("Select Your Option:");
	print("1. Start Timer:");
	print("2. About");
	print("3. Exit");
	option = input("Option:")
	if (option == 1):
		starttimer()
	elif (option == 2):
		about()
	elif (option == 3):
		doexit()
	else:
		print "Invalid Choice: " , option
		time.sleep(5);
		menu()




def userinputtime():
	os.system('clear');
	global hour
	hour = input("Enter Hours:");
	global minute
	minute = input("Enter Minutes:");
	global second
	second = input("Enter Seconds:");
	menu()



## start of the application.

os.system('clear');
print("Welcome To The Python Timer!!!");
print("By: Slink");
time.sleep(5);

userinputtime()
