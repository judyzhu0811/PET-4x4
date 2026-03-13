import re
import csv

# Input/output files
input_file = "raw_output.txt"
output_file = "photon_data.csv"

# Open CSV for writing
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["EventID", "DetectorID", "PhotonCount"])  # header

    with open(input_file, "r") as f:
        for line in f:
            # Adjust the regex based on how your photon counts appear in raw_output.txt
            # Example line: "Event 1 Detector 2: 5 photons"
            match = re.search(r"Event\s+(\d+)\s+Detector\s+(\d+):\s+(\d+)\s+photons", line)
            if match:
                event_id = int(match.group(1))
                detector_id = int(match.group(2))
                photon_count = int(match.group(3))
                writer.writerow([event_id, detector_id, photon_count])

print(f"CSV saved as {output_file}")
