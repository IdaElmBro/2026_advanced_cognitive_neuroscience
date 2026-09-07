from pathlib import Path
from utils.fnames import FileNames


# ------------------------------------------------------------------
# PREPROCESSING PARAMETERS
# ------------------------------------------------------------------

## list of bad channels for each subject
BAD_CHANNELS = {
    "example": ["MEG0121", "MEG192"],
}

DATES = {
    "example": "20251003_000000",
}

## Filtering
L_FREQ = 0.1
H_FREQ = 40
ICA_L_FREQ = 1
FILT_METHOD = "fir"

## Epoching
EPOCHS_TMIN = -0.2
EPOCHS_TMAX = 0.7
BASELINE = (None, 0) # from tmin to time of stimulation
DOWNSAMPLE_RATE = 250

# ICA
N_ICA_COMPONENTS = 0.99
ICA_METHOD = "fastica"
RANDOM_STATE = 42


# ------------------------------------------------------------------
# SOURCE MODELLING
# ------------------------------------------------------------------
SRC_SPACING = "oct6"
VOL_SPACING = 10


# ------------------------------------------------------------------
# PATHS
# ------------------------------------------------------------------
# determining the user to find a nice place to save derivatives 
p = Path(__file__)

uCloud_user = next(
    part for part in p.parts
    if "#" in part and part.split("#")[1].isdigit()
)


fnames = FileNames()
fnames.add('root', '/work')
fnames.add('raw', '{root}/raw')


fnames.add('subjects_dir', '{root}/freesurfer')
fnames.add('ucloud_memberfiles', '{root}'+f'/{uCloud_user}')
fnames.add('derivatives', '{ucloud_memberfiles}/derivatives')
fnames.add('meg_derivatives', '{derivatives}/MEG')


fnames.add('sub_meg_derivatives', '{meg_derivatives}/{subject}')
fnames.add('sub_raw', '{raw}/{subject}/{date}/workshop_2025_raw.fif')

# subject level derivatives
fnames.add('sub_filtered', '{sub_meg_derivatives}/{subject}_filtered_{l_freq}-{h_freq}_{method}_meg.fif')
fnames.add('sub_filtered_ica', '{sub_meg_derivatives}/{subject}_filtered_{l_freq}-{h_freq}_{method}_ICA_meg.fif')
fnames.add('sub_ica', '{sub_meg_derivatives}/{subject}_ica.fif')
fnames.add('sub_filtered_ica_epochs', '{sub_meg_derivatives}/{subject}_filtered_{l_freq}-{h_freq}_{method}_ICA-epo.fif')


# reports
fnames.add('reports', '{derivatives}/reports')
fnames.add('anatomy_report', '{reports}/{subject}/{subject}_anatomy_report.h5')
fnames.add('preproc_report', '{reports}/{subject}/{subject}_preproc_report.h5')

# bem
fnames.add('bem_model', '{sub_meg_derivatives}/{subject}_bem.fif')
fnames.add('bem_sol', '{sub_meg_derivatives}/{subject}_bem_solution.fif')

# source spaces
fnames.add('src_surface', '{sub_meg_derivatives}/{subject}_surface-spacing-{surf_spacing}-src.fif')
fnames.add('src_volume', '{sub_meg_derivatives}/{subject}_volume-spacing-{vol_spacing}mm-src.fif')
fnames.add('src_combined', '{sub_meg_derivatives}/{subject}_combined-surface-spacing-{surf_spacing}-volume-spacing-{vol_spacing}mm-src.fif')
