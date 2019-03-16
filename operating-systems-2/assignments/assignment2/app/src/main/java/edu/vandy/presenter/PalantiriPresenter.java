package edu.vandy.presenter;

import java.lang.ref.WeakReference;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

import android.content.Intent;
import android.util.Log;
import edu.vandy.MVP;
import edu.vandy.common.GenericPresenter;
import edu.vandy.common.Utils;
import edu.vandy.model.PalantiriModel;
import edu.vandy.utils.Options;
import edu.vandy.view.DotArrayAdapter.DotColor;

import static java.util.stream.Collectors.toList;

/**
 * This class manages the Palantiri simulation.  The simulation begins
 * in the start() method, which is called by the UI Thread and is
 * provided a reference to MVP.RequiredViewOps, which is used to
 * manipulate the UI.  The Options singleton contains the number of
 * beings to simulate and the number of palantiri to simulate.
 * 
 * The simulation should run as follows: the correct number of
 * palantiri should be instantiated and added to the LeasePool in the
 * Model layer.  A Java thread should be created for each Being.  Each
 * Being thread should attempt to acquire a palantir a certain number
 * of times (defined via the GAZE_ATTEMPTS constant below).  As this
 * is happening, Being threads should call the appropriate methods in
 * MVP.RequiredViewOps to demonstrate which palantiri are being used
 * and which Beings currently own a palantir.
 *
 * This class plays the "Presenter" role in the Model-View-Presenter
 * (MVP) pattern by acting upon the Model and the View, i.e., it
 * retrieves data from the Model (e.g., PalantiriModel) and formats it
 * for display in the View (e.g., PalantiriActivity).  It expends the
 * GenericModel superclass and implements MVP.ProvidedPresenterOps and
 * MVP.RequiredModelOps so it can be created/managed by the
 * GenericModel framework.
 */
