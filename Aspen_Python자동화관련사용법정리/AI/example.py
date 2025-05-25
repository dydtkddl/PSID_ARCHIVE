
#!/usr/bin/env python3
import os
import argparse
import logging
import csv
import win32com.client

# =========================
# 1. INIT SECTION
# =========================
def init_args():
    parser = argparse.ArgumentParser(
        description="Mass Aspen Plus Case Study Automation"
    )
    parser.add_argument(
        "--aspen-file", required=True,
        help="Path to Aspen backup (.bkp) file"
    )
    parser.add_argument(
        "--output-csv", default="results.csv",
        help="Path to output CSV file"
    )
    parser.add_argument(
        "--temps", nargs="+", type=float, default=[300, 320, 340],
        help="Temperature grid (K)"
    )
    parser.add_argument(
        "--pressures", nargs="+", type=float, default=[1, 5, 10],
        help="Pressure grid (bar)"
    )
    parser.add_argument(
        "--flows", nargs="+", type=float, default=[100, 150, 200],
        help="Feed flow grid (kmol/hr)"
    )
    parser.add_argument(
        "--visible", action="store_true",
        help="Show Aspen Plus GUI during runs"
    )
    return parser.parse_args()

def init_simulation(aspen_file: str, visible: bool):
    AspenSimulation = win32com.client.gencache.EnsureDispatch("Apwn.Document")
    AspenSimulation.InitFromArchive2(os.path.abspath(aspen_file))
    AspenSimulation.Visible = visible
    # Shortcuts
    STRM = AspenSimulation.Tree.Elements("Data").Elements("Streams")
    BLK  = AspenSimulation.Tree.Elements("Data").Elements("Blocks")
    logging.info(f"Aspen initialized from: {aspen_file}")
    return AspenSimulation, STRM, BLK

# =========================
# 2. CASE STUDY SECTION
# =========================
def run_case_study(sim, STRM, temps, pressures, flows, output_csv):
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Temperature_K", "Pressure_bar", "FeedFlow_kmolhr", "Prod_Temp_K"])
        for T in temps:
            for P in pressures:
                for F in flows:
                    # set inputs
                    STRM.Elements("FEED").Elements("Input").Elements("TEMP").Value = T
                    STRM.Elements("FEED").Elements("Input").Elements("PRES").Value = P
                    STRM.Elements("FEED").Elements("Input") \
                         .Elements("FLOWBASE").Elements("MIXED").Value = F
                    # verify
                    status = STRM.Elements("FEED").COMPSTATUS
                    logging.debug(f"Feed status: {status}")
                    # run
                    sim.Engine.Run2()
                    # read output
                    prod_temp = STRM.Elements("PROD") \
                                    .Elements("Output") \
                                    .Elements("STR_MAIN") \
                                    .Elements("TEMP") \
                                    .Elements("MIXED").Value
                    writer.writerow([T, P, F, prod_temp])
    logging.info(f"Case study complete, results saved to {output_csv}")

# =========================
# 3. CLOSE SECTION
# =========================
def close_simulation(sim):
    fullpath = sim.FullName
    sim.Close(os.path.abspath(fullpath))
    logging.info("Aspen Plus session closed")

# =========================
# 4. MAIN ROUTINE
# =========================
def main():
    args = init_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    sim, STRM, BLK = init_simulation(args.aspen_file, args.visible)
    run_case_study(sim, STRM, args.temps, args.pressures, args.flows, args.output_csv)
    close_simulation(sim)

if __name__ == "__main__":
    main()

