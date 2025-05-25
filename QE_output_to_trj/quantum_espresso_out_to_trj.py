import sys
import os

def extract_all_atomic_positions(file_path):
    start_str = "ATOMIC_POSITIONS (angstrom)\n"
    
    with open(file_path, "r") as f:
        content = f.read()

    indices = []
    start = 0

    while True:
        start = content.find(start_str, start)
        if start == -1:
            break
        start += len(start_str)

        end = content.find("\n\n", start)  # Find blank line separating frames
        if end == -1:
            end = len(content)
        
        frame_data = content[start:end].strip()
        indices.append(frame_data)
        start = end  # Move to next frame

    return indices if indices else None

def write_xyz_trajectory(frames, output_file):
    with open(output_file, "w") as f:
        for frame in frames:
            lines = frame.split("\n")
            num_atoms = 0
            cleaned_lines = []

            for line in lines:
                split_line = line.split()
                if len(split_line) >= 4:  # Include lines with extra values like '0 0 0'
                    cleaned_lines.append(" ".join(split_line[:4]))
                    num_atoms += 1

            if num_atoms > 0:
                f.write(f"{num_atoms}\n")  # First line: number of atoms
                f.write("Frame from Quantum Espresso Output\n")  # Second line: comment
                for atom_line in cleaned_lines:
                    f.write(atom_line + "\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("Error: File not found!")
        sys.exit(1)
    
    frames = extract_all_atomic_positions(input_file)
    if frames:
        output_file = os.path.splitext(input_file)[0] + ".xyz"
        write_xyz_trajectory(frames, output_file)
        print(f"Multi-frame trajectory written to {output_file}")
    else:
        print("Error: No atomic positions found in the file!")

if __name__ == "__main__":
    main()