public class PalantiriPresenter
       extends GenericPresenter<MVP.RequiredPresenterOps,
                                MVP.ProvidedModelOps,
                                PalantiriModel>
       implements MVP.ProvidedPresenterOps, 
                  MVP.RequiredPresenterOps {
    /**
     * Used for Android debugging.
     */
    private final static String TAG = 
        PalantiriPresenter.class.getName();

    /**
     * Keeps track of whether a runtime configuration change ever
     * occurred.
     */
    private boolean mConfigurationChangeOccurred;

    /**
     * Used to simplify actions performed by the UI, so the
     * application doesn't have to worry about it.
     */
    public WeakReference<MVP.RequiredViewOps> mView;

    /**
     * The list of Beings (implemented as concurrently executing Java
     * Threads) that are attempting to acquire Palantiri for gazing.
     */
    private List<BeingAsyncTask> mBeingsAsyncTasks;

    /**
     * Tracks whether a simulation is currently running or not.
     */
    private boolean mRunning = false;

    /**
     * This List keeps track of how many palantiri we have and whether
     * they're in use or not.
     */
    private List<DotColor> mPalantiriColors =
        new ArrayList<>();
	
    /**
     * This List keeps track of how many beings we have and whether
     * they're gazing or not.
     */
    private List<DotColor> mBeingsColors =
        new ArrayList<>();

    /**
     * A CyclicBarrier entry barrier that ensures all background
     * threads start running at the same time.
     */
    private CyclicBarrier mEntryBarrier;

    /**
     * A CountDownLatch exit barrier that ensures the waiter thread
     * doesn't finish until all the BeingAsyncTasks finish.
     */
    private CountDownLatch mExitBarrier;

    /**
     * A ThreadFactory object that spawns an appropriately named
     * Thread for each Being.
     */
    private ThreadFactory mThreadFactory = (r->{return new Thread(r);});
        // TODO -- you fill in here by replacing "return null" with a - DONE
        // ThreadFactory implementation that creates a new Thread each
        // time it's called.
        // @@ Please use a lambda here! - DONE

    /**
     * Default constructor that's needed by the GenericActivity
     * framework.
     */
    public PalantiriPresenter() {
    }

    /**
     * Hook method called when a new instance of PalantiriPresenter is
     * created.  One time initialization code goes here, e.g., storing
     * a WeakReference to the View layer and initializing the Model
     * layer.
     * 
     * @param view
     *            A reference to the View layer.
     */
    @Override
    public void onCreate(MVP.RequiredViewOps view) {
        // Set the WeakReference.
        mView = new WeakReference<>(view);

        // Invoke the special onCreate() method in GenericModel,
        // passing in the PalantiriModel class to instantiate/manage
        // and "this" to provide this MVP.RequiredModelOps instance.
        super.onCreate(PalantiriModel.class,
                       this);

        // Get the intent used to start the Activity.
        final Intent intent = view.getIntent();

        // Initialize the Options singleton using the extras contained
        // in the intent.
        if (!Options.instance().parseArgs(view.getActivityContext(),
                                          makeArgv(intent)))
            Utils.showToast(view.getActivityContext(),
                            "Arguments were incorrect");

        // A runtime configuration change has not yet occurred.
        mConfigurationChangeOccurred = false;
    }

    /**
     * Hook method dispatched by the GenericActivity framework to
     * initialize the PalantiriPresenter object after it's been
     * created.
     *
     * @param view         
     *          The currently active MVP.RequiredViewOps.
     */
    @Override
    public void onConfigurationChange(MVP.RequiredViewOps view) {
        Log.d(TAG,
              "onConfigurationChange() called");

        // Reset the WeakReference.
        mView =
            new WeakReference<>(view);

        // A runtime configuration change occurred.
        mConfigurationChangeOccurred = true;
    }

    /**
     * Hook method called to shutdown the Model layer.
     *
     * @param isChangingConfigurations
     *        True if a runtime configuration triggered the onDestroy() call.
     */
    @Override
    public void onDestroy(boolean isChangingConfigurations) {
        // Destroy the model.
        // getModel().onDestroy(isChangingConfigurations);
    }

    /**
     * Returns true if a configuration change has ever occurred, else
     * false.
     */
    @Override
    public boolean configurationChangeOccurred() {
        return mConfigurationChangeOccurred;
    }

    /**
     * Factory method that creates an Argv string containing the
     * options.
     */
    private String[] makeArgv(Intent intent) {
        // Create the list of arguments to pass to the Options
        // singleton.
        return new String[]{
                "-b", // Number of Being threads.
                intent.getStringExtra("BEINGS"),
                "-p", // Number of Palantiri.
                intent.getStringExtra("PALANTIRI"),
                "-i", // Gazing iterations.
                intent.getStringExtra("GAZING_ITERATIONS"),
        };
    }

    /**
     * Returns true if the simulation is currently running, else false.
     */
    public boolean isRunning() {
        return mRunning;
    }

    /**
     * Sets whether the simulation is currently running or not.
     */
    public void setRunning(boolean running) {
        mRunning = running;
    }

    /**
     * Returns the List of Palantiri and whether they are gazing.
     */
    public List<DotColor> getPalantiriColors() {
        return mPalantiriColors;
    }

    /**
     * Returns the List of Beings and whether they are gazing.
     */
    public List<DotColor> getBeingsColors() {
        return mBeingsColors;
    }

    /**
     * This method is called if an unrecoverable exception occurs or
     * the user explicitly stops the simulation.  It interrupts all
     * the other threads and notifies the UI.
     */
    @Override
    public void shutdown() {
        synchronized(this) {
            // Inform the user that we're shutting down the
            // simulation.
            mView.get().shutdownOccurred(mBeingsAsyncTasks.size());

            /// Cancel all the BeingAsyncTasks.
            // TODO - you fill in here. - DONE
            // @@ Please use the forEach stream operator here. - DONE
            //Cancel and interrupt the tasks
            mBeingsAsyncTasks.stream().forEach(t->t.cancel(true));
        }
    }

    /**
     * This method is called when the user asks to start the
     * simulation in the context of the main UI Thread.  It creates
     * the designated number of Palantiri and adds them to the
     * PalantiriManager.  It then creates a Thread for each Being and
     * has each Being attempt to acquire a Palantir for gazing,
     * mediated by the PalantiriManager.  The Threads call methods
     * from the MVP.RequiredViewOps interface to visualize what is
     * happening to the user.
     **/
    @Override
    public void start() {
        // Initialize the Palantiri.
        getModel().makePalantiri(Options.instance().numberOfPalantiri());

        // Show the Beings on the UI.
        mView.get().showBeings();

        // Show the palantiri on the UI.
        mView.get().showPalantiri();

        // Initialize an exit barrier to ensure the waiter thread
        // doesn't finish until all the BeingAsyncTasks finish.
        // TODO -- you fill in here. - DONE
        mExitBarrier = new CountDownLatch(Options.instance().numberOfBeings());

        // Initialize an entry barrier that ensures all background
        // threads start running at the same time.
        // Number of beings+1 to account for this thread
        // TODO -- DONE
        mEntryBarrier = new CyclicBarrier(Options.instance().numberOfBeings() + 1);

        // Create and execute an AsyncBeingAsyncTask for each Being.
        beginBeingTasksGazing(Options.instance().numberOfBeings());

        // Spawn a thread that waits for all the Being threads to
        // finish.
        waitForBeingTasksToFinishGazing();
    }

    /**
     * Create a List of Threads that will be used to represent the
     * Beings in this simulation.  Each Thread is passed a
     * BeingRunnable parameter that takes the index of the Being in
     * the list as a parameter.
     * 
     * @param beingCount
     *            Number of Being Threads to create.
     */
    private void beginBeingTasksGazing(int beingCount) {
        // Use Java 8 Streams to generate beingCount number of
        // BeingAsyncTasks that are stored in a List and then execute
        // all these tasks in a custom ThreadPoolExecutor that
        // contains (1) a fixed-size pool of Threads corresponding to
        // the number of Beings, (2) a LinkedBlockingQueue, and (3)
        // the ThreadFactory instance.
        // TODO - You fill in here. - DONE
        //Create beingCount AsyncTasks and put them in mBeingAsyncTasks
        mBeingsAsyncTasks = Stream
                .generate(()->new BeingAsyncTask(mEntryBarrier,mExitBarrier))
                .limit(beingCount)
                .collect(toList());

        //Create the ThreadPoolExecutor and execute the AsyncTasks on it
        ThreadPoolExecutor myExecutor = new ThreadPoolExecutor(beingCount,
                beingCount,
                // @@ This is the wrong value to pass here: - DONE
                0,
                TimeUnit.MILLISECONDS,
                new LinkedBlockingQueue<>(),
                mThreadFactory);
        // @@ Please use the forEach stream operator here. - DONE
        mBeingsAsyncTasks.stream().forEach(t->t.executeOnExecutor(myExecutor,this));
    }

    /**
     * Spawn a thread to wait for all the Being threads to finish.
     */
    private void waitForBeingTasksToFinishGazing() {
        // Create/start a waiter thread that uses mExitBarrier to wait
        // for all the BeingAsyncTasks to finish.  After they are all
        // finished then tell the UI thread this simulation is done.
        new Thread(() -> {
            try {
                // Let all the BeingAsyncTasks start gazing.
                // TODO -- you fill in here. - DONE
                mEntryBarrier.await();

                // Wait for all BeingAsyncTasks to stop gazing.
                // TODO -- you fill in here. - DONE
                mExitBarrier.await();
            } catch (Exception e) {
                Log.d(TAG,
                      "joinBeingAsyncTasks() received exception");
                // If we get interrupted while waiting, stop
                // everything.
                shutdown();
            } finally {
                // Tell the UI thread this simulation is done.
                mView.get().done();
            }
        }).start();
    }
}
