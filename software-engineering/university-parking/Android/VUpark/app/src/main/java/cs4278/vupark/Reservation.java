package cs4278.vupark;

import java.sql.Time;
import java.util.Date;

/**
 * Created by Danny on 11/15/2017.
 * Class to hold an instance of a reservation.
 */

public class Reservation {
    private Date mStartDate;
    String mLotName;
    private int mSpotNumber;

    public Reservation(Date startDateTime, String lotName, int spotNumber){
        mStartDate = startDateTime;
        mLotName = lotName;
        mSpotNumber = spotNumber;
    }

    public Date getStartDate(){
        return mStartDate;
    }

    public void setStartDate(Date startDate){
        mStartDate = startDate;
    }

    public String getParkingLot() {
        return mLotName;
    }

    public void setGarageNumber(String lot) {
        mLotName = lot;
    }

    public int getmSpotNumber() {
        return mSpotNumber;
    }

    public void setSpotNumber(int spotNumber) {
        mSpotNumber = spotNumber;
    }
}
