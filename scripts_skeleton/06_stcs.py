import mne
from pathlib import Path
import pickle

from params import SRC_SPACING, VOL_SPACING, L_FREQ, H_FREQ, FILT_METHOD, SUBJECT_TO, MINIMUM_NORM_METHOD, fnames
from utils.argparser import setup_argparser
from utils.logger import setup_report, save_report


if __name__ == "__main__":
    parser = setup_argparser(description="Compute source time courses from epochs", subject=True)
    args = parser.parse_args()
    subject = args.subject


    # ------------------------------------------------------------------
    # Prepare to load all the needed elements
    # ------------------------------------------------------------------

    # src_path = 
    # fwd_path =
    # morph_path = 
    # epochs_path = 
    
    # ------------------------------------------------------------------
    # Load epochs, and choose a subset of them (all targets for example as you may run into memory problems otherwise)
    # ------------------------------------------------------------------
    epochs = mne.read_epochs(epochs_path)
    epochs = epochs["<INSERT SOMETHING HERE!>"]

    # ------------------------------------------------------------------
    # Open a report
    # ------------------------------------------------------------------
    # TODO: path
    # TODO: 

    # ------------------------------------------------------------------
    # Compute covariance between sensors for whitening and add to report
    # ------------------------------------------------------------------    
    # TODO: Compute noise covariance
    # TODO: add covariance to report

    # ------------------------------------------------------------------
    # Inverse
    # ------------------------------------------------------------------    
    fwd = mne.read_forward_solution(fwd_path)
    # TODO: make inverse operator

    # ------------------------------------------------------------------
    # Get source time courses
    # ------------------------------------------------------------------ 
    stcs = mne.minimum_norm.apply_inverse_epochs(
        epochs, inv,
        method=MINIMUM_NORM_METHOD,
        lambda2=1.0 / 9.0
    )

    # ------------------------------------------------------------------
    # Morph to fsaverage to we can analyse at group level
    # ------------------------------------------------------------------ 
    morph = mne.read_source_morph(morph_path)
    stcs_morphed = [morph.apply(stc) for stc in stcs]

    # ------------------------------------------------------------------
    # Save morphed source time courses
    # ------------------------------------------------------------------ 
    # TODO: DEFINE WHERE YOU WANT TO SAVE THE STCS. We'll save them using pickle, so use .pkl as file ending
    # stcs_path = 

    with open(stcs_path, "wb") as f:
        pickle.dump(stcs_morphed, f)


    # ------------------------------------------------------------------
    # Save report
    # ------------------------------------------------------------------ 
    save_report(report, report_path)