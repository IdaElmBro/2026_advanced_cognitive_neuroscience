# File overview

> **Note:** Some files may not be uploaded until later!

## Notebooks
The purpose of the notebooks in this repository is to provide you with some code and exercises which should make you more familiar with the data and different steps in a MEG analysis pipeline. 

* `filter_ica_epochs.ipynb`: Illustrates a basic preprocessing pipeline, including filtering the data, using ICA to remove artifacts from eye movements and cardiac activity, finding events from the stimulus channel, and creating epochs.

* `add_epoch_metadata.ipynb`: Shows how to add behavioural metadata to the epochs (e.g. ensuring that each event is associated with the contrast, objective response, pas score, etc).

* `photodiode.ipynb`: Shows how to use the photodiode signal to account for delays between the trigger and the actual onset of the stimulus.

* `headmovement_chpi.ipynb`: Shows how to use the continuous HPI recordings to determine how much the participant moved during the experiment.

* `source_recon.ipynb`: Illustrates the steps involved in setting up the source space, computing the forward model and  the data for source reconstruction.

*Coming soon to a GitHub repo near you:*

* `MVPA.ipynb`: Illustrates how to prepare the data and perform multivariate pattern analysis (MVPA), including regressing out the effect of contrast. 


## Scripts
The skeleton scripts in the `scripts_skeleton` folder are designed to guide you through building your own analysis pipeline. You should be able to find the code you need in the notebooks and adapt it for use in the scripts. See the table in the next section to find out which notebooks are relevant to each script.

* `01_anatomy.py`
* `02_forward.py`
* `03_filter.py`
* `04_ica.py`
* `05_epochs.py`
* `06_stcs.py`

*Coming soon to a GitHub repo near you:*
* `07_evoked.py`
* `08_erf_stats.py`

In addition to these, you may also want to develop scripts for your specific analyses. 
The `07_evoked.py` and `08_erf_stats.py` scripts can serve as inspiration for how to prepare and analyse data first at the subject level, and then compute group-level statistics.

## Correspondence between analysis scripts and notebooks

To guide you, here is a table showing which notebooks may contain relevant code for developing each script.

| Script          | Relevant notebook(s)                                                                | Notes                                                                                                                            |
| --------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `01_anatomy.py` | `source_recon.ipynb`                                                       | Defining source locations for surface and volumetric source space, and computing the morph to `fsaverage`. Provided but need to be modified if you want to run it yourself as you don't have writing rights to the fwd folder.          |
| `02_forward.py` | `source_recon.ipynb`                                                       | Creating the forward model for surface and volumetric source space. Provided but need to be modified if you want to run it yourself as you don't have writing rights to the fwd folder.                                                 |
| `03_filter.py`  | `filter_ica_epochs.ipynb`                                                           | Adding bad channels to `info` and filtering.                                                                                     |
| `04_ica.py`     | `filter_ica_epochs.ipynb`                                                           | ICA / artifact removal.                                                                                                          |
| `05_epochs.py`  | `filter_ica_epochs.ipynb`, `photodiode.ipynb`, `add_epoch_metadata.ipynb` | Accounting for the delay between the trigger and stimulus onset, creating epochs, and adding behavioural metadata to the epochs. |
| `06_stcs.py`  | `source_recon.ipynb` | Compute source time courses from epochs using a minimum-norm inverse solution, then morph them to fsaverage for group-level analysis.|
## Other files

| File        | Notes                                                                                                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `params.py` | Shared analysis parameters used by the analysis scripts. This is where subject-specific information (e.g. bad channels), filtering parameters, and filenames are defined and kept track of. |
