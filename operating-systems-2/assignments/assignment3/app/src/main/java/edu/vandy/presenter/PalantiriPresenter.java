package edu.vandy.presenter;

import java.lang.ref.WeakReference;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.Phaser;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import android.app.VoiceInteractor;
import android.content.Intent;
import android.util.DebugUtils;
import android.util.Log;
import edu.vandy.MVP;
import edu.vandy.R;
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
 * GenericPresenter superclass and implements MVP.ProvidedPresenterOps
 * and MVP.RequiredModelOps so it can be created/managed by the
 * GenericPresenter framework.
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
    @SuppressWarnings("WeakerAccess")
    public WeakReference<MVP.RequiredViewOps> mView;

    /**
     * The list of BeingRunnables that will run concurrently in a
     * parallel stream.
     */
    private List<BeingRunnable> mBeingRunnables;

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
     * A Phaser entry barrier that ensures all background
     * threads start running at the same time.
     */
    private Phaser mEntryBarrier;

    /**
     * A CountDownLatch exit barrier that ensures the waiter thread
     * doesn't finish until all the BeingAsyncTasks finish.
     */
    private CountDownLatch mExitBarrier;

    /**
     * Default constructor that's needed by the GenericPresenter
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
        mView =
            new WeakReference<>(view);

        // Invoke the special onCreate() method in GenericPresenter,
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
                            R.string.toast_incorrect_arguments);

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
        getModel().onDestroy(isChangingConfigurations);
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
        /**
         * Reset all BeingRunnable static members.
         */
        BeingRunnable.reset();

        // Initialize the Palantiri.
        getModel().makePalantiri(Options.instance().numberOfPalantiri());

        // Store the number of Beings.
        int numberOfBeings = Options.instance().numberOfBeings();

        // Ensure the ForkJoin thread pool has the right number of
        // threads.
        // TODO -- you fill in here. - DONE
        // @@ Yikes, this isn't the right way to "ensure the forkjoin - DONE
        // thread pool has the right number of threads"!
        if((numberOfBeings+1) != ForkJoinPool.commonPool().getPoolSize()){
            System.setProperty("java.util.concurrent.ForkJoinPool.common.parallelism",
                    Integer.toString(numberOfBeings+1));
        }

        // Initialize an exit barrier to ensure the waiter thread
        // doesn't finish until all the BeingAsyncTasks finish.
        // TODO -- you fill in here. - DONE
        mExitBarrier = new CountDownLatch(Options.instance().numberOfBeings());
        // Initialize an entry barrier that ensures all background
        // threads start running at the same time.
        // TODO -- you fill in here. - DONE
        mEntryBarrier = new Phaser();
        // Show the Beings on the UI.
        mView.get().showBeings();

        // Show the palantiri on the UI.
        mView.get().showPalantiri();

        // Enable all Beings to start running the gazing logic, which
        // attempts to acquire a lease on a Palantir and gaze into it.
        beginBeingsGazing(numberOfBeings);

        // Wait for all Beings to finish gazing and then inform the
        // View layer that the simulation is done.
        waitForBeingsToFinishGazing();
    }

    /**
     * Run all Beings in a Parallel Stream, each of which attempts to
     * acquire a lease on a Palantir and gaze into it.
     *
     * @param beingCount Total number of Beings that want to gaze into
     *                   Palantiri.
     */
    private void beginBeingsGazing(int beingCount) {
        // Create a list of BeingRunnables of size beingCount that
        // will be run concurrently in a parallel stream.
        // TODO -- you fill in here. - DONE

        mBeingRunnables = Stream.generate(()->new BeingRunnable(this,mEntryBarrier,mExitBarrier))
                .limit(beingCount)
                .collect(toList());
        // Yikes, something important is missing here: - DONE
        new Thread(()->{
            mBeingRunnables.parallelStream().forEach(r->r.run());
        }).start();

    }

    /**
     * Wait for all Beings to finish gazing and then inform the View
     * layer that the simulation is done.
     */
    private void waitForBeingsToFinishGazing() {
        // Start a Java Thread that waits for all the Beings to finish
        // gazing and then calls mView.get().done() to inform the View
        // layer that the simulation is done.
        // TODO -- you fill in here. - DONE
        new Thread(()->{
            try {
                mExitBarrier.await();
                mView.get().done();
            } catch (InterruptedException e) {
                shutdown();
                e.printStackTrace();
            }
        }).start();
    }

    /**
     * This method is called if an unrecoverable exception occurs or
     * the user explicitly stops the simulation.  It shuts down all
     * the Threads and notifies the View layer that the simulation is
     * done.
     */
    @Override
    public void shutdown() {
        synchronized(this) {
            // Shutdown all the BeingRunnables.
            // TODO -- you fill in here, without using Thread.interrupt(). - DONE
            // @@ This is the wrong way to shut things down.  Look at BeingRunnables.. - DONE
            mBeingRunnables.get(0).shutdown();

            // Inform the user that we're shutting down the
            // simulation.
            mView.get().shutdownOccurred(mBeingRunnables.size());
        }
    }
}
