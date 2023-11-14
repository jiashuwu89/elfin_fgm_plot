"""This code reads orbits_fgm_cal_elb.csv 
and plot parameter vs time of the closest terminator crossing.
'type_id' = 4 if satellite is in shadow(eclipse), 
'type_id' = 3 is satellite is in sun.
Continuous events of 3 means that the spacecraft did not enter shadow and was in high beta.

This only plot respect to the closest shadow-sun crossing
"""
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os
from plot_parameter import get_paraCSV, getFileList
import matplotlib.patches as mpatches

COLORS_DICT = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'yellow',
    4: 'purple',
    5: 'orange',
    6: 'pink',
    }

XLIM1 = -3000
XLIM2 = 6000

def get_terminatorCSV(filename: str) -> pd.DataFrame:
    """read from orbits_fgm_cal_elb.csv
    """
    df = pd.read_csv(filename)
    df['start_time_datetime'] = list(map(lambda ts: dt.datetime.strptime(ts, '%Y-%m-%d/%H:%M:%S'), df['start_time']))
    df['stop_time_datetime'] = list(map(lambda ts: dt.datetime.strptime(ts, '%Y-%m-%d/%H:%M:%S'), df['stop_time']))
    
    return df

def extract_terminator(df: pd.DataFrame, terminator_type: str = None):
    """get the terminator crossing according to type_id change
    """
    if terminator_type == 'sun-shadow':
        df['type_id_change'] = (df['type_id'] == 3) & (df['type_id'].shift(-1) == 4)
    elif terminator_type == 'shadow-sun':
        df['type_id_change'] = (df['type_id'] == 4) & (df['type_id'].shift(-1) == 3)
    else:
        df['type_id_change'] = (df['type_id'] != df['type_id'].shift(-1))
    df_rows = df.loc[df['type_id_change'] == True]
    return df_rows[['start_time_datetime', 'stop_time_datetime', 'type_id']]


def plot_dt_Gain(df_terminator: pd.DataFrame):
    """plot time relative to closest terminator vs Gain
    """
    fig, (ax2, ax4, ax6) = plt.subplots(3,1, figsize=(10, 8))

    ax2.scatter(df_terminator['dt_terminator'], df_terminator['G1'], color=df_terminator['color'])
    ax4.scatter(df_terminator['dt_terminator'], df_terminator['G1'], color=df_terminator['color'])
    ax6.scatter(df_terminator['dt_terminator'], df_terminator['G1'], color=df_terminator['color'])

    ax2.set_ylabel("G1")
    ax2.set_ylim([0, 300])
    ax2.set_xlim([XLIM1, XLIM2])
    ax2.set_title("shadow-sun crossing")

    ax4.set_ylabel("G2")
    ax4.set_ylim([0, 300])
    ax4.set_xlim([XLIM1, XLIM2])

    ax6.set_xlabel("time to terminator (s)")
    ax6.set_ylabel("G3")
    ax6.set_ylim([0, 200])
    ax6.set_xlim([XLIM1, XLIM2])

    legend_handles = [mpatches.Patch(color=color, label=f'Beta {i*10+10} - {i*10+20}') for i, color in COLORS_DICT.items()]
    plt.legend(handles=legend_handles, title='Beta Ang')
    plt.show()


def plot_dt_th(df_terminator: pd.DataFrame):
    """plot time relative to closest terminator vs theta
    """
    fig, (ax2, ax4, ax6) = plt.subplots(3,1, figsize=(10, 8))
    ax2.scatter(df_terminator['dt_terminator'], df_terminator['th1'], color=df_terminator['color'])
    ax4.scatter(df_terminator['dt_terminator'], df_terminator['th2'], color=df_terminator['color'])
    ax6.scatter(df_terminator['dt_terminator'], df_terminator['th3'], color=df_terminator['color'])
    
    ax2.set_ylabel("th1")
    ax2.set_ylim([50, 110])
    ax2.set_xlim([XLIM1, XLIM2])
    ax2.set_title("shadow-sun crossing")

    ax4.set_ylabel("th2")
    ax4.set_ylim([50, 110])
    ax4.set_xlim([XLIM1, XLIM2])

    ax6.set_xlabel("time to terminator (s)")
    ax6.set_ylabel("th3")
    ax6.set_ylim([-20, 120])
    ax6.set_xlim([XLIM1, XLIM2])

    legend_handles = [mpatches.Patch(color=color, label=f'Beta {i*10+10} - {i*10+20}') for i, color in COLORS_DICT.items()]
    plt.legend(handles=legend_handles, title='Beta Ang')
    plt.show()


