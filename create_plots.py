import pandas as pd
import matplotlib.pyplot as plt
import os
import zipfile

def plot_and_save(csv_path, output_zip):
    #Load CSV data
    df = pd.read_csv(csv_path)
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')

    plot_dir = "plots"
    os.makedirs(plot_dir, exist_ok=True)

    plots = {
        "V_in": "Input Voltage (V_in) vs. Time",
        "V_bat": "Battery Voltage (V_bat) vs. Time",
        "V_C1": "Cell 1 Voltage (V_C1) vs. Time",
        "V_C2": "Cell 2 Voltage (V_C2) vs. Time",
        "V_C3": "Cell 3 Voltage (V_C3) vs. Time",
        "I_cqh": "Charging Current (I_cqh) vs. Time",
        "I_sum": "Total Current (I_sum) vs. Time",
        "T_int": "Internal Temperature (T_int) vs. Time",
    }

    plot_files = []
    for col, title in plots.items():
        plt.figure(figsize=(10, 5))
        plt.plot(df['time'], df[col], label=col, color='b')
        plt.xlabel("Time")
        plt.ylabel(col)
        plt.title(title)
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        
        plot_path = os.path.join(plot_dir, f"{col}.png")
        plt.savefig(plot_path)
        plot_files.append(plot_path)
        plt.close()

    #Create the ZIP file
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for file in plot_files:
            zipf.write(file, os.path.basename(file))

if __name__ == "__main__":
    csv_path = "/Users/kalilsmallwood/Desktop/Capstone 2025/PSUCapstone2025_BatteryChargingStation/test_data_csv(fake).csv"#Will change to wherever the data for that day or session gets saved 
    output_zip = "plots.zip"#Change to SD card or wherever we are gonna save the plots to
    plot_and_save(csv_path, output_zip)
    print(f"Plots saved in {output_zip}")
