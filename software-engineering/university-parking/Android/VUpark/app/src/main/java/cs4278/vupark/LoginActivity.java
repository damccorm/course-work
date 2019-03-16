package cs4278.vupark;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.maps.model.PolygonOptions;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.HashMap;

public class LoginActivity extends AppCompatActivity {

    private EditText mVUnetid;
    private EditText mPassword;
    private Button mLoginButton;
    private HashMap<String, Object> userMap = new HashMap<>();
    private FirebaseDatabase database;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // obtain references to the EditTexts to input username and password
        mVUnetid = findViewById(R.id.vunetid_text);
        mPassword = findViewById(R.id.password_text);

        // obtain references to the login button
        mLoginButton = findViewById(R.id.login_button);
        final Intent intent = new Intent(this, MapsActivity.class);

        //Click listener for login button. Checks if valid username/password, if not displays
        //error message.
        mLoginButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View view) {
                        String username = mVUnetid.getText().toString();
                        String password = mPassword.getText().toString();
                        int result = tryLogin(username, password, userMap, intent);
                        if (result == -1){
                            Toast.makeText(getApplicationContext(), "Invalid password",
                                    Toast.LENGTH_LONG).show();
                        }
                        else if(result == -2){
                            Toast.makeText(getApplicationContext(), "Invalid username",
                                    Toast.LENGTH_LONG).show();
                        }
                    }
                }
        );

        //Connects to Firebase database and automatically fills userMap with the data.
        database = FirebaseDatabase.getInstance();
        DatabaseReference userRef = database.getReference("users");
        userRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                userMap = (HashMap)dataSnapshot.getValue();
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                Toast.makeText(getApplicationContext(), "Failed to load user info from database",
                        Toast.LENGTH_LONG).show();
            }
        });
    }

    public int tryLogin(String username, String password, HashMap<String, Object> mUserMap, Intent intent) {
        //Function to try to login user. If successful, starts new activity, if not returns error
        //code (-2 if user doesn't exist, -1 if password is wrong).
        if (mUserMap.containsKey(username)) {
            HashMap<String, String> user_info = (HashMap) mUserMap.get(username);
            if (user_info.get("password").equals(password)) {
                if (intent != null) {
                    intent.putExtra("username", username);
                    intent.putExtra("permit", user_info.get("permit"));
                    startActivity(intent);
                }
                return 0;
            } else {
                return -1;
            }
        } else {
            return -2;
        }
    }
}
