import matplotlib
import pathlib
import mne
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('Qt5Agg')

class DataProcessor:
    def __init__(self):
        self.raw = None
        self.events = None
        self.event_id = None
        self.raw_eeg = None
        self.raw_eeg_cropped = None
        self.raw_eeg_filtered = None

    def load_raw_data(self):
        sample_data_dir = pathlib.Path(mne.datasets.sample.data_path())
        raw_path = sample_data_dir / 'EEG' / 'sample' / 'sample_audvis_raw.fif'
        self.raw = mne.io.read_raw(raw_path)

    def plot_raw_data(self):
        self.raw.plot()

    def find_events(self):
        self.events = mne.find_events(self.raw)

    def define_event_id(self):
        self.event_id = {
            'Auditory/Left': 1,
            'Auditory/Right': 2,
            'Visual/Left': 3,
            'Visual/Right': 4,
            'Smiley': 5,
            'Button': 32
        }

    def count_button_events(self):
        num_button_events = len(self.events[self.events[:, 2] == 32])
        return num_button_events

    def plot_raw_data_with_events(self):
        self.raw.plot(events=self.events, event_id=self.event_id)

    def get_raw_info(self):
        info = self.raw.info
        return info

    def get_meas_date(self):
        meas_date = self.raw.info['meas_date']
        return meas_date

    def get_sampling_frequency(self):
        sfreq = self.raw.info['sfreq']
        return sfreq

    def get_bad_channels(self):
        bads = self.raw.info['bads']
        return bads

    def get_channel_names(self):
        ch_names = self.raw.info['ch_names'][:10]
        return ch_names

    def get_first_channel_info(self):
        first_channel_info = self.raw.info['chs'][0]
        return first_channel_info

    def plot_sensors(self, ch_type='eeg', kind=None):
        if kind == '3d':
            self.raw.plot_sensors(kind=kind, ch_type=ch_type)
        else:
            self.raw.plot_sensors(ch_type=ch_type)

    def add_bad_channel(self, channel):
        self.raw.info['bads'] += [channel]

    def preprocess_raw_eeg(self):
        self.raw_eeg = self.raw.copy().pick_types(meg=False, eeg=True, eog=True, exclude=[])

    def get_num_channels(self):
        num_channels = len(self.raw_eeg.ch_names)
        return num_channels

    def get_eeg_info(self):
        eeg_info = self.raw_eeg.info
        return eeg_info

    def crop_raw_eeg(self, tmax=100):
        self.raw_eeg_cropped = self.raw_eeg.copy().crop(tmax=tmax)

    def get_last_time_point(self):
        last_time_point = self.raw_eeg_cropped.times[-1]
        return last_time_point

    def filter_raw_eeg(self, l_freq=0.1, h_freq=40):
        self.raw_eeg_filtered = self.raw_eeg_cropped.filter(l_freq=l_freq, h_freq=h_freq)

    def load_data(self):
        self.raw_eeg_cropped.load_data()

    def plot_raw_eeg_with_events(self):
        self.raw_eeg_cropped.plot(events=self.events, event_id=self.event_id)

    def plot_psd(self):
        fig, ax = plt.subplots(2)
        self.raw_eeg_cropped.plot_psd(ax=ax[0], show=False)
        self.raw_eeg_filtered.plot_psd(ax=ax[1], show=False)
        ax[0].set_title('PSD before filtering')
        ax[1].set_title('PSD after filtering')
        ax[1].set_xlabel('Frequency (Hz)')
        fig.set_tight_layout(True)
        plt.show()

    def save_filtered_data(self, output_path):
        self.raw_eeg_filtered.save(output_path, overwrite=True)


data_processor = DataProcessor()
data_processor.load_raw_data()
data_processor.plot_raw_data()
data_processor.find_events()
data_processor.define_event_id()
data_processor.plot_raw_data_with_events()

info = data_processor.get_raw_info()
meas_date = data_processor.get_meas_date()
sfreq = data_processor.get_sampling_frequency()
bads = data_processor.get_bad_channels()
ch_names = data_processor.get_channel_names()
first_channel_info = data_processor.get_first_channel_info()

