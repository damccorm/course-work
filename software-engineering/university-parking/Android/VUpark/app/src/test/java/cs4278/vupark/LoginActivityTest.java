package cs4278.vupark;

import android.content.Intent;

import org.junit.Test;

import java.util.ArrayList;
import java.util.HashMap;

import static org.junit.Assert.*;

/**
 * Created by Danny on 12/10/2017.
 */
public class LoginActivityTest {
    @Test
    public void tryLogin() throws Exception {
        LoginActivity l = new LoginActivity();
        HashMap<String, Object> userMap = new HashMap<>();
        HashMap<String, String> userInfoMap = new HashMap<>();
        userInfoMap.put("password", "dpassword");
        userMap.put("dmccormick", userInfoMap);
        assertEquals(l.tryLogin("dmccormick", "dpassword", userMap, null), 0);
        assertEquals(l.tryLogin("dmccormick", "notdpassword", userMap, null), -1);
        assertEquals(l.tryLogin("notdmccormick", "dpassword", userMap, null), -2);
    }

}