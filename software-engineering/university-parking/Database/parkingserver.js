const express = require('express');
const app = express();
const mysql = require('mysql');
const moment = require('moment');
const bodyParser = require('body-parser');
const randomstring = require('randomstring');
const crypto = require('crypto-js/sha256');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

const connection = mysql.createConnection({
	host:'parkingdatabase.c9dcrnrodp1p.us-east-2.rds.amazonaws.com',
 	user: 'ParkTeam',
 	password:'variablerateplanning',
 	database:'parking'
});
const LIMIT = 100;
connection.connect((err)=> {
})

app.post('/createAccount', (req, res) => {
	let uname = req.body.UserID;
	let pass = req.body.Password;
	let salt = randomstring.generate();
	let hash = crypto(pass+salt);
	let createUserQuery = "INSERT INTO Accounts SET ? ";
	connection.query(createUserQuery, {UserID: uname, "Salt": salt, "Hash": hash}, (err, createres) => {
		if(err){ 
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);}
		else{
			res.send(JSON.stringify({"Success" : createres.UserID}));
		}
	});
});
app.post('/validateCredentials', (req, res)=> {
	let uname = req.body.UserID;
	let pass = req.body.Password;
	let checkUserQuery = "SELECT * " +
						 "FROM Accounts " +
						 "WHERE UserID = " + uname;
	connection.query(checkUserQuery, (err, validres)=> {
		if(err){ 
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);}
		else{
			if(validres) {
				let salt = validres.Salt;
				if(validres.Hash==(crypto(salt + pass))) {
					res.send(JSON.stringify({"Success" : {"UserID": validres.UserID, "Permit": validres.Permit}}));	
				} else {
					let resObj = {"Failure": "Incorrect Password"};
					res.send(JSON.stringify(resObj));
				}
			} else {
				let resObj = {"Failure": "UserID not found"};
				res.send(JSON.stringify(resObj));
			}
		}
	})
})
app.get('/makeReservation', (req, res) => {
	let toIns = {}
	toIns.UserID = req.query.UserID;
	toIns.Lot = req.query.Lot;
	toIns.Space = req.query.Space;
	if(req.query.ScheduleStart) {
		toIns.ScheduleStart = req.query.ScheduleStart;
		toIns.ScheduleEnd = req.query.ScheduleEnd;
	} else {
		toIns.ScheduleStart = moment().format('YYYY-MM-DD HH:MM:SS');
		toIns.ScheduleEnd = moment().add(30, 'minutes').format('YYYY-MM-DD HH:MM:SS');
	}
	toIns.Completion = null;
	let startquery = "INSERT INTO Reservations SET ?";
	connection.query(startquery, toIns, (err, sqlres) => {
		if(err){ 
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);}
		else{
			let obj = {};
			obj["ScheduleEnd"] = sqlres.ScheduleEnd;
			obj["Lot"] = sqlres.Lot;
			obj["Space"] = sqlres.Space;
			res.send(JSON.stringify(obj));
		}

	})

});

app.get('/getAvailableLots', (req, res) => {
	let startquery = "SELECT Lot, Count(Space) as Numspaces "
										+ "FROM Spaces "
										+ "WHERE Occupied = 0 AND Permit = \" " + req.query.permit + "\" "
										+ " GROUP BY Lot";
	console.log(startquery);
	connection.query(startquery, (err, rows) => {
		if(err) {
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);
		}
		let obj = {};
		let count =0;
		rows.forEach( (row) => {
			let temp = {};
			temp.Lot = row.Lot;
			temp.Spaces = row.Numspaces;
			obj[count.toString()]= temp;
			count++;
		});
		res.send(JSON.stringify(obj));
	})
});

app.get('/getReservations', (req, res) => {
	let startquery = "SELECT * "
										+ "FROM Reservations "
										+ "WHERE UserID = " + req.query.UserID +
										" LIMIT " + LIMIT;
	console.log(startquery);
	connection.query(startquery, (err, rows) => {
		if(err) {
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);
		}
		let obj = {};
		let count =0;
		rows.forEach( (row) => {
		  //	UserID VARCHAR(256) NOT NULL,
			// 	Lot VARCHAR(256) NOT NULL,
			// 	Space INT NOT NULL,
			// 	ScheduleStart DateTime NOT NULL,
			// 	ScheduleEnd DateTime NOT NULL,
			// 	Completion DateTime,
			// 	ReservationPrice Float,
			let temp = {};
			temp.Lot = row.Lot;
			temp.Space = row.Space;
			temp.ScheduleStart = row.ScheduleStart;
			temp.ScheduleEnd = row.ScheduleEnd;
			temp.Completion = row.Completion;
			temp.ReservationPrice = row.ReservationPrice;
			obj[count.toString()]= temp;
			count++;
		});
		res.send(JSON.stringify(obj));
	})
});


app.get('/getPermit', (req, res) => {
	let startquery = "SELECT Permit "
										+ "FROM Accounts "
										+ "WHERE UserID = " + req.query.UserID;
	console.log(startquery);
	connection.query(startquery, (err, rows) => {
		if(err) {
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);
		}
		let obj = {};
		rows.forEach( (row) => {
			obj['permit']= row.Permit;
		});
		res.send(JSON.stringify(obj));
	})
});

app.get('/setPermit', (req, res) => {
	let startquery = "UPDATE Accounts "
										+ "Set Permit =  " + req.query.Permit
										+ " WHERE UserID = " + req.query.UserID;
	console.log(startquery);
	connection.query(startquery, (err, result) => {
		if(err) {
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);
		}
		let obj = {};
		obj['UserID'] = result.UserID;
		obj['Permit'] = result.Permit;
		res.send(JSON.stringify(obj));
	})
});