data_processor.plot_sensors(ch_type='eeg')
data_processor.plot_sensors(kind='3d', ch_type='eeg')

data_processor.add_bad_channel('EEG 051')
data_processor.plot_sensors(ch_type='eeg')

data_processor.preprocess_raw_eeg()
num_channels = data_processor.get_num_channels()
eeg_info = data_processor.get_eeg_info()
data_processor.plot_raw_eeg_with_events()

data_processor.crop_raw_eeg()
last_time_point = data_processor.get_last_time_point()
data_processor.filter_raw_eeg()
data_processor.load_data()
data_processor.plot_raw_eeg_with_events()
data_processor.plot_psd()

data_processor.save_filtered_data(pathlib.Path('out_data') / 'eeg_cropped_filt_raw.fif')

data_processor.load_raw_data()
data_processor.find_events()
data_processor.define_event_id()

ALLEEG = [data_processor.raw_eeg_filtered]

sRate = data_processor.get_sampling_frequency()
pNTS = data_processor.raw_eeg_cropped.n_times

winNoverlap = int((pNTS * 75) / 100)

pNFFT = 512

waitX = len(ALLEEG)

FFT = []

for ii in range(len(ALLEEG)):
    spectra = []
    freqs = []
    
    for kk in range(ALLEEG[ii].data.shape[0]):
        f, Pxx = welch(ALLEEG[ii].data[kk, :], fs=sRate, window='hann', nperseg=pNTS,
                       noverlap=winNoverlap, nfft=pNFFT, scaling='density')
        spectra.append(Pxx)
        freqs = f
    
    FFT.append(spectra)

FFT = np.array(FFT)

mean_spectrum = np.mean(FFT[0], axis=0)
plt.plot(freqs, 10 * np.log10(mean_spectrum), linewidth=3, color='red')
plt.xlim([1, 40])
plt.xlabel('Frequency [Hz]')
plt.ylabel('PSD [dB/Hz]')
plt.grid(True, which='both')
plt.minorticks_on()
plt.show()

for ii in range(len(FFT)):
    sum_power = np.zeros((FFT[ii].shape[1],))

    delta_power = np.zeros((FFT[ii].shape[1],))
    theta_power = np.zeros((FFT[ii].shape[1],))
    alpha_power = np.zeros((FFT[ii].shape[1],))
    beta_power = np.zeros((FFT[ii].shape[1],))

    rel_delta_power = np.zeros((FFT[ii].shape[1],))
    rel_theta_power = np.zeros((FFT[ii].shape[1],))
    rel_alpha_power = np.zeros((FFT[ii].shape[1],))
    rel_beta_power = np.zeros((FFT[ii].shape[1],))

    for kk in range(FFT[ii].shape[1]):
        sum_power[kk] = np.sum(FFT[ii][:, kk])

        delta_power[kk] = np.sum(FFT[ii][(freqs >= 1) & (freqs <= 3), kk])
        theta_power[kk] = np.sum(FFT[ii][(freqs >= 4) & (freqs <= 7), kk])
        alpha_power[kk] = np.sum(FFT[ii][(freqs >= 8) & (freqs <= 12), kk])
        beta_power[kk] = np.sum(FFT[ii][(freqs >= 13) & (freqs <= 30), kk])

        rel_delta_power[kk] = delta_power[kk] / sum_power[kk]
        rel_theta_power[kk] = theta_power[kk] / sum_power[kk]
        rel_alpha_power[kk] = alpha_power[kk] / sum_power[kk]
        rel_beta_power[kk] = beta_power[kk] / sum_power[kk]

    mean_delta_power = np.mean(delta_power)
    mean_theta_power = np.mean(theta_power)
    mean_alpha_power = np.mean(alpha_power)
    mean_beta_power = np.mean(beta_power)

    mean_rel_delta_power = np.mean(rel_delta_power)
    mean_rel_theta_power = np.mean(rel_theta_power)
    mean_rel_alpha_power = np.mean(rel_alpha_power)
    mean_rel_beta_power = np.mean(rel_beta_power)

    FFT[ii] = {
        'mean_delta_power': mean_delta_power,
        'mean_theta_power': mean_theta_power,
        'mean_alpha_power': mean_alpha_power,
        'mean_beta_power': mean_beta_power,
        'mean_rel_delta_power': mean_rel_delta_power,
        'mean_rel_theta_power': mean_rel_theta_power,
        'mean_rel_alpha_power': mean_rel_alpha_power,
        'mean_rel_beta_power': mean_rel_beta_power,
    }

