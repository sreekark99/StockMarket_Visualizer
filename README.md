
# Stock Backtest and Visualization



## Requirements
Before running the scripts, ensure the following Python libraries are installed:

numpy - For numerical operations.

pandas - For data manipulation and analysis.

matplotlib - For static data visualization (if needed).

requests - For sending HTTP requests.

yfinance - For downloading stock data.

dash - For creating the interactive web application.
Make sure "LongPath" is enabled in Windows v10 and above.

Refer: https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell#enable-long-paths-in-windows-10-version-1607-and-later

plotly - For creating interactive plots.

```python
  pip install numpy pandas matplotlib requests yfinance dash plotly

```

## File Overview

There will be two primary files for the app.

File 1: "main_code.py"

File 2: "app_visualization.py"

Both the files will be run using a single command.

```python
python main_code.py && python app_visualization.py

```

We need to run this command from the folder where all both the files are stored. Make sure both the files ("File 1" and "File 2") are in the same folder.

Once the above command is executed, default browser will open the visualization plots. However, you can open it on the local URL: http://127.0.0.1:8050/

The visualization is done for only the stocks that are traded during the period.

Please Note: The URL may differ based on the OS and Software versions, do check the Terminal/Command Prompt where the command is executed to find the local URL where it opens.

To Exit the code, type Ctrl+c (or) Cmd+c.



## Screenshots

![App Screenshot 1](https://i.ibb.co/ccnMyzY/Screenshot-1867.png)
![App Screenshot 2](https://i.ibb.co/6wXPLL9/Screenshot-1868.png)
![App Screenshot 3](https://i.ibb.co/6vmPXj6/Screenshot-1869.png)
![App Screenshot 4](https://i.ibb.co/FnM8dh3/Screenshot-1870.png)




## Authors

- [Sreekar K](https://github.com/sreekark99)

