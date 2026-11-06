#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.patches import FancyBboxPatch, Rectangle
import os
from math import ceil 


def _ax_plot(ax, x, y, secs=10, lwidth=0.5, amplitude_ecg = 1.8, time_ticks =0.2):
    ax.set_xticks(np.arange(0,11,time_ticks))    
    ax.set_yticks(np.arange(-ceil(amplitude_ecg),ceil(amplitude_ecg),1.0))

    #ax.set_yticklabels([])
    #ax.set_xticklabels([])

    ax.minorticks_on()
    
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))

    ax.set_ylim(-amplitude_ecg, amplitude_ecg)
    ax.set_xlim(0, secs)

    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle='-', linewidth='0.5', color=(1, 0.7, 0.7))

    ax.plot(x,y, linewidth=lwidth)


lead_index = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
def plot_12(
        ecg, 
        sample_rate = 500, 
        title       = 'ECG 12', 
        lead_index  = lead_index, 
        lead_order  = None,
        columns     = 2,
        speed = 50,
        voltage = 20,
        line_width = 0.6
        ):
    """Plot multi lead ECG chart.
    # Arguments
        ecg        : m x n ECG signal data, which m is number of leads and n is length of signal.
        sample_rate: Sample rate of the signal.
        title      : Title which will be shown on top off chart
        lead_index : Lead name array in the same order of ecg, will be shown on 
            left of signal plot, defaults to ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        lead_order : Lead display order 
        columns    : display columns, defaults to 2
        speed      : signal speed on display, defaults to 50 mm / sec
        voltage    : signal voltage on display, defaults to 20 mm / mV
        line_width : line width, default to 0.6
    """
    if not lead_order:
        lead_order = list(range(0,len(ecg)))

    leads = len(lead_order)
    seconds = len(ecg[0])/sample_rate

    plt.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots(
        ceil(len(lead_order)/columns),columns,
        sharex=True, 
        sharey=True,
        figsize=((speed/25)*seconds*columns,    # 1 inch= 25,4 mm. Rounded to 25 for simplicity
            (4.1*voltage/25)*leads/columns)     # 1 subplot usually contains values in range of (-2,2) mV
        )
    fig.subplots_adjust(
        hspace = 0, 
        wspace = 0.04,
        left   = 0.04,  # the left side of the subplots of the figure
        right  = 0.98,  # the right side of the subplots of the figure
        bottom = 0.06,  # the bottom of the subplots of the figure
        top    = 0.95
        )
    fig.suptitle(title)

    step = 1.0/sample_rate

    for i in range(0, len(lead_order)):
        if(columns == 1):
            t_ax = ax[i]
        else:
            t_ax = ax[i//columns,i%columns]
        t_lead = lead_order[i]
        t_ax.set_ylabel(lead_index[t_lead])
        t_ax.tick_params(axis='x',rotation=90)
       
        _ax_plot(t_ax, np.arange(0, len(ecg[t_lead])*step, step), ecg[t_lead], seconds)

def plot(
        ecg, 
        sample_rate    = 500, 
        title          = 'ECG 12', 
        lead_index     = lead_index, 
        lead_order     = None,
        style          = None,
        columns        = 2,
        row_height     = 6,
        show_lead_name = True,
        show_grid      = True,
        show_separate_line  = True,
        highlight_leads=None,
        p_waves=None,
        qrs_waves=None,
        t_waves=None,
        pvcs=None,
        pacs=None,
        highlight_ranges=None,
        highlight_range2=None,
        highlight_color=None,
        highlight_alpha=0.2,
        checkmarks=None,
        checkmark_color="black",
        boundary_overlays=None,
        scale=1.0,
        stack=True,
        ):
    """Plot multi lead ECG chart.
    # Arguments
        ecg        : m x n ECG signal data, which m is number of leads and n is length of signal.
        sample_rate: Sample rate of the signal.
        title      : Title which will be shown on top off chart
        lead_index : Lead name array in the same order of ecg, will be shown on 
            left of signal plot, defaults to ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        lead_order : Lead display order 
        columns    : display columns, defaults to 2
        style      : display style, defaults to None, can be 'bw' which means black white
        row_height :   how many grid should a lead signal have,
        show_lead_name : show lead name
        show_grid      : show grid
        show_separate_line  : show separate line
    """
    highlight_color = "blue" if highlight_color is None else highlight_color

    if not lead_order:
        lead_order = list(range(0,len(ecg)))
    secs  = len(ecg[0])/sample_rate
    leads = len(lead_order)
    rows  = int(ceil(leads/columns))
    # display_factor = 2.5
    display_factor = scale
    line_width = 0.5
    fig, ax = plt.subplots(figsize=(secs*columns * display_factor, rows * row_height / 5 * display_factor))
    display_factor = display_factor ** 0.5
    fig.subplots_adjust(
        hspace = 0, 
        wspace = 0,
        left   = 0,  # the left side of the subplots of the figure
        right  = 1,  # the right side of the subplots of the figure
        bottom = 0,  # the bottom of the subplots of the figure
        top    = 1
        )

    fig.suptitle(title)

    x_min = 0
    x_max = columns*secs
    y_min = row_height/4 - (rows/2)*row_height
    y_max = row_height/4

    if (style == 'bw'):
        color_major = (0.4,0.4,0.4)
        color_minor = (0.75, 0.75, 0.75)
        color_line  = (0,0,0)
    else:
        color_major = (1,0,0)
        color_minor = (1, 0.7, 0.7)
        color_line  = (0,0,0.7)

    if(show_grid):
        ax.set_xticks(np.arange(x_min,x_max,0.2))    
        ax.set_yticks(np.arange(y_min,y_max,0.5))

        ax.minorticks_on()
        
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))

        ax.grid(which='major', linestyle='-', linewidth=0.5 * display_factor, color=color_major)
        ax.grid(which='minor', linestyle='-', linewidth=0.5 * display_factor, color=color_minor)

    ax.set_ylim(y_min,y_max)
    ax.set_xlim(x_min,x_max)


    for c in range(0, columns):
        for i in range(0, rows):
            if (c * rows + i < leads):
                y_offset = -(row_height/2) * ceil(i%rows)
                # if (y_offset < -5):
                #     y_offset = y_offset + 0.25

                x_offset = 0
                if(c > 0):
                    x_offset = secs * c
                    if(show_separate_line):
                        ax.plot([x_offset, x_offset], [ecg[t_lead][0] + y_offset - 0.3, ecg[t_lead][0] + y_offset + 0.3], linewidth=line_width * display_factor, color=color_line)

         
                t_lead = lead_order[c * rows + i]
         
                step = 1.0/sample_rate
                if(show_lead_name):
                    ax.text(x_offset + 0.07, y_offset - 0.5, lead_index[t_lead], fontsize=9 * display_factor)
                    if highlight_leads is not None and lead_index[t_lead] in highlight_leads:
                        bbox = FancyBboxPatch(
                            (x_offset + 0.37, y_offset - 0.5),
                            9.25,
                            1,
                            boxstyle="round,rounding_size=0.5",
                            fc="yellow",
                            ec="none"
                        )
                        ax.add_patch(bbox)
                ax.plot(
                    np.arange(0, len(ecg[t_lead])*step, step) + x_offset, 
                    ecg[t_lead] + y_offset,
                    linewidth=line_width * display_factor, 
                    color=color_line
                    )
                if p_waves is not None:
                    for p_wave in p_waves[t_lead]:
                        onset = p_wave.onset
                        offset = p_wave.offset
                        xs = np.arange(onset * step, offset * step, step) + x_offset
                        if len(xs) > offset - onset:
                            xs = xs[:-1]
                        if len(xs) == 0:
                            continue

                        ax.axvspan(
                            xmin=xs[0],
                            xmax=xs[-1],
                            ymin=(min(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) - 0.025,
                            ymax=(max(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) + 0.025,
                            color="orange",
                            alpha=0.5
                        )

                if qrs_waves is not None:
                    for j, qrs_wave in enumerate(qrs_waves[t_lead]):
                        onset = qrs_wave.onset
                        offset = qrs_wave.offset
                        xs = np.arange(onset * step, offset * step, step) + x_offset
                        if len(xs) > offset - onset:
                            xs = xs[:-1]
                        if len(xs) == 0:
                            continue

                        color = "red"
                        if pvcs is not None and pvcs[j]:
                            color = "green"
                        elif pacs is not None and pacs[j]:
                            color = "yellow"

                        ax.axvspan(
                            xmin=xs[0],
                            xmax=xs[-1],
                            ymin=(min(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) - 0.025,
                            ymax=(max(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) + 0.025,
                            color=color,
                            alpha=0.5
                        )
                if t_waves is not None:
                    for t_wave in t_waves[t_lead]:
                        onset = t_wave.onset
                        offset = t_wave.offset
                        xs = np.arange(onset * step, offset * step, step) + x_offset
                        if len(xs) > offset - onset:
                            xs = xs[:-1]
                        if len(xs) == 0:
                            continue

                        ax.axvspan(
                            xmin=xs[0],
                            xmax=xs[-1],
                            ymin=(min(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) - 0.025,
                            ymax=(max(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) + 0.025,
                            color="cyan",
                            alpha=0.5
                        )
                
                if highlight_ranges is not None:
                    for highlight_range in highlight_ranges:
                        onset = highlight_range[0]
                        offset = highlight_range[1]
                        xs = np.arange(onset * step, offset * step, step) + x_offset
                        if len(xs) > offset - onset:
                            xs = xs[:-1]
                        if len(xs) == 0:
                            continue

                        ax.axvspan(
                            xmin=xs[0],
                            xmax=xs[-1],
                            ymin=(min(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) - 0.025,
                            ymax=(max(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) + 0.025,
                            color=highlight_color,
                            alpha=highlight_alpha
                        )

                if highlight_range2 is not None:
                    onset = highlight_range2[0]
                    offset = highlight_range2[1]
                    xs = np.arange(onset * step, offset * step, step) + x_offset
                    if len(xs) > offset - onset:
                        xs = xs[:-1]
                    if len(xs) == 0:
                        continue

                    ax.axvspan(
                        xmin=xs[0],
                        xmax=xs[-1],
                        ymin=(min(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) - 0.025,
                        ymax=(max(ecg[t_lead][onset:offset]) + y_offset - y_min) / (y_max - y_min) + 0.025,
                        color="magenta",
                        alpha=0.8
                    )
                
                if checkmarks is not None:
                    for x in checkmarks:
                        ax.scatter(
                            x=x * step + x_offset,
                            y=max(y_offset + 0.35, max(ecg[t_lead][max(0, x-10):min(x+10, len(ecg[t_lead]))] + y_offset + 0.35)),
                            marker=r"$\checkmark$",
                            s=50,
                            color=checkmark_color,
                        )

                # boundary_overlays: highlight each beat's onset..offset span as a translucent
                # colored box, without any line over the trace. Multiple algorithms are stacked
                # into horizontal sub-bands within the lead so their colors do not blend;
                # single-point features (no offset) get a small marker at the fiducial.
                if boundary_overlays is not None:
                    _K = len(boundary_overlays)
                    _hh = (row_height / 2) * 0.45
                    # each algorithm is a translucent box + crisp border, drawn behind the grid
                    # and trace. stack=True lays them out as thin gantt bars so edges line up;
                    # stack=False draws every box full height so they overlap and blend.
                    _stack = stack and _K > 1
                    _sh = _hh * 0.6
                    _bar_full = (2 * _sh) / max(_K, 1)
                    _bar_h = _bar_full * 0.8
                    for _k, _ov in enumerate(boundary_overlays):
                        _waves = _ov.get("waves", {}).get(t_lead)
                        if not _waves:
                            continue
                        _color = _ov.get("color", "blue")
                        _fa = _ov.get("alpha", 0.5)          # translucent fill
                        _ea = _ov.get("edge_alpha", 0.95)    # crisper border
                        _elw = 1.2 * display_factor
                        if _stack:
                            _top = y_offset + _sh - _k * _bar_full
                            _bot = _top - _bar_h
                        else:
                            _top, _bot = y_offset + _hh, y_offset - _hh
                        for _spans in _waves.values():
                            for _on, _off in _spans:
                                _on = None if _on is None or (isinstance(_on, float) and np.isnan(_on)) else _on
                                _off = None if _off is None or (isinstance(_off, float) and np.isnan(_off)) else _off
                                if _on is not None and _off is not None:
                                    _x0, _x1 = _on * step + x_offset, _off * step + x_offset
                                elif _on is not None or _off is not None:
                                    # point feature (ST at the J point): small +/-10 ms box
                                    # around the fiducial (x axis is in seconds, so fs-independent)
                                    _xc = (_on if _on is not None else _off) * step + x_offset
                                    _x0, _x1 = _xc - 0.010, _xc + 0.010
                                else:
                                    continue
                                # translucent fill + a more-opaque border, both behind grid/trace
                                ax.fill_between([_x0, _x1], _bot, _top,
                                                color=_color, alpha=_fa, linewidth=0, zorder=-5)
                                ax.add_patch(Rectangle((_x0, _bot), _x1 - _x0, _top - _bot,
                                                       facecolor="none", edgecolor=_color,
                                                       linewidth=_elw, alpha=_ea, zorder=-5))

    if boundary_overlays is not None:
        from matplotlib.patches import Patch
        _handles = [Patch(facecolor=_ov.get("color", "blue"), alpha=0.6,
                          label=_ov.get("name", "?")) for _ov in boundary_overlays]
        ax.legend(handles=_handles, loc="upper right", fontsize=8,
                  framealpha=0.95, ncol=max(1, len(_handles)))


def plot_1(ecg, sample_rate=500, title = 'ECG', fig_width = 15, fig_height = 2, line_w = 0.5, ecg_amp = 1.8, timetick = 0.2):
    """Plot multi lead ECG chart.
    # Arguments
        ecg        : m x n ECG signal data, which m is number of leads and n is length of signal.
        sample_rate: Sample rate of the signal.
        title      : Title which will be shown on top off chart
        fig_width  : The width of the plot
        fig_height : The height of the plot
    """
    plt.figure(figsize=(fig_width,fig_height))
    plt.suptitle(title)
    plt.subplots_adjust(
        hspace = 0, 
        wspace = 0.04,
        left   = 0.04,  # the left side of the subplots of the figure
        right  = 0.98,  # the right side of the subplots of the figure
        bottom = 0.2,   # the bottom of the subplots of the figure
        top    = 0.88
        )
    seconds = len(ecg)/sample_rate

    ax = plt.subplot(1, 1, 1)
    #plt.rcParams['lines.linewidth'] = 5
    step = 1.0/sample_rate
    _ax_plot(ax,np.arange(0,len(ecg)*step,step),ecg, seconds, line_w, ecg_amp,timetick)
    
DEFAULT_PATH = './'
show_counter = 1
def show_svg(tmp_path = DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        tmp_path: path for temporary saving the result svg file
    """ 
    global show_counter
    file_name = tmp_path + "show_tmp_file_{}.svg".format(show_counter)
    plt.savefig(file_name)
    os.system("open {}".format(file_name))
    show_counter += 1
    plt.close()

def show():
    plt.show()


def save_as_png(file_name, path = DEFAULT_PATH, dpi = 100, layout='tight'):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
        dpi      : set dots per inch (dpi) for the saved image
        layout   : Set equal to "tight" to include ax labels on saved image
    """
    plt.ioff()
    plt.savefig(path + file_name + '.png', dpi = dpi, bbox_inches=layout)
    plt.close()

def save_as_svg(file_name, path = DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
    """
    plt.ioff()
    plt.savefig(path + file_name + '.svg')
    plt.close()

def save_as_jpg(file_name, path = DEFAULT_PATH):
    """Plot multi lead ECG chart.
    # Arguments
        file_name: file_name
        path     : path to save image, defaults to current folder
    """
    plt.ioff()
    plt.savefig(path + file_name + '.jpg')
    plt.close()
