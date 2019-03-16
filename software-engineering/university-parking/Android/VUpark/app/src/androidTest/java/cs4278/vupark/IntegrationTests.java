package cs4278.vupark;

import android.content.Context;
import android.content.Intent;
import android.os.Looper;
import android.support.test.InstrumentationRegistry;
import android.support.test.runner.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import java.util.ArrayList;
import java.util.HashMap;

import static org.junit.Assert.*;

/**
 * Created by Danny on 12/10/2017.
 */
@RunWith(AndroidJUnit4.class)
public class IntegrationTests {
    @Test
    public void useAppContext() throws Exception {
        // Context of the app under test.
        Context appContext = InstrumentationRegistry.getTargetContext();

        assertEquals("cs4278.vupark", appContext.getPackageName());
        MapsActivity mapsActivity = new MapsActivity();
        Thread.sleep(2000);
        HashMap<String, Object> lotMap = mapsActivity.getLotMap();
        ArrayList<ParkingLot> mLots = mapsActivity.getmParkingLots();
        for(String lotKey: lotMap.keySet()) {
            HashMap<String, Object> lot = (HashMap) lotMap.get(lotKey);
            assertTrue(lot.containsKey("title"));
            String lotName = lot.get("title").toString();
            boolean inLots = false;
            for (ParkingLot curLot: mLots){
                if (curLot.getName() == lotName){
                    inLots = true;
                }
            }
            assertTrue(inLots);
        }
    }

}
