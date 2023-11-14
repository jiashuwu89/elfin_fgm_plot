"""This code reads orbits_fgm_cal_elb.csv 
and plot parameter vs time of the closest terminator crossing.
'type_id' = 4 if satellite is in shadow(eclipse), 
'type_id' = 3 is satellite is in sun.
Continuous events of 3 means that the spacecraft did not enter shadow and was in high beta.
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

def get_terminatorCSV(filename: str) -> pd.DataFrame:
    """read from orbits_fgm_cal_elb.csv
    """
    df = pd.read_csv(filename)
    df['start_time_datetime'] = list(map(lambda ts: dt.datetime.strptime(ts, '%Y-%m-%d/%H:%M:%S'), df['start_time']))
    df['stop_time_datetime'] = list(map(lambda ts: dt.datetime.strptime(ts, '%Y-%m-%d/%H:%M:%S'), df['stop_time']))
    
    return df

def extract_terminator(df: pd.DataFrame):
    """get the terminator crossing according to type_id change
    """
    df['type_id_change'] = (df['type_id'] != df['type_id'].shift(-1))
    df_rows = df.loc[df['type_id_change'] == True]
    return df_rows[['start_time_datetime', 'stop_time_datetime', 'type_id']]


def plot_dt_Gain(df_terminator34: pd.DataFrame, df_terminator43: pd.DataFrame):
    """plot time relative to closest terminator vs Gain
    """
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2, figsize=(10, 8))
    ax1.scatter(df_terminator34['dt_terminator'], df_terminator34['G1'], color=df_terminator34['color'])
    ax3.scatter(df_terminator34['dt_terminator'], df_terminator34['G2'], color=df_terminator34['color'])
    ax5.scatter(df_terminator34['dt_terminator'], df_terminator34['G3'], color=df_terminator34['color'])

    ax2.scatter(df_terminator43['dt_terminator'], df_terminator43['G1'], color=df_terminator43['color'])
    ax4.scatter(df_terminator43['dt_terminator'], df_terminator43['G1'], color=df_terminator43['color'])
    ax6.scatter(df_terminator43['dt_terminator'], df_terminator43['G1'], color=df_terminator43['color'])

    ax1.set_ylabel("G1")
    ax1.set_ylim([0, 300])
    ax1.set_xlim([0, 6000])
    ax1.set_title("sun-shadow crossing")

    ax2.set_ylabel("G1")
    ax2.set_ylim([0, 300])
    ax2.set_xlim([0, 6000])
    ax2.set_title("shadow-sun crossing")

    ax3.set_ylabel("G2")
    ax3.set_xlim([0, 6000])
    ax3.set_ylim([0, 300])

    ax4.set_ylabel("G2")
    ax4.set_ylim([0, 300])
    ax4.set_xlim([0, 6000])

    ax5.set_xlabel("time to terminator (s)")
    ax5.set_ylabel("G3")
    ax5.set_ylim([0, 200])
    ax5.set_xlim([0, 6000])

    ax6.set_xlabel("time to terminator (s)")
    ax6.set_ylabel("G3")
    ax6.set_ylim([0, 200])
    ax6.set_xlim([0, 6000])

    legend_handles = [mpatches.Patch(color=color, label=f'Beta {i*10+10} - {i*10+20}') for i, color in COLORS_DICT.items()]
    plt.legend(handles=legend_handles, title='Beta Ang')
    plt.show()


def plot_dt_th(df_terminator34: pd.DataFrame, df_terminator43: pd.DataFrame):
    """plot time relative to closest terminator vs theta
    """
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2, figsize=(10, 8))
    ax1.scatter(df_terminator34['dt_terminator'], df_terminator34['th1'], color=df_terminator34['color'])
    ax2.scatter(df_terminator43['dt_terminator'], df_terminator43['th1'], color=df_terminator43['color'])
    ax3.scatter(df_terminator34['dt_terminator'], df_terminator34['th2'], color=df_terminator34['color'])
    ax4.scatter(df_terminator43['dt_terminator'], df_terminator43['th2'], color=df_terminator43['color'])
    ax5.scatter(df_terminator34['dt_terminator'], df_terminator34['th3'], color=df_terminator34['color'])
    ax6.scatter(df_terminator43['dt_terminator'], df_terminator43['th3'], color=df_terminator43['color'])
    ax1.set_ylabel("th1")
    ax1.set_ylim([50, 110])
    ax1.set_xlim([0, 6000])
    ax1.set_title("sun-shadow crossing")

    ax2.set_ylabel("th1")
    ax2.set_ylim([50, 110])
    ax2.set_xlim([0, 6000])
    ax2.set_title("shadow-sun crossing")

    ax3.set_ylabel("th2")
    ax3.set_ylim([50, 110])
    ax3.set_xlim([0, 6000])

    ax4.set_ylabel("th2")
    ax4.set_ylim([50, 110])
    ax4.set_xlim([0, 6000])

    ax5.set_xlabel("time to terminator (s)")
    ax5.set_ylabel("th3")
    ax5.set_ylim([-20, 120])
    ax5.set_xlim([0, 6000])

    ax6.set_xlabel("time to terminator (s)")
    ax6.set_ylabel("th3")
    ax6.set_ylim([-20, 120])
    ax6.set_xlim([0, 6000])

    legend_handles = [mpatches.Patch(color=color, label=f'Beta {i*10+10} - {i*10+20}') for i, color in COLORS_DICT.items()]
    plt.legend(handles=legend_handles, title='Beta Ang')
    plt.show()


def plot_dt_ph(df_terminator34: pd.DataFrame, df_terminator43: pd.DataFrame):
    """plot time relative to closest terminator vs phi
    """
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3,2, figsize=(10, 8))
    ax1.scatter(df_terminator34['dt_terminator'], df_terminator34['ph1'], color=df_terminator34['color'])
    ax2.scatter(df_terminator43['dt_terminator'], df_terminator43['ph1'], color=df_terminator43['color'])
    ax3.scatter(df_terminator34['dt_terminator'], df_terminator34['ph2'], color=df_terminator34['color'])
    ax4.scatter(df_terminator43['dt_terminator'], df_terminator43['ph2'], color=df_terminator43['color'])
    ax5.scatter(df_terminator34['dt_terminator'], df_terminator34['ph3'], color=df_terminator34['color'])
    ax6.scatter(df_terminator43['dt_terminator'], df_terminator43['ph3'], color=df_terminator43['color'])
    ax1.set_ylabel("ph1")
    ax1.set_ylim([-100, 100])
    ax1.set_xlim([0, 6000])
    ax1.set_title("sun-shadow crossing")

    ax2.set_ylabel("ph1")
    ax2.set_ylim([-100, 100])
    ax2.set_xlim([0, 6000])
    ax2.set_title("shadow-sun crossing")

    ax3.set_ylabel("ph2")
    ax3.set_ylim([-110, 110])
    ax3.set_xlim([0, 6000])

    ax4.set_ylabel("ph2")
    ax4.set_ylim([-110, 110])
    ax4.set_xlim([0, 6000])

    ax5.set_xlabel("time to terminator (s)")
    ax5.set_ylabel("ph3")
    ax5.set_ylim([-120, 0])
    ax5.set_xlim([0, 6000])

    ax6.set_xlabel("time to terminator (s)")
    ax6.set_ylabel("ph3")
    ax6.set_ylim([-120, 0])
    ax6.set_xlim([0, 6000])

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
    df_terminator = extract_terminator(df)
    #df_terminator['terminator_datetime'] = df_terminator['stop_time_datetime'] + 0.5*(df_terminator['stop_time_datetime'] - df_terminator['start_time_datetime'])
    df_terminator['terminator_datetime'] = df_terminator['stop_time_datetime']


    beta_df = beta_df.sort_values(by='beta_datetime')
    beta_df['beta_ang'] = beta_df['beta_ang'].apply(lambda x: (x-10)//10)
    beta_df['color'] = beta_df['beta_ang'].map(COLORS_DICT)
    df_terminator = df_terminator.sort_values(by='terminator_datetime')


    df_merged = pd.merge_asof(beta_df, df_terminator, left_on='beta_datetime', right_on='terminator_datetime', direction='backward')
    df_merged['dt_terminator'] = list(map(lambda ts: ts.total_seconds(), df_merged['beta_datetime'] - df_merged['terminator_datetime']))

    terminator_34 = df_merged[df_merged['type_id'] == 3]
    terminator_43 = df_merged[df_merged['type_id'] == 4]
    #plt.plot(terminator_34['dt_terminator'],terminator_34['G1'])

    #print(df_merged[['start_time_datetime_x','end_time_datetime','beta_datetime','start_time_datetime_y','stop_time_datetime', 'terminator_datetime', 'type_id']][0:100])


    plot_dt_Gain(terminator_34, terminator_43)
    plot_dt_th(terminator_34, terminator_43)
    plot_dt_ph(terminator_34, terminator_43)

    
    breakpoint()
    
