import os
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from typing import List

def get_paraCSV(filename: str) -> pd.DataFrame:
    """This function reads fgm parameters from csv file"""
    try:
        df = pd.read_csv(filename)
        df['start_time_datetime'] = list(map(lambda ts: dt.datetime.strptime(ts, "%Y-%m-%d/%H:%M:%S"), df['start_time']))
        df['end_time_datetime'] = list(map(lambda ts: dt.datetime.strptime(ts, "%Y-%m-%d/%H:%M:%S"), df['end_time']))
        
        return df
    except:
        print(f"{filename} can't be loaded!")
        return


def getFileList(foldername: str, mission: str, start_time_str: str, end_time_str: str) -> List[str]:
    """Get the file list according to start and end time"""
    filenames = os.listdir(foldername)
    datetime_format = '%Y-%m-%d_%H%M'
    filename_select = []
    start_time = dt.datetime.strptime(start_time_str, "%Y-%m-%d")
    end_time = dt.datetime.strptime(end_time_str, "%Y-%m-%d")
    for filename in filenames:
        if filename.endswith(f"{mission}_Gthphi.csv"):
            datetime_str = filename.split('_')[0] + '_' + filename.split('_')[1]
            datetime = dt.datetime.strptime(datetime_str, datetime_format)
            filename_select.append(filename) if datetime > start_time and datetime < end_time else []
    
    return filename_select



def plot_beta_Gain(beta_df: pd.DataFrame):

    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(10, 8))
    ax1.scatter(beta_df['beta_ang'], beta_df['G1'])
    ax2.scatter(beta_df['beta_ang'], beta_df['G2'])
    ax3.scatter(beta_df['beta_ang'], beta_df['G3'])
    ax1.set_ylabel("G1")
    ax1.set_ylim([0, 300])
    ax2.set_ylabel("G2")
    ax2.set_ylim([0, 300])
    ax3.set_xlabel("beta angle (deg)")
    ax3.set_ylabel("G3")
    ax3.set_ylim([0, 200])
    ax1.set_title("fgm Gain and beta angle")

    plt.show()


def plot_beta_th(beta_df: pd.DataFrame):

    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(10, 8))
    ax1.scatter(beta_df['beta_ang'], beta_df['th1'])
    ax2.scatter(beta_df['beta_ang'], beta_df['th2'])
    ax3.scatter(beta_df['beta_ang'], beta_df['th3'])
    ax1.set_ylabel("th1")
    ax1.set_ylim([50, 110])
    ax2.set_ylabel("th2")
    ax2.set_ylim([50, 110])
    ax3.set_xlabel("beta angle (deg)")
    ax3.set_ylabel("th2")
    ax3.set_ylim([-20, 120])
    ax1.set_title("fgm theta and beta angle")

    plt.show()


def plot_beta_ph(beta_df: pd.DataFrame):

    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(10, 8))
    ax1.scatter(beta_df['beta_ang'], beta_df['ph1'])
    ax2.scatter(beta_df['beta_ang'], beta_df['ph2'])
    ax3.scatter(beta_df['beta_ang'], beta_df['ph3'])
    ax1.set_ylabel("ph1")
    ax1.set_ylim([-100, 100])
    ax2.set_ylabel("ph2")
    ax2.set_ylim([-110, 110])
    ax3.set_xlabel("beta angle (deg)")
    ax3.set_ylabel("ph3")
    ax3.set_ylim([-120, 0])
    ax1.set_title("fgm phi and beta angle")

    plt.show()  


def plot_beta_offset(beta_df: pd.DataFrame):

    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(10, 8))
    ax1.scatter(beta_df['beta_ang'], beta_df['O1/G1'])
    ax2.scatter(beta_df['beta_ang'], beta_df['O2/G2'])
    ax3.scatter(beta_df['beta_ang'], beta_df['O3/G3'])
    ax1.set_ylabel("O1/G1")
    ax1.set_ylim([-10000, 10000])
    ax2.set_ylabel("O2/G2")
    ax2.set_ylim([-10000, 10000])
    ax3.set_xlabel("beta angle (deg)")
    ax3.set_ylabel("O3/G3")
    ax3.set_ylim([-5000, 5000])
    ax1.set_title("fgm offset and beta angle")

    plt.show()        


if __name__ == "__main__":
    mission = "elb"
    foldername = "parameters"
    start_time_str = "2021-12-16"
    end_time_str = "2022-06-26"
    filenames = getFileList(foldername, mission, start_time_str, end_time_str)
    dfs = [get_paraCSV(os.path.join(foldername, filename)) for filename in filenames]
    beta_df = pd.concat(dfs, ignore_index=True)

    plot_beta_Gain(beta_df)
    plot_beta_th(beta_df)
    plot_beta_ph(beta_df)
    plot_beta_offset(beta_df)
    

