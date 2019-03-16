package cs4278.vupark;

import android.graphics.Color;
import android.widget.Toast;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Polygon;
import com.google.android.gms.maps.model.PolygonOptions;

import java.util.List;
import java.util.Map;

/**
 * Created by Andrew on 11/14/2017.
 */

public class ParkingLot {
    private String name;

    // Google Maps drawn polygon + options (characteristics)
    private PolygonOptions polyOptions;
    private Polygon lot;

    private String permits;
    private List<Integer> availableSpots;

    ParkingLot(String name, PolygonOptions lotOptions) {
        this.name = name;
        this.polyOptions = lotOptions;
    }

    public String getName() {
        return name;
    }

    public String getPermits() {
        return permits;
    }

    public PolygonOptions getPolyOps(){
        return polyOptions;
    }

    public void setPolygon(Polygon poly){
        lot = poly;
    }

    public Polygon getPolygon() {
        return lot;
    }
}
