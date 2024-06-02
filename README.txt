This folder contains the sources and scripts for the "Automatic Language Identification
Based on Plain Text Input" project.

First the folder:
	- Books folder contains the pdf files to extract the phrases to later extract the features to train the prediction model.
	- ExtractedText folder contains txt files that contains the extracted phrases from the books which will be used to extract the features.
	- Extracted features folder contains the features extracted saved in csv from the ExtractedText folder
	- Training models folder contains scripts to train different models to predict languages. However the used in the final version is model_MNB.ipynb which is in the main folder

Next, the scripts:
	- Phrase_extractor.py, extracts the phrases from the books folder and saves the phrases in a txt in the ExtractedText folder
	- FeatureExtraction.py, extracts the features from the phrases in the ExtractedText folder
	- gui_onfly.py, the main script that the shows GUI with the whole prediction process.
	- kalman.py, contains the Kalman filter class and its methods
	- model_MNB.ipynb, trains he MNB model to predict the language and creates the files cv.sav, le.sav, Trained_model.sav 

Finally, the files cv.sav, le.sav, Trained_model.sav are the trained model that is used by the gui_onfly.py script to predict the language.