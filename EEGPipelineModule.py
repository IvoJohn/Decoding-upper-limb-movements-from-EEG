#!/usr/bin/env python
# coding: utf-8

# In[8]:


import mne

def read_gdf(data_path, preload=True, eog=[61,62,63], drop_channels=64, verbose=0):
    gdf_data = mne.io.read_raw_gdf(data_path, preload=preload, eog=eog, verbose=verbose)
    gdf_data.drop_channels(gdf_data.ch_names[drop_channels:])
    gdf_data.drop_channels(gdf_data.ch_names[:3])
    return gdf_data

def create_epochs(data, event_id, event_dictionary, tmin, tmax, preload=True, verbose=0):
    events, _ = mne.events_from_annotations(data, event_id=event_id, verbose=verbose)
    epochs = mne.Epochs(raw=data, events=events, event_id=event_dictionary, tmin=tmin, tmax=tmax, preload=preload, verbose=verbose)
    return epochs

def filtering_epochs(epochs, l_freq, h_freq, method='fft', verbose=0):
    epochs_filtered = epochs.filter(l_freq=l_freq, h_freq=h_freq, method=method, verbose=verbose)
    return epochs_filtered

def downsampling_epochs(epochs, sfreq, npad='auto'):
    epochs_resampled = epochs.resample(sfreq, npad=npad)
    return epochs_resampled

def epochs_to_dataframe(epochs, ch_drop=-3, save=False, path=''):
    epochs.drop_channels(epochs.ch_names[ch_drop:])
    data_frame = epochs.to_data_frame()
    if save:
        data_frame.to_csv(path, index=False)
    return data_frame