app.get('/getAvailableSpots', (req, res) => {
	let Date = new Date();
	let startquery = "SELECT Space, RatePerHour, ReservationPrice "
										+ "FROM Spaces x, Prices y "
										+ "WHERE x.Occupied = 0 AND x.Permit = \" " + req.query.permit + "\" "
										+ " AND x.PriceRateClass = y.PriceRateClass AND  GROUP BY Lot";
	console.log(startquery);
	connection.query(startquery, (err, rows) => {
		if(err) {
			console.log(err);
		}
		let obj = {};
		let count =0;
		rows.forEach( (row) => {
			let temp = {};
			temp.Lot = row.Lot;
			temp.Spaces = row.Numspaces;
			obj[count.toString()]= temp;
			count++;
		});
		res.send(JSON.stringify(obj));
	})
});

app.get('/checkIn', (req, res) => {
	let checkOpen = "Select * "+
					"FROM Spaces " +
					"WHERE Lot = " + req.query.Lot +
					" AND Space = " + req.query.Space +
					" AND (Occupied = 0 OR Occupied = NULL)";
	connection.query(checkOpen, (err, checkResp) => {
		if(err) {
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);
		}
		let checkCounter = 0;
		checkResp.forEach( (check) => {
			checkCounter ++;
		})
		if(checkCounter == 1) {
			let setOccupied = "UPDATE Spaces " +
							  "SET Occupied = 1 " +
							  "WHERE Lot = " + req.query.Lot +
							  " AND Space = " + req.query.Space;
			connection.query(setOccupied, (err, occupiedSuccess) => {
				if(err) {
					let resObj = {"Failure": "True"};
					res.send(JSON.stringify(resObj));
					console.log(err);
				}else {				
					let startquery = "SELECT * "
						+ "FROM Reservations "
						+ "WHERE UserID = " + req.query.UserID +
						" AND Lot = " + req.query.Lot + 
						" AND Space = " + req.query.Space + 
						" AND Completion = NULL ";
					console.log(startquery);
					connection.query(startquery, (err, rows) => {
					if(err) {
						let resObj = {"Failure": "True"};
						res.send(JSON.stringify(resObj));
						console.log(err);
					}
					let obj = {};
					let count = 0;
					rows.forEach( (row) => {
						count++;
					});
					if(count ==0) {
						let toIns = {}
						toIns["UserID"] = req.query.UserID;
						toIns["Lot"] = req.query.Lot;
						toIns["Space"] = req.query.Space;
						toIns["TimeIn"] = moment().format('YYYY-MM-DD HH:MM:SS');
						let curquery = "INSERT INTO Logs SET ?";
						connection.query(curquery, toIns, (err, sqlres)=> {
							if(err){ 
								let resObj = {"Failure": "True"};
								res.send(JSON.stringify(resObj));
								console.log(err);
							} else {
								//#TODO update occupied in logs, maybe have that be before the reservation check to make it more easily undoable
								let resObj = {"Success":"Parked in available spot"};
								res.send(JSON.stringify(resObj));
							}
						})	
					} else if (count ==1) {
						let toIns = {}
						toIns["UserID"] = req.query.UserID;
						toIns["Lot"] = req.query.Lot;
						toIns["Space"] = req.query.Space;
						toIns["TimeIn"] = moment().format('YYYY-MM-DD HH:MM:SS');
						let curquery = "INSERT INTO Logs SET ?";
						connection.query(curquery, toIns, (err, sqlres)=> {
							if(err){ 
								let resObj = {"Failure": "True"};
								res.send(JSON.stringify(resObj));
								console.log(err);
							} else {
								//#TODO update occupied in logs, maybe have that be before the reservation check to make it more easily undoable
								let updateResvQuery = "UPDATE Reservations SET COMPLETION = " + moment().format('YYYY-MM-DD HH:MM:SS') + 
													" + WHERE WHERE UserID = " + req.query.UserID +
													" AND Lot = " + req.query.Lot + 
													" AND Space = " + req.query.Space +
													" AND Completion = NULL";
								connection.query(updateResvQuery, (err,resvresp) => {
									if(err){ 
										let resObj = {"Failure": "True"};
										res.send(JSON.stringify(resObj));
										console.log(err);
									}
									let resObj = {"Success":"Reservation completed"}
									res.send(JSON.stringify(resObj));
								})
							}

						})	 
					}
					})
				}
			})
		} else {
			let resObj = {"Failure": "Spot is occupied"};
			res.send(JSON.stringify(resObj));
		}
	})
});

app.get('/checkIn', (req, res) => {
	let checkParked = "UPDATE Spaces " +
					"SET Occupied = 0" +
					"WHERE Lot = " + req.query.Lot +
					" AND Space = " + req.query.Space +
					" AND (Occupied = 1";
	connection.query(checkOpen, (err, checkResp) => {
		if(err){ 
			let resObj = {"Failure": "True"};
			res.send(JSON.stringify(resObj));
			console.log(err);
		}  else {
			if( checkResp.changedRows ==1) {
				let resObj = {"Success":"Unparked successfully"};
				res.send(JSON.stringify(resObj));
			} else {
				let resObj = {"Failure":"Was not parked beforehand"};
				res.send(JSON.stringify(resObj));
			}
		}
	})
});

app.listen(3000);
