# EEG Smart Glasses

Welcome to the repository for the Smart Glasses with EEG Reading and Health Feedback! These smart glasses analyze the electrical signals of the user's brain and display health feedback on the lens, enabling effortless and regular monitoring of brain conditions, thus facilitating early detection of neural diseases and strokes. By integrating the EEG system into glasses, I aim to reduce the invasiveness, time consumption, and cost associated with traditional EEG procedures.

### Table of Contents
1. The Research
3. Design and Modelling
5. The Code

### The Research
The foundation of this project is based on extensive research in the fields of neurology, EEG technology, and wearable devices. A in-depth literature review was conducted to understand the principles of EEG signals and how they correlate with neural health. This research helped identify the most relevant EEG biomarkers and their significance in diagnosing various neurological conditions. The study of existing EEG devices and wearable technologies provided insights into the limitations of current solutions. I recognized the need for a non-invasive, comfortable, and user-friendly EEG monitoring system that could seamlessly integrate into daily life without compromising data accuracy.

#### Electrode Placement
To ensure optimal daily monitoring, the strategic use of only two electrodes placed on the T7 (left temporal) and T8 (right temporal) areas is preferred. This specific electrode placement is scientifically advantageous as it minimizes interference from the positive-charged eyeball artifacts, which can distort EEG readings. By focusing on these lateral temporal regions, the EEG signals can be more accurately captured, providing valuable insights into the brain's electrical activity and facilitating more precise neurological assessments.

#### Electrode Type
The best electrodes for EEG (Electroencephalography) are typically silver/silver chloride (Ag/AgCl) electrodes. These electrodes offer low impedance, stable and reliable recordings, and minimal skin irritation. They provide accurate signal acquisition and are widely used in EEG research and clinical applications due to their excellent conductivity properties and biocompatibility with the skin.

#### Best Solution
Developing smart glasses with EEG detection capabilities is an ideal approach due to the high prevalence of neural disease patients among seniors, constituting 80% of the affected population. Leveraging the fact that an impressive 92% of seniors already wear glasses, incorporating EEG technology into these smart eyewear devices offers a non-intrusive and convenient means of monitoring brain activity, facilitating early detection and personalized management of neurological conditions in this vulnerable demographic.

### Design and Modelling
A 3D modeling software named Blender was utilized to design the glasses, considering ergonomic factors and feedback from potential users. Multiple iterations of the 3D model were developed and tested to ensure optimal fit and comfort for various head shapes and sizes. An aesthetic look was considered, while still in incorporating places for wires, circuit boards and holes for electrodes to read the EEG of the user.

### The Code

#### MNE Python
MNE-Python is a powerful and versatile Python library designed for the analysis of neurophysiological data, particularly EEG (Electroencephalography) and MEG (Magnetoencephalography) data. MNE stands for "Magnetoencephalography and Electroencephalography," highlighting its focus on these two neuroimaging modalities. The library provides a comprehensive set of tools for processing, visualization, and analysis of brain signals, enabling researchers and neuroscientists to explore and interpret brain activity in various experimental paradigms. MNE-Python supports data loading from different file formats, event handling, artifact removal, frequency and time-frequency analysis, source localization, connectivity analysis, and much more. Its integration with other Python libraries such as NumPy, SciPy, and Matplotlib enhances its capabilities for scientific computing and data visualization. MNE-Python has become a widely adopted tool in the neuroimaging community due to its user-friendly interface, rich functionality, and extensive documentation, making it a valuable asset for advancing our understanding of brain function and cognition.

#### File 1 (eegcode.py):

1. Import Libraries:
- matplotlib: A plotting library for Python.
- pathlib: A library for handling file paths.
- mne: A library for processing EEG and MEG data.
- numpy: A library for numerical operations.
- matplotlib.pyplot: A module for creating plots with Matplotlib.
2. Class Definition DataProcessor:
- This class is defined to process EEG data and perform various operations on it.
- The class has several methods for loading raw EEG data, plotting the raw data, finding events, defining event IDs, counting button events, and more.
3. Class GuidelineChecker:
- This class is defined to check EEG frequency bands (delta, theta, alpha, beta) against certain criteria and assign a status to each band based on the evaluation.
4. data_processor Object Creation and Data Processing:
- An instance of the DataProcessor class is created, and various methods are called to process the EEG data step by step.
- EEG data is loaded, plotted, events are found, event IDs are defined, and the raw data is plotted with events.

5. EEG Data Preprocessing:
- The raw EEG data is preprocessed by copying the relevant channels (MEG, EEG, EOG) and excluding any bad channels.
6. EEG Data Filtering:
- The preprocessed EEG data is filtered to keep frequencies between 0.1 Hz and 40 Hz.
7. Plotting Power Spectral Density (PSD):
- The PSD is computed and plotted for the filtered EEG data before and after filtering.
8. Saving Filtered Data:
- The filtered EEG data is saved to a file named 'eeg_cropped_filt_raw.fif'.
9. EEG Data Analysis:
- Some EEG data analysis is performed using Welch's method to compute the power in different frequency bands (delta, theta, alpha, beta).
10. Class GuidelineChecker Usage:
- The GuidelineChecker class is used to evaluate the EEG data against specific frequency band criteria and assign a status (pass, half pass, fail) to each band.
11. Result Text Assignment:
- A text result is determined based on the number of passed, half-passed, and failed criteria, and it is assigned to the result variable.

#### File 2 (main.py):

1. Import Libraries:
- board: A library to access board pins on a microcontroller.
- busio: A library for handling communication buses like I2C.
- adafruit_ssd1306: A library for driving SSD1306-based OLED displays.
- adafruit_display_text: A library for displaying text on Adafruit displays.
- adafruit_bitmap_font: A library for loading bitmap fonts.
2. OLED Display Setup:
- The code sets up an OLED display with a width of 96 pixels and a height of 16 pixels using the SSD1306_I2C class.
3. main() Function:
- The main() function initializes the display, loads a font, creates a display group, adds a text label to the group, and shows the group on the OLED display.
- It prints the result, reads analog input from pin A0, and waits for 0.1 seconds.
4. Infinite Loop:
- The main() function is called in an infinite loop to continuously update and display the text result and read the analog input.

Overall, the code processes EEG data, filters it, analyzes it to compute power in different frequency bands, and provides a result based on the evaluation of the frequency bands. The result is then displayed on an OLED screen along with analog input readings from the microcontroller.

###### For any inquiries, feel free to contact me at lakyvasu2008@gmail.com!
