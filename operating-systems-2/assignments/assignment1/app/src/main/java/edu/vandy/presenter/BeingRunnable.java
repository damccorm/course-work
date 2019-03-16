package edu.vandy.presenter;

import android.util.Log;

import java.util.concurrent.atomic.AtomicInteger;

import edu.vandy.common.Utils;
import edu.vandy.model.Palantir;
import edu.vandy.utils.Options;

/**
 * This class implements the gazing logic of a BeingThread.  Since
 * Beings are identified by their indices in the list they must be
 * supplied with an index when created.
 */
public class BeingRunnable
       implements Runnable {
    /**
     * Used for Android debugging.
     */
    private final static String TAG = 
        BeingRunnable.class.getName();

    /**
     * Reference to the enclosing Presenter.
     */
    private final PalantiriPresenter mPresenter;

    /**
     * The number of Beings that currently have a Palantir.  Initially
     * set to 0.
     */
    private static AtomicInteger mGazingThreads =
        new AtomicInteger(0);

    /**
     * The ID of this Being.
     */
    private final int mBeingId;

    /**
     * The number of total Beings from 0 to n - 1;
     */
    private static AtomicInteger mBeingCount =
        new AtomicInteger(0);

    /**
     * Constructor initializes the field.
     */
    BeingRunnable(PalantiriPresenter presenter) {
        mPresenter = presenter;
        mBeingId = mBeingCount.getAndIncrement();
    }

    /**
     * Return the being Id, which is transformed to fit within the
     * total number of Beings.
     */
    private int getBeingId() {
        // Use the modulus operator to keep the being Id within the
        // necessary array bounds.
        return mBeingId % Options.instance().numberOfBeings();
    }

    /**
     * Run the loop that performs the Being gazing logic.
     */
    @Override
    public void run() {
        // Don't start the threads immediately.
        Utils.pauseThread(500);

        // Define local variables.
        int i = 0;

        // Gaze at a palantir the designated number of times.
        for (;
             i < Options.instance().gazingIterations();
             ++i) {
            if (!gazeIntoPalantir(getBeingId(),
                                  Thread.currentThread().getName()))
                break;
        }

        Log.d(TAG,
              "Being "
              + getBeingId()
              + " has finished "
              + i 
              + " of its "
              + Options.instance().gazingIterations()
              + " gazing iterations");
    }

    /**
     * Perform the Being gazing logic.
     *
     * @return True if gazing completed normally, else false.
     */
    private boolean gazeIntoPalantir(int beingId,
                                     String threadName) {
        // Return if PalantiriPresenter instructs us to stop gazing.
        // TODO -- replace "false" with the appropriate call. - DONE
        if (Thread.interrupted()) {
            Log.d(TAG,
                    "Thread.interrupted() is true for Being "
                            + beingId
                            + " in Thread "
                            + threadName);

            // If we've been instructed to stop gazing, notify the UI
            // and return gracefully.
            mPresenter.mView.get().threadShutdown(beingId);
            return false;
        } else {
            Palantir palantir = null;

            try {
                // Show that we're waiting on the screen.
                mPresenter.mView.get().markWaiting(beingId);

                // Get a Palantir from the Model layer - this call can
                // block if there are no available Palantiri.
                // TODO -- you fill in here. - DONE
                palantir = mPresenter.getModel().acquirePalantir();

                // Do a sanity check.
                if (palantir == null) {
                    Log.d(TAG,
                            "Palantir was null in for Being "
                                    + beingId
                                    + " in thread "
                                    + threadName);
                    return false;
                }

                // Make sure we were supposed to get a Palantir.
                if (!incrementGazingCountAndCheck(beingId,
                        palantir))
                    return false;

                // Mark it as used on the screen.
                mPresenter.mView.get().markUsed(palantir.getId());

                // Show that we're gazing on the screen.
                mPresenter.mView.get().markGazing(beingId);

                // Gaze at my Palantir for the alloted time.
                palantir.gaze();

                // Show that we're no longer gazing.
                mPresenter.mView.get().markIdle(beingId);
                Utils.pauseThread(500);

                // Mark the Palantir as being free.
                mPresenter.mView.get().markFree(palantir.getId());
                Utils.pauseThread(500);

                // Tell the double-checker that we're about to give up
                // a Palantir.
                decrementGazingCount();
            } catch (Exception e) {
                Log.d(TAG,
                        "Exception caught in Being "
                                + beingId);

                // If we're interrupted by an exception, notify the UI
                // and return gracefully.
                mPresenter.mView.get().threadShutdown(beingId);
                return false;
            } finally {
                // Return the Palantir back to PalantiriManager in the
                // Model layer.
                // TODO -- you fill in here. - DONE
                mPresenter.getModel().releasePalantir(palantir);
            }
            return true;
        }
    }

    /**
     * This method is called each time a BeingThread acquires a
     * Palantir, so it is called concurrently from different threads.
     * This method increments the number of threads gazing and checks
     * that the number of threads gazing does not exceed the number of
     * Palantiri in the simulation using an AtomicLong object
     * instantiated above (mGazingThreads).  If the number of gazing
     * threads exceeds the number of Palantiri, this thread will call
     * shutdown and return false.
     * 
     * @param beingId
     *         The Id of the current Being.
     * @param palantir
     *         The Palantir that was just acquired.
     *         
     * @return false if the number of gazing threads is greater
     *         than the number of Palantiri, otherwise true.
     */
    private boolean incrementGazingCountAndCheck(int beingId,
                                                 Palantir palantir) {
        // TODO - You fill in here.
        // @@ Something(s) important are missing here!  Read the spec above..
        // @@ Fixed by adding the shutdown call in else statement
        if(mGazingThreads.incrementAndGet() <= mBeingCount.get()){
            return true;
        }
        else{
            //Shutdown if there has been an error and there are more
            //gazers than Palantiri
            mPresenter.shutdown();
            return false;
        }
    }

    /**
     * This method is called each time a Being is about to release a
     * Palantir.  It should simply decrement the number of gazing
     * threads in mGazingThreads.
     */
    private void decrementGazingCount() {
        // TODO - You fill in here.
        mGazingThreads.decrementAndGet();
    }
}