def plot_dt_ph(df_terminator: pd.DataFrame):
    """plot time relative to closest terminator vs phi
    """
    fig, (ax2, ax4, ax6) = plt.subplots(3,1, figsize=(10, 8))
    ax2.scatter(df_terminator['dt_terminator'], df_terminator['ph1'], color=df_terminator['color'])
    ax4.scatter(df_terminator['dt_terminator'], df_terminator['ph2'], color=df_terminator['color'])
    ax6.scatter(df_terminator['dt_terminator'], df_terminator['ph3'], color=df_terminator['color'])

    ax2.set_ylabel("ph1")
    ax2.set_ylim([-100, 100])
    ax2.set_xlim([XLIM1, XLIM2])
    ax2.set_title("shadow-sun crossing")

    ax4.set_ylabel("ph2")
    ax4.set_ylim([-110, 110])
    ax4.set_xlim([XLIM1, XLIM2])

    ax6.set_xlabel("time to terminator (s)")
    ax6.set_ylabel("ph3")
    ax6.set_ylim([-120, 0])
    ax6.set_xlim([XLIM1, XLIM2])

    legend_handles = [mpatches.Patch(color=color, label=f'Beta {i*10+10} - {i*10+20}') for i, color in COLORS_DICT.items()]
    plt.legend(handles=legend_handles, title='Beta Ang')
    plt.show()


if __name__ == "__main__":
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.min_rows', 500)
    pd.set_option('display.max_colwidth', 150)
    pd.set_option('display.width', 200)
    pd.set_option('expand_frame_repr', True)

    mission = "elb"
    foldername = "parameters"
    start_time_str = "2021-12-16"
    end_time_str = "2022-06-26"
    filenames = getFileList(foldername, mission, start_time_str, end_time_str)
    dfs = [get_paraCSV(os.path.join(foldername, filename)) for filename in filenames]
    beta_df = pd.concat(dfs, ignore_index=True)
    beta_df['beta_datetime'] = beta_df['end_time_datetime'] + 0.5*(beta_df['end_time_datetime'] - beta_df['start_time_datetime'])


    filename = mission+"_fgm_sunshadow_20211201_20220630.csv"
    df = get_terminatorCSV(filename)
    df_terminator = extract_terminator(df, terminator_type='shadow-sun')
    #df_terminator['terminator_datetime'] = df_terminator['stop_time_datetime'] + 0.5*(df_terminator['stop_time_datetime'] - df_terminator['start_time_datetime'])
    df_terminator['terminator_datetime'] = df_terminator['stop_time_datetime']


    beta_df = beta_df.sort_values(by='beta_datetime')
    beta_df['beta_ang'] = beta_df['beta_ang'].apply(lambda x: (x-10)//10)
    beta_df['color'] = beta_df['beta_ang'].map(COLORS_DICT)
    df_terminator = df_terminator.sort_values(by='terminator_datetime')


    df_merged = pd.merge_asof(beta_df, df_terminator, left_on='beta_datetime', right_on='terminator_datetime', direction='nearest')
    df_merged['dt_terminator'] = list(map(lambda ts: ts.total_seconds(), df_merged['beta_datetime'] - df_merged['terminator_datetime']))
    #plt.plot(terminator_34['dt_terminator'],terminator_34['G1'])

    #print(df_merged[['start_time_datetime_x','end_time_datetime','beta_datetime','start_time_datetime_y','stop_time_datetime', 'terminator_datetime', 'type_id']][0:100])


    plot_dt_Gain(df_merged)
    plot_dt_th(df_merged)
    plot_dt_ph(df_merged)

    
    breakpoint()
    
