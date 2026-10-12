import mne
import numpy as np
from scipy.stats import ttest_rel
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from pathlib import Path
from params import (
    fnames, L_FREQ, H_FREQ, FILT_METHOD, DATES, 
    EVOKED_CONDS, # list = ["stimulus/0", "stimulus/1"] 
    EVOKED_TMIN, EVOKED_TMAX,   # 0.160 , 0.175
    EVOKED_SENSORS,             # ['MEG2531', 'MEG2541', 'MEG2611','MEG2621']
)


def stats(window_means, conditions):
    if len(conditions) != 2:
        raise ValueError("A paired t-test requires exactly two conditions.")

    data1 = np.asarray(window_means[conditions[0]], dtype=float)
    data2 = np.asarray(window_means[conditions[1]], dtype=float)

    if len(data1) != len(data2):
        raise ValueError("Conditions must contain the same number of participants.")

    if not (np.isfinite(data1).all() and np.isfinite(data2).all()):
        raise ValueError("Data contain NaN or infinite values.")

    t_stat, p_value = ttest_rel(data1, data2)

    print(f"Paired t-test: {conditions[0]} vs {conditions[1]}")
    print(f"t({len(data1) - 1}) = {t_stat:.3f}, p = {p_value:.5f}")
    print(f"Mean difference = {(data1 - data2).mean():.6g}")

    return t_stat, p_value

def plot_results(evokeds, window_means, tmin_stats, tmax_stats, picks, savepath=None):

    colours = ["steelblue", "goldenrod"]
    conditions = list(evokeds.keys())
    n_subjects = [len(evokeds[cond]) for cond in conditions]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=300)


    # Plot grand-average ERFs
    for i, (cond, cond_evokeds) in enumerate(evokeds.items()):
        times = cond_evokeds[0].times

        data = np.stack([
            evoked.get_data(picks=picks)
            for evoked in cond_evokeds
        ])
        # Shape: participants x sensors x time
        grandaverage_evoked = data.mean(axis=(0, 1))

        axes[0].axvspan(
            tmin_stats, tmax_stats, color="grey", alpha=0.2
        )
        axes[0].plot(
            times,
            grandaverage_evoked,
            label=cond,
            color=colours[i % len(colours)]
        )

    axes[0].axvline(0, color="black", linestyle="--", linewidth=0.8)
    axes[0].set(
        xlabel="Time (s)",
        ylabel="Amplitude",
        title=f"Grand-average ERF ({picks})"
    )
    axes[0].legend()

    # Find samples within the time window
    times = evokeds[conditions[0]][0].times
    time_mask = (times >= tmin_stats) & (times <= tmax_stats)


    # Paired participant-level plot
    x = np.array([0, 1])

    for subject_idx in range(n_subjects[0]):
        y = [
            window_means[cond][subject_idx]
            for cond in conditions
        ]

        axes[1].plot(
            x, y,
            marker="o",
            color="grey",
            alpha=0.7,
            linewidth=1
        )

    # Overlay condition means
    for i, cond in enumerate(conditions):
        axes[1].scatter(
            i,
            np.mean(window_means[cond]),
            color=colours[i],
            edgecolor="black",
            s=80,
            zorder=3,
            label=f"{cond} mean"
        )


    axes[1].set_xticks(x)
    axes[1].set_xticklabels(conditions)
    axes[1].set_xlim([-0.5, 1.5])

    axes[0].set(
        xlabel="Time (s)",
        ylabel="Mean Amplitude",
        title=f"Mean amplitude: {tmin_stats:.3f}–{tmax_stats:.3f} s"
    )
    axes[1].legend()

    # Create a small inset in the upper-right corner
    ax_inset = inset_axes(
        axes[0],
        width="20%",
        height="20%",
        loc="right",
        borderpad=1,
    )

    info = evokeds[conditions[0]][0].info.copy()
    info["bads"] = []  # Don't mark bad channels in red

    # Plot all magnetometers
    mne.viz.plot_sensors(
        info,
        kind="topomap",
        ch_type="mag",
        axes=ax_inset,
        show_names=False,
        pointsize=0.2,
        show=False,
    )

    # Overlay selected sensors
    selected_info = mne.pick_info(
        info,
        mne.pick_channels(info["ch_names"], include=picks),
    )

    mne.viz.plot_sensors(
        selected_info,
        kind="topomap",
        ch_type="mag",
        axes=ax_inset,
        show_names=False,
        pointsize=10,
        show=False,
    )

    ax_inset.set_title("Sensors", fontsize=8)
        
    # Aesthetics: remove top and right spines
    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout()
    

    if savepath is not None:
        fig.savefig(savepath, dpi=300, bbox_inches="tight")

    plt.show()

    return fig, ax




if __name__ == "__main__":

    figure_path = Path(fnames.figures)
    figure_path.mkdir(exist_ok=True, parents=True)

    evokeds = {cond: [] for cond in EVOKED_CONDS}
    window_means = {cond: [] for cond in EVOKED_CONDS}

    for subject in DATES.keys():
        for cond in EVOKED_CONDS:
            evoked_path = fnames.sub_filtered_ica_evoked(subject=subject, l_freq=L_FREQ, h_freq=H_FREQ, method=FILT_METHOD, cond=cond.replace("/", "-"))
            evoked = mne.read_evokeds(evoked_path)
            evokeds[cond].extend(evoked)

            data = evoked[0].get_data(picks=EVOKED_SENSORS, tmin=EVOKED_TMIN, tmax=EVOKED_TMAX)

            # Mean across sensors and time points
            mean_amplitude = data.mean()
            window_means[cond].append(mean_amplitude)

    plot_results(evokeds, window_means, EVOKED_TMIN, EVOKED_TMAX, EVOKED_SENSORS, savepath=figure_path / "evoked_analysis_results.png")
    stats(window_means, EVOKED_CONDS)
