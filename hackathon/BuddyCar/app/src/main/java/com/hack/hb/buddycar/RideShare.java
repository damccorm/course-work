package com.hack.hb.buddycar;



import java.util.ArrayList;

/**
 * Created by michaelriley on 11/12/16.
 */

public class RideShare {

    public String ID;

    public String myDriverID;

    public String myRiderID;

    public String myStartCity;

    public String myEndCity;

    public String myDate;

    public String getID()
    {
        return ID;
    }

    public String getDriverID(){
        return myDriverID;
    }

    public String getRiderID() {return myRiderID;}

    public String getMyStartCity(){
        return myStartCity;
    }

    public String getMyEndCity(){
        return myEndCity;
    }

    public String getMyDate(){
        return myDate;
    }

    public RideShare(){

    }

    //ctor
    public RideShare (String DriverID,String RiderID, String startCity, String endCity, String date) {
        //ID = tripId;
        myDriverID = DriverID;
        myRiderID = RiderID;
        myStartCity = startCity;
        myEndCity = endCity;
        myDate = date;
    }

    //Alt Constructor
    //Pre: The data must be in the order as follows, with only spaces in between
    //myTripId FK_ID myStartCity myEndCity isDriverToString() myDate
    /*RideShare(String rsData){
        int endtripIDIndex = rsData.indexOf("?-?");
        ID = rsData.substring(0, endtripIDIndex);

        String IDnum = rsData.substring(endtripIDIndex+3, rsData.length()-3);
        int IDnumIndex =IDnum.indexOf("?-?");
        FK_ID =rsData.substring(endtripIDIndex+3, IDnumIndex);

        String startCity = rsData.substring(IDnumIndex+3, rsData.length()-3);
        int startCityIndex =startCity.indexOf("?-?");
        myStartCity = rsData.substring(IDnumIndex+3, startCityIndex);

        String endCity = rsData.substring(startCityIndex+3, rsData.length()-3);
        int endCityIndex =endCity.indexOf("?-?");
        myEndCity = rsData.substring(startCityIndex+3, endCityIndex);

        String isDriver = rsData.substring(endCityIndex+3, rsData.length()-3);
        int isDriverIndex =isDriver.indexOf("?-?");
        String checkDriver = rsData.substring(endCityIndex+3, isDriverIndex);
        myIsDriver = checkDriver.equals("passenger");

        String date = rsData.substring(isDriverIndex+3, rsData.length()-3);
        int dateIndex =date.indexOf("?-?");
        myDate = rsData.substring(isDriverIndex+3, dateIndex);
    }

    public String myTripIDtoString(){
        return ID;
    }
    public String FK_IDtoString(){
        return FK_ID;
    }
    public String startToString(){
        return myStartCity;
    }
    public String endToString(){
        return myEndCity;
    }
    public String isDriverToString(){
        if(myIsDriver){
            return "driver";
        }else{
            return "passenger";
        }
    }
    public String dateToString(){
        return myDate;
    }

    public String toString(){
        String toReturn = ID + ' ' + FK_ID + ' ' + myStartCity;
        toReturn = toReturn + ' ' + myEndCity + isDriverToString() + ' ' + myDate;
        return toReturn;
    }

    public String listToString(PaginatedQueryList<RideShare> myList){
        String s = "";
        for (RideShare r: myList) {
            s = r.toString() + "!?n?!";
        }
        return s;
    }
    public ArrayList<RideShare> stringToList(String s){
        ArrayList<RideShare> myRides = new ArrayList<>();
        int index = 0;
        while (s.length() > 0){
            index = s.indexOf("!?n?!");
            RideShare temp = new RideShare(s.substring(0,index-1));
            myRides.add(temp);
            s=s.substring(index + 5);
        }

        return myRides;
    }*/
}
