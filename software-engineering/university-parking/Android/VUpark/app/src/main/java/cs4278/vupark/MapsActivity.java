package cs4278.vupark;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.AsyncTask;
import android.provider.ContactsContract;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ViewAnimator;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polygon;
import com.google.android.gms.maps.model.PolygonOptions;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.w3c.dom.Text;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
public class MapsActivity extends FragmentActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private String permit;
    private ArrayList<ParkingLot> mParkingLots = new ArrayList<>();
    private ArrayList<String> listItems = new ArrayList<>();
    private ArrayAdapter<String> listViewAdapter;
    private boolean mapReadyToBePainted = false;
    private HashMap<String, Object> lotMap;

    private Button park_button;
    private Button lots_button;
    private Button account_button;
    private ImageButton info_button;

    private ViewAnimator animator;
    private TextView lot_name;
    private Button reserve_button;
    private Button register_button;
    private ListView lot_listview;

    private ParkingLot curLot;
    private TextView lot_name_entry;
    private int curSpot;
    private int curSpotNumber;
    private String curSpotName;
    private TextView spot_entry;
    private String spot_cost = "FREE";
    private TextView cost_entry;

    private Button park_car_button;
    private Button cancel_reservation_button;

    private TextView confirmation_lot_name_entry;
    private TextView confirmation_spot_entry;
    private TextView confirmation_cost_entry;
    private Button leave_spot_button;
    private FirebaseDatabase database;

    private final int MY_PERMISSIONS_REQUEST_FINE_LOCATION = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);

        database = FirebaseDatabase.getInstance();
        DatabaseReference lotRef = database.getReference("lots");
        lotRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                lotMap = (HashMap)dataSnapshot.getValue();
                for(String lotKey: lotMap.keySet()){
                    HashMap<String, Object> lot = (HashMap)lotMap.get(lotKey);
                    String lotName = lot.get("title").toString();
                    HashMap<String, Double> polygon = (HashMap)lot.get("polygon");
                    double[][] coordinates = {
                            {polygon.get("x1"),
                                    polygon.get("y1")},
                            {polygon.get("x2"),
                                    polygon.get("y2")},
                            {polygon.get("x3"),
                                    polygon.get("y3")},
                            {polygon.get("x4"),
                                    polygon.get("y4")}};
                    mParkingLots.add(constructParkingLot(lotName, coordinates));
                }
                if(mapReadyToBePainted){
                    paintLots();
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                Toast.makeText(getApplicationContext(), "Failed to load lot info from database",
                        Toast.LENGTH_LONG).show();
            }
        });

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        // Obtain references to the buttons on the top toolbar
        park_button = findViewById(R.id.park_button);
        lots_button = findViewById(R.id.lots_button);
        account_button = findViewById(R.id.account_button);
        info_button = findViewById(R.id.help_button);

        // Obtain references to the components in the "Park" tab (the only tab implemented for MVP)

        // Reference to the animator allowing the bottom portion of the view to change
        animator = findViewById(R.id.animator);

        // References to components from the view after selecting a lot
        lot_name = findViewById(R.id.lot_name);
        reserve_button = findViewById(R.id.reserve_button);
        register_button = findViewById(R.id.register_button);
        lot_listview = findViewById(R.id.lot_list);

        // Tie functionality to buttons on view after selecting lot

        // Reserve spot button functionality
        reserve_button.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                // If the current spot is valid
                if(curSpot != -1) {
                    // update reserved lot, spot, and cost
                    lot_name_entry.setText(curLot.getName());
                    spot_entry.setText(curSpotName);
                    cost_entry.setText(spot_cost);

                    // move to the reserved view
                    animator.setDisplayedChild(2);

                    // update the database
                    setSpotOccupancy(curSpotNumber, true);
                }
            }
        });

        // Register button functionality (mark that you've parked)
        register_button.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(curSpot != -1) {
                    // update parked lot, spot, and cost
                    confirmation_lot_name_entry.setText(curLot.getName());
                    confirmation_spot_entry.setText(curSpotName);
                    confirmation_cost_entry.setText(spot_cost);

                    // move to the parked view
                    animator.setDisplayedChild(3);

                    // update the database to flag the car as parked
                    setSpotOccupancy(curSpotNumber, true);
                }
            }
        });

        // References to components from the view after reserving a spot
        park_car_button = findViewById(R.id.park_car_button);
        cancel_reservation_button = findViewById(R.id.cancel_reservation_button);
        lot_name_entry = findViewById(R.id.lot_name_entry);
        spot_entry = findViewById(R.id.spot_entry);
        cost_entry = findViewById(R.id.cost_entry);

        // Tie functionality to buttons on view after reserving a spot

        // Park button functionality
        park_car_button.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(curSpot != -1) {
                    // update parked lot, spot, and cost
                    confirmation_lot_name_entry.setText(curLot.getName());
                    confirmation_spot_entry.setText(curSpotName);
                    confirmation_cost_entry.setText(spot_cost);

                    // move to the parked view
                    animator.setDisplayedChild(3);

                    // update the database to flag the car as parked
                    setSpotOccupancy(curSpotNumber, true);
                }
            }
        });

        // Cancel reservation button functionality
        cancel_reservation_button.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Change the current spot to -1 (signifying no spot selected)
                curSpot = -1;

                // Switch to the default view, and clear the selection
                animator.setDisplayedChild(1);
                lot_listview.clearChoices();
                lot_listview.setAdapter(listViewAdapter);

                // Update the database, clearing the reservation
                setSpotOccupancy(curSpotNumber, false);
            }
        });

        // References to components from the view after marking that you have parked
        confirmation_lot_name_entry = findViewById(R.id.confirmation_lot_name_entry);
        confirmation_spot_entry = findViewById(R.id.confirmation_spot_entry);
        confirmation_cost_entry = findViewById(R.id.confirmation_cost_entry);
        leave_spot_button = findViewById(R.id.leave_spot_button);

        // Tie functionality to buttons on view after marking that you have parked
        leave_spot_button.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(curSpot != -1) {
                    // Change the current spot to -1 (signifying no spot selected)
                    curSpot = -1;

                    // Switch to the default view, and clear the selection
                    animator.setDisplayedChild(1);
                    lot_listview.clearChoices();
                    lot_listview.setSelection(-1);
                    lot_listview.setAdapter(listViewAdapter);

                    // Update the database, clearing the reservation
                    setSpotOccupancy(curSpotNumber, false);
                }
            }
        });

        Intent incomingIntent = getIntent();
        ArrayList<String> names = incomingIntent.getStringArrayListExtra("names");
        permit = incomingIntent.getStringExtra("permit");
        listViewAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, listItems);
        lot_listview.setAdapter(listViewAdapter);
        lot_listview.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                final String spotString = listItems.get(position);
                curSpotName = spotString;
                if(curSpot != position) {
                    curSpot = position;
                    listViewAdapter.notifyDataSetChanged();
                }

            }
        });
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // enable location marker if allowed, otherwise request permission
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED) {
            mMap.setMyLocationEnabled(true);
        } else {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    MY_PERMISSIONS_REQUEST_FINE_LOCATION);
        }

        // place the lots (polygons) onto the map
        mapReadyToBePainted = true;
        if (mParkingLots.size() > 0){
            paintLots();
            mapReadyToBePainted = false;
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST_FINE_LOCATION: {
                // if permission for fine location was granted
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    try {
                        // set location marker on map
                        mMap.setMyLocationEnabled(true);
                    } catch(SecurityException e) {
                        Log.println(Log.DEBUG, "MapsActivity", "Permissions failure.");
                    }
                }
                // otherwise, don't enable the marker -- not necessary for MVP
            }
        }
    }

    private ParkingLot constructParkingLot(String name, double[][] coordinates){
        PolygonOptions polygonOps = new PolygonOptions().clickable(true);

        // add the coordinates to the polygon
        for(double[] coordinate : coordinates) {
            polygonOps.add(new LatLng(coordinate[0], coordinate[1]));
        }
        // adjust the style of the polygon
        polygonOps.strokeWidth(3.5f).fillColor(Color.RED);

        return new ParkingLot(name, polygonOps);
    }

    private void paintLots(){

        for(int i = 0; i < mParkingLots.size(); i++){
            ParkingLot lot = mParkingLots.get(i);
            Polygon poly = mMap.addPolygon(lot.getPolyOps());
            lot.setPolygon(poly);
            poly.setTag(lot);
        }

        mMap.setOnPolygonClickListener(new GoogleMap.OnPolygonClickListener() {
            @Override
            public void onPolygonClick(Polygon polygon) {onPolygonClicked(polygon);}
        });

        // Move the camera to Terrace Place Garage
        LatLng terracePlaceGarage = new LatLng(36.150285, -86.799749);
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(terracePlaceGarage, 15.0f));
    }

    // public for testing purposes
    public void onPolygonClicked(Polygon polygon){
        // Update the current lot and lot name
        curLot = (ParkingLot)polygon.getTag();
        String curLotName = curLot.getName();
        lot_name.setText(curLotName);
        animator.setDisplayedChild(1);
        listViewAdapter.clear();

        // reset the current spot to unchosen (-1)
        curSpot = -1;

        // Fill in the list with the spots in the lot from the database
        for(String lotKey: lotMap.keySet()){
            HashMap<String, Object> lot = (HashMap)lotMap.get(lotKey);
            String lotName = lot.get("title").toString();
            if(curLotName.equals(lotName)){
                ArrayList<HashMap<String, Object>> spaceMap = (ArrayList<HashMap<String, Object>>)lot.get("spaces");
                for(HashMap<String, Object> spaceInfo: spaceMap){
                    if(!(Boolean)spaceInfo.get("occupied") && permit.equals(spaceInfo.get("permit").toString())){
                        curSpotNumber = Integer.parseInt(spaceInfo.get("name").toString());
                        listItems.add("Space " + spaceInfo.get("name").toString());
                    }
                }
            }
        }
    }

    private void setSpotOccupancy(int spaceNumber, boolean occupied){
        String curLotName = curLot.getName();
        DatabaseReference ref1 = database.getReference("lots");
        for(String lotKey: lotMap.keySet()){
            HashMap<String, Object> lot = (HashMap)lotMap.get(lotKey);
            String lotName = lot.get("title").toString();
            if(curLotName.equals(lotName)){
                DatabaseReference ref2 = ref1.child(lotKey).child("spaces");
                ArrayList<HashMap<String, Object>> spaceMap = (ArrayList<HashMap<String, Object>>)lot.get("spaces");
                for(int i = 0; i < spaceMap.size(); i++){
                    HashMap<String, Object> spaceInfo = spaceMap.get(i);
                    int num = Integer.parseInt(spaceInfo.get("name").toString());
                    if(num == spaceNumber){
                        spaceInfo.put("occupied", occupied);
                        spaceMap.set(i, spaceInfo);
                    }
                }
                ref2.setValue(spaceMap);
            }
        }

    }

    @Override
    protected void onDestroy() {
        // clear any reservation before being destroyed
        setSpotOccupancy(curSpotNumber, false);
        super.onDestroy();
    }

    public HashMap<String, Object> getLotMap(){
        //Exists for testing purposes
        return lotMap;
    }

    public ArrayList<ParkingLot> getmParkingLots(){
        //Exists for testing purposes
        return mParkingLots;
    }

    public int getCurSpot() {
        // Exists for testing purposes
        return curSpot;
    }

    public TextView getLotName() {
        // Exists for testing purposes
        return lot_name;
    }

    public ViewAnimator getAnimator() {
        // Exists for testing purposes
        return animator;
    }
}
