import mne
from mne.preprocessing import ICA, create_ecg_epochs, create_eog_epochs

from params import fnames, L_FREQ, H_FREQ, ICA_L_FREQ, FILT_METHOD, N_ICA_COMPONENTS, ICA_METHOD, RANDOM_STATE, ICA_DECIM
from utils.argparser import setup_argparser
from utils.logger import setup_report, save_report


if __name__ == "__main__":
    parser = setup_argparser(description="Run ICA decomposition of the data and identify artefact components", subject=True)
    args = parser.parse_args()
    subject = args.subject

    # ------------------------------------------------------------------
    # Open preprocessing report
    # ------------------------------------------------------------------
    report_path = fnames.preproc_report(subject=subject)
    report = setup_report(report_path, title=f"Preprocessing Report | {subject} ")

    # ------------------------------------------------------------------
    # Load filtered data with higher high-pass cutoff, to remove slow drifts that can interfere with ICA
    # ------------------------------------------------------------------
    raw_filtered_ica_path = fnames.sub_filtered(subject=subject, l_freq=ICA_L_FREQ, h_freq=H_FREQ, method=FILT_METHOD)
    
    # TODO: load it. 
    # raw_ica = .....

    # ------------------------------------------------------------------
    # Fit ICA to the data
    # ------------------------------------------------------------------
    # TODO: instanciate the ICA object
    # TODO: fit the ICA. hint set the decim=10 to run quicker. Should not influence the results to much. 
    # You may want to set the parameter in the params.py file. ICA_DECIM=10 and import it here


    # ------------------------------------------------------------------
    # Find onsets of heart beats and blinks. Create epochs around them
    # ------------------------------------------------------------------
    ecg_epochs = create_ecg_epochs(raw_ica, tmin=-0.3, tmax=0.3, preload=False)
    eog_epochs = create_eog_epochs(raw_ica, tmin=-0.5, tmax=0.5, preload=False)
    
    
    # ------------------------------------------------------------------
    # Find ICA components that correlate with heart beats.
    # ------------------------------------------------------------------
    ecg_epochs.decimate(5)
    ecg_epochs.load_data()
    ecg_epochs.apply_baseline((None, None))
    ecg_inds, ecg_scores = ica.find_bads_ecg(ecg_epochs, method="ctps")
    print("    Found %d ECG indices" % (len(ecg_inds),))


    # ------------------------------------------------------------------
    # Find ICA components that correlate with eye movement
    # ------------------------------------------------------------------
    # TODO: do the same thing for EOG!
    

    # ------------------------------------------------------------------
    # mark the components to be excluded
    # ------------------------------------------------------------------
    ica.exclude = ecg_inds + eog_inds

    # ------------------------------------------------------------------
    # save ica!
    # ------------------------------------------------------------------
    ica_path = fnames.sub_ica(subject=subject)
    ica.save(ica_path, overwrite=True)

    del raw_ica

    # ------------------------------------------------------------------
    # Load the data with a LESS high high-pass cutoff
    # ------------------------------------------------------------------
    # TODO: use fnames to define the path to the. Remember to use l_freq=L_FREQ instead of ICA_L_FREQ
    # TODO: load it. 
    # raw = .....


    # ------------------------------------------------------------------
    # add the ICA components to the report and save it
    # ------------------------------------------------------------------
    report.add_ica(
        ica, title="ICA", inst=raw, 
        ecg_evoked=ecg_epochs.average(), ecg_scores=ecg_scores, 
        eog_evoked=eog_epochs.average(), eog_scores=eog_scores,
        replace=True
    )
    

    # ------------------------------------------------------------------
    # Apply ICA and save 
    # ------------------------------------------------------------------
    raw_filtered_ica_path = fnames.sub_filtered_ica(subject=subject, l_freq=L_FREQ, h_freq=H_FREQ, method=FILT_METHOD)

    ica.apply(raw)
    raw.save(raw_filtered_ica_path, overwrite=True)


    # ------------------------------------------------------------------
    # Add the ICA cleaned raw data to the report
    # ------------------------------------------------------------------
    # TODO: Add the ICA cleaned raw data to the report. Hint: have a look at the 03_filter.py file and make sure to provide a informative title
    

    # ------------------------------------------------------------------
    # Save the report
    # ------------------------------------------------------------------
    # TODO: save report
   