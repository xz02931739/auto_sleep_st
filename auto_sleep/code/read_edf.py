import pyedflib
import numpy as np
from scipy.interpolate import interp1d


def changing_fs(raw_signal,raw_sr,new_sr):
    
    new_signal_len = int((len(raw_signal)//raw_sr)*new_sr)
    x = np.arange(len(raw_signal))
    # y = raw_signal
    x_new = np.linspace(0,len(raw_signal)-1,new_signal_len)
    f = interp1d(x, raw_signal, kind='cubic')
    new_signal = f(x_new)
    
    return new_signal


def read_edfrecord(edffile): #the value of length is only related to respiratory signals

    # EEG_channels = ['C4']
    # EOG_channels = ['E1','E2']
    # air_channels = ['Nasal Pressure','Airflow']
    # ECG_channels = ['ECG2']
    channels = ['Nasal Pressure','Airflow','E1','E2','C4','ECG2']
    f = pyedflib.EdfReader(edffile)
    # signal_duration =f.getFileDuration()
    signal_labels = f.getSignalLabels()
 
    assert len(list(set(channels)&set(signal_labels))) == 6
          
    #extracting SLeep staging signals
    i = 0
    sig = [None]*6
    new_sr = 200           
    for chan in channels:
        chan_index = signal_labels.index(chan)            
        sig[i] = f.readSignal(chan_index)
        channel_sf = f.getSampleFrequency(chan_index)
        if channel_sf != new_sr:
            sig[i] = changing_fs(sig[i], channel_sf, new_sr)
        i += 1
             
    sig = np.array(sig)         
    
    #spliting signals
    #time_win = 60
    epoch_len = new_sr*30
    num_epochs = sig.shape[1]//epoch_len
    sig_eff = sig[:,:int(num_epochs*epoch_len)]
    #normalizing the whole signal
    
    # SS_sig_eff = normalize(SS_sig_eff,axis=1,norm='max')
    # Res_sig_eff = normalize(Res_sig_eff,axis=1,norm='max')
    samples = np.array(np.split(sig_eff,num_epochs,axis=1)) 
    new_samples = []
    for idx in range(len(samples)-1):                                                                
        sample_before = samples[idx]
        sample_after = samples[idx+1]
        joint_sample = np.concatenate((sample_before,sample_after),axis=1)
        new_samples.append(joint_sample)
                       
    new_samples = np.array(new_samples)
    
    return new_samples
    