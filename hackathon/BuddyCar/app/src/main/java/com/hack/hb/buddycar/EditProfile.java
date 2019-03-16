package com.hack.hb.buddycar;

import android.content.Intent;
import android.provider.Settings;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Button;

import static com.hack.hb.buddycar.R.layout.activity_main;

/*
//How to get Android device ID
final String android_id = Settings.Secure.getString(getApplicationContext().getContentResolver(),
        Settings.Secure.ANDROID_ID);
*/

public class EditProfile extends AppCompatActivity {

    public final static String PROFILE = "com.hack.hb.buddycar.profile";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.content_edit_profile);


        //link to database
        final Database db = new Database(this);
        //Info Needed: String DriverID,String RiderID, String startCity, String endCity, String date,
        //Android device ID
        final String android_id = Settings.Secure.getString(getApplicationContext().getContentResolver(),
                Settings.Secure.ANDROID_ID);


        final Button submitButton = (Button) findViewById(R.id.button);
        submitButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                EditText txtName = (EditText) findViewById(R.id.name);
                EditText txtBio = (EditText) findViewById(R.id.bio);
                EditText txtAge = (EditText) findViewById(R.id.age);
                EditText txtGender = (EditText) findViewById(R.id.gender);
                int age = Integer.parseInt(txtAge.getText().toString());
                String name = txtName.getText().toString();
                String bio = txtBio.getText().toString();
                String gender = txtGender.getText().toString();

                Profile myProfile= new Profile(android_id, name, bio, age, gender);
                db.saveProfile(myProfile);

                CharSequence stringId = "Success! Your rating is " + myProfile.rating;
                Snackbar mySnackbar = Snackbar.make(findViewById(R.id.layout_id), stringId, 5);
                mySnackbar.show();

                Intent intent = new Intent(EditProfile.this, MainActivity.class);
                startActivity(intent);
            }
        });



    }
}

