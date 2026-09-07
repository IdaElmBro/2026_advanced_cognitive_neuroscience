
import mne

from params import fnames
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
    # Load the ICA preprocessed data
    # ------------------------------------------------------------------
    # TODO: Use fnames to define the filepath
    # TODO: Load the data


    # ------------------------------------------------------------------
    # Now you've had some practise working this way! 
    # Try to create headings yourself and add relevant code!
    # What steps need to be done? 
    # Which things can we visualise on the way to make sure everything looks good? 
    # hint hint hints: 
    #   https://mne.tools/stable/generated/mne.Report.html#mne.Report.add_events
    #   https://mne.tools/stable/generated/mne.Report.html#mne.Report.add_epochs
    # ------------------------------------------------------------------



    # ------------------------------------------------------------------
    # Save epochs. Remember to include relevant 
    # ------------------------------------------------------------------



    # ------------------------------------------------------------------
    # Save report
    # ------------------------------------------------------------------