package com.hack.hb.buddycar;

/**
 * Created by Harrison on 11/12/16.
 */

public class Profile {

    public String ID;

    public String deviceId;

    public String name;

    public double rating;

    public int numRatings;

    public String bio;

    public int age;

    public String gender;

    public Profile(){

    }
    //Constructor
    Profile(String androidID, String profName, String profBio, int profAge, String profGender) {
        deviceId = androidID;
        name = profName;
        bio = profBio;
        age = profAge;
        gender = profGender;

        numRatings = 0;
        rating = 0;
    }

    //Alt Constructor
//    //Pre: The data must be in the order as follows, with only spaces in between
//    //ID name rating numRatings bio age gender
//    Profile(String profileData){
//        int endIDIndex = profileData.indexOf(".?.");
//        ID = profileData.substring(0, endIDIndex);
//
//        String endName = profileData.substring(endIDIndex+3, profileData.length()-3);
//        int endNameIndex =endName.indexOf(".?.");
//        name = profileData.substring(endIDIndex+3, endNameIndex);
//
//        String endRating = profileData.substring(endNameIndex+3, profileData.length()-3);
//        int endRatingIndex =endRating.indexOf(".?.");
//        rating = Double.parseDouble(profileData.substring(endNameIndex+3, endRatingIndex));
//
//        String endNumRatings = profileData.substring(endRatingIndex+3, profileData.length()-3);
//        int endNumRatingsIndex =endNumRatings.indexOf(".?.");
//        numRatings = Integer.parseInt(profileData.substring(endRatingIndex+3, endNumRatingsIndex));
//
//        String endBio = profileData.substring(endNumRatingsIndex+3, profileData.length()-3);
//        int endBioIndex =endBio.indexOf(".?.");
//        bio = profileData.substring(endNumRatingsIndex+3, endBioIndex);
//
//        String endAge = profileData.substring(endBioIndex+3, profileData.length()-3);
//        int endAgeIndex =endAge.indexOf(".?.");
//        age = Integer.parseInt(profileData.substring(endBioIndex+3, endAgeIndex));
//
//        String endGender = profileData.substring(endAgeIndex+3, profileData.length()-3);
//        int endGenderIndex =endGender.indexOf(".?.");
//        gender = profileData.substring(endAgeIndex+3, endGenderIndex);
//    }


    public void modifyRating (int newStars) {
        rating = rating + newStars;
        numRatings++;
        rating = rating / numRatings;
    }

    public String getID(){
        return ID;
    }

    public void setID(String mID){
        ID = mID;
    }

    public String getName(){
        return name;
    }

    public void setName(String mName){
        name = mName;
    }

    public String getBio(){
        return bio;
    }

    public void setBio(String mBio){
        bio = mBio;
    }

    public int getAge(){
        return age;
    }

    public void setAge(int mAge){
        age = mAge;
    }

    public String getGender(){
        return gender;
    }

    public void setGender(String mGender){
        gender = mGender;
    }

    public int getNumRatings(){
        return numRatings;
    }

    public void setNumRatings(int mNumRatings){
        numRatings = mNumRatings;
    }

    public Double getRating(){
        return rating;
    }

    public void setRating(Double mRating){
        rating = mRating;
    }

    public String IDtoString(){return ID;}

    public String nameToString(){return name;}

    public String ratingToString(){return rating + "";}

    public String numRatingsToString(){return numRatings+"";}

    public String bioToString(){return bio;}

    public String ageToString(){return age+"";}

    public String genderToString(){return gender;}

    public String toString(){
        String toBeReturned = IDtoString() + " ? ";
        toBeReturned = toBeReturned + nameToString() + ".?.";
        toBeReturned = toBeReturned + ratingToString() + ".?.";
        toBeReturned = toBeReturned + numRatingsToString() + ".?.";
        toBeReturned = toBeReturned + bioToString() + ".?.";
        toBeReturned = toBeReturned + ageToString() + ".?.";
        toBeReturned = toBeReturned + genderToString();
        return toBeReturned;
    }

}