class GuidelineChecker:
    def __init__(self, name):
        self.name = name
        self.status = None

delta = GuidelineChecker("delta")
theta = GuidelineChecker("theta")
alpha = GuidelineChecker("alpha")
beta = GuidelineChecker("beta")

# Delta Band (0.5-4 Hz)
if 0.5 <= FFT[ii]["Mean_rel_Delta"] <= 4 and 0.2 <= FFT[ii]["rel_delta"] <= 0.5 and 10 <= FFT[ii]["MeanDelta"] <= 50:
    delta.status = 'pass'
elif 0.5 <= FFT[ii]["Mean_rel_Delta"] <= 4 or 0.2 <= FFT[ii]["rel_delta"] <= 0.5 or 10 <= FFT[ii]["MeanDelta"] <= 50:
    delta.status = 'half pass'
else:
    delta.status = 'fail'

# Theta Band (4-8 Hz)
if 4 <= FFT[ii]["Mean_rel_Theta"] <= 8 and 0.05 <= FFT[ii]["rel_theta"] <= 0.2 and 10 <= FFT[ii]["MeanTheta"] <= 50:
    theta.status = 'pass'
elif 4 <= FFT[ii]["Mean_rel_Theta"] <= 8 or 0.05 <= FFT[ii]["rel_theta"] <= 0.2 or 10 <= FFT[ii]["MeanTheta"] <= 50:
    theta.status = 'half pass'
else:
    theta.status = 'fail'

# Alpha Band (8-13 Hz)
if 8 <= FFT[ii]["Mean_rel_Alpha"] <= 13 and 0.2 <= FFT[ii]["rel_alpha"] <= 0.5 and 10 <= FFT[ii]["MeanAlpha"] <= 50:
    alpha.status = 'pass'
elif 8 <= FFT[ii]["Mean_rel_Alpha"] <= 13 or 0.2 <= FFT[ii]["rel_alpha"] <= 0.5 or 10 <= FFT[ii]["MeanAlpha"] <= 50:
    alpha.status = 'half pass'
else:
    alpha.status = 'fail'

# Beta Band (13-30 Hz)
if 13 <= FFT[ii]["Mean_rel_Beta"] <= 30 and 0.05 <= FFT[ii]["rel_beta"] <= 0.2 and 10 <= FFT[ii]["MeanBeta"] <= 50:
    beta.status = 'pass'
elif 13 <= FFT[ii]["Mean_rel_Beta"] <= 30 or 0.05 <= FFT[ii]["rel_beta"] <= 0.2 or 10 <= FFT[ii]["MeanBeta"] <= 50:
    beta.status = 'half pass'
else:
    beta.status = 'fail'

ps = 0
hps = 0
f = 0

objects = [delta, theta, alpha, beta]

for i in objects:
    if i.status == 'pass':
        ps += + 1
    elif i.status == 'half pass':
        hps += + 1
    elif i.status == 'fail':
        f += + 1


if f > ps and hps:
    text = "There is a major abnormality in your EEG result. It would be best to contact a medical professional immediately."
elif hps > ps and hps:
    text = "You are healthy. However, it would be best to get an MRI test as soon as you can to prevent any risks."
elif ps > hps and f:
    text = "You are healthy!"
elif ps == hps:
    text = "You are healthy, but make sure you keep moving and eat less processed foods."
elif hps == f:
    text = "There isn't any risk at the moment, however, there is a large possibilitiy of one to occur. It is best to talk to a doctor."
elif ps == f:
    text = "Some parts of your results are abnormal, so it would be best for you to check with a doctor."
