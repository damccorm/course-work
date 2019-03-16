package edu.vandy.model;

import android.support.annotation.NonNull;
import android.util.Log;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Semaphore;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.concurrent.locks.StampedLock;

/**
 * Defines a mechanism that mediates concurrent access to a fixed
 * number of available Palantiri.  This class uses a "fair" Semaphore,
 * a HashMap, and synchronized statements to mediate concurrent access
 * to the Palantiri.  This class implements a variant of the "Pooling"
 * pattern (kircher-schwanninger.de/michael/publications/Pooling.pdf).
 */
public class PalantiriManager {
    /**
     * Debugging tag used by the Android logger.
     */
    protected final static String TAG = 
        PalantiriManager.class.getSimpleName();

    /**
     * A counting Semaphore that limits concurrent access to the fixed
     * number of available palantiri managed by the PalantiriManager.
     */
    private final Semaphore mAvailablePalantiri;

    /**
     * A map that associates the @a Palantiri key to the @a boolean
     * values that keep track of whether the key is available.
     */
    protected final HashMap<Palantir, Boolean> mPalantiriMap;

    /**
     * Java synchronizer that protects the Palantiri state.
     */
    // TODO -- you fill in here.  Ugrads use a ReaderWriterLock
    // synchronizer, whereas grad students must use a StampedLock.
    private final ReadWriteLock mReadWriteLock;

    /**
     * Constructor creates a PalantiriManager for the List of @a
     * palantiri passed as a parameter and initializes the fields.
     */
    public PalantiriManager(List<Palantir> palantiri) {
        // Create a new HashMap, iterate through the List of Palantiri
        // and initialize each key in the HashMap with "true" to
        // indicate it's available, and initialize the Semaphore to
        // use a "fair" implementation that mediates concurrent access
        // to the given Palantiri.
        // TODO -- you fill in here.
        mPalantiriMap = new HashMap<>();
        palantiri.forEach(p->mPalantiriMap.put(p,true));

        mAvailablePalantiri = new Semaphore(palantiri.size(),true);

        mReadWriteLock = new ReentrantReadWriteLock();
    }

    /**
     * Get a Palantir from the PalantiriManager, blocking until one is
     * available.
     */
    public Palantir acquire() {
        // Acquire the Semaphore uninterruptibly and then iterate
        // through the HashMap in a thread-safe manner to find the
        // first key in the HashMap whose value is "true" (which
        // indicates it's available for use).  Replace the value of
        // this key with "false" to indicate the Palantir isn't
        // available and then return that palantir to the client. 

        // TODO -- you fill in here.  Ugrads should use a downgrading - DONE
        // write lock implementation, whereas grads should use an
        // upgrading write lock implementation.

        // @@ You aren't implementing a downgrading write lock here. - DONE
        mAvailablePalantiri.acquireUninterruptibly();
        Lock lock = mReadWriteLock.writeLock();
        lock.lock();
        try{
            for(Palantir p: mPalantiriMap.keySet()){
                if(mPalantiriMap.replace(p,true,false)){
                    final Lock readLock = mReadWriteLock.readLock();
                    readLock.lock();
                    try{
                        lock.unlock();
                        return p;
                    }
                    finally {
                        lock = readLock;
                    }
                }
            }
        }
        finally {
            lock.unlock();
        }
        // This shouldn't happen, but we need this here to make the
        // compiler happy.
        return null;
    }

    /**
     * Returns the designated @code palantir to the PalantiriManager
     * so that it's available for other Threads to use.
     */
    public void release(final Palantir palantir) {
        // Put the "true" value back into HashMap for the palantir key
        // in a thread-safe manner using a write lock and release the
        // Semaphore if all works properly.
        // TODO -- you fill in here. - DONE
        mReadWriteLock.writeLock().lock();
        try{
            if(mPalantiriMap.replace(palantir,false,true)){
                mAvailablePalantiri.release();
            }
        }
        finally {
            mReadWriteLock.writeLock().unlock();
        }
    }

    /*
     * The following method is just intended for use by the regression
     * tests, not by applications.
     */

    /**
     * Returns the number of available permits on the semaphore.
     */
    public int availablePermits() {
        // TODO -- you fill in here. - DONE
        return mAvailablePalantiri.availablePermits();
    }
}
