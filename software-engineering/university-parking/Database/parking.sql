DROP TABLE IF EXISTS   Reservations, Logs, Spaces, Accounts, Prices;
SET FOREIGN_KEY_CHECKS=0;
CREATE TABLE Accounts (
	UserID VARCHAR(256) NOT NULL,
	Salt VARCHAR(256) NOT NULL,
	Hash VARCHAR(256) NOT NULL,
	Permit VARCHAR(16),
	AccountType VARCHAR(16),
	PRIMARY KEY(UserID)
);
CREATE TABLE Prices(
	PriceRateClass INT NOT NULL,
	StartTime Time NOT NULL,
	EndTime Time NOT NULL,
	RatePerHour Float NOT NULL,
	ReservationPrice Float NOT NULL,
	PRIMARY KEY(PriceRateClass, StartTime, EndTime)
);
CREATE TABLE Spaces (
	Lot VARCHAR(256) NOT NULL,
	Space INT NOT NULL,
	Permit VARCHAR(16) NOT NULL,
	PriceRateClass INT NOT NULL,
	Occupied boolean,
	PRIMARY KEY(Lot, Space)
);
CREATE TABLE Logs (
	UserID VARCHAR(256) NOT NULL,
	Lot VARCHAR(256) NOT NULL,
	Space INT NOT NULL,
	TimeIn DateTime NOT NULL,
	TimeOut DateTime,
	Rate FLOAT,
	PRIMARY KEY(UserID, TimeIn),
	UNIQUE(Lot, Space, TimeIn),
	FOREIGN KEY(UserID) REFERENCES Accounts(UserID),
	FOREIGN KEY(Lot, Space) REFERENCES Spaces(Lot, Space)
);
CREATE TABLE Reservations(
	UserID VARCHAR(256) NOT NULL,
	Lot VARCHAR(256) NOT NULL,
	Space INT NOT NULL,
	ScheduleStart DateTime NOT NULL,
	ScheduleEnd DateTime NOT NULL,
	Completion DateTime,
	ReservationPrice Float,
	PRIMARY KEY(UserID, Lot, Space, ScheduleStart),
	FOREIGN KEY(Lot, Space) REFERENCES Spaces(Lot, Space),
	FOREIGN KEY(UserID) REFERENCES Accounts(UserID)
);
INSERT INTO Accounts (UserID, Salt, Hash, Permit) VALUES ("Ben", "FakeSalt", "FakeHash", "VK");
INSERT INTO Spaces (Lot, Space, Permit, PriceRateClass, Occupied) VALUES ("Terrace Place", 1, "VK", 1, 0);
INSERT INTO Spaces (Lot, Space, Permit, PriceRateClass, Occupied) VALUES ("Terrace Place", 2, "VK", 0, 0);
INSERT INTO Spaces (Lot, Space, Permit, PriceRateClass, Occupied) VALUES ("Terrace Place", 3, "VK", 0, 0);
INSERT INTO Spaces (Lot, Space, Permit, PriceRateClass, Occupied) VALUES ("Terrace Place", 4, "VK", 0, 0);
INSERT INTO Spaces (Lot, Space, Permit, PriceRateClass, Occupied) VALUES ("Terrace Place", 5, "VK", 1, 0);
INSERT INTO Spaces (Lot, Space, Permit, PriceRateClass, Occupied) VALUES ("Terrace Place", 6, "VK", 1, 0);
INSERT INTO Prices (PriceRateClass, StartTime, EndTime, RatePerHour, ReservationPrice) VALUES (0, "00:00:00", "23:59:59", 2.5, 1.5);
INSERT INTO Prices (PriceRateClass, StartTime, EndTime, RatePerHour, ReservationPrice) VALUES (1, "00:00:00", "23:59:59", 0, 1.0);
SET FOREIGN_KEY_CHECKS=1;
