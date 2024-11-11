import ydata_profiling as yp
from ..dataset import create_dataset
import webbrowser
import sys
from pathlib import Path

if __name__ == "__main__":
    df = create_dataset()
    profile = yp.ProfileReport(df)

    profile.to_notebook_iframe()