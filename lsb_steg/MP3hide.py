import os
from tqdm import tqdm

def hide(mp3_file, file_to_hide, output_file):
    if not os.path.exists(mp3_file):
        raise FileNotFoundError(f"MP3 file '{mp3_file}' not found.")
    if not os.path.exists(file_to_hide):
        raise FileNotFoundError(f"File to hide '{file_to_hide}' not found.")
    
    # Read the MP3 file
    with open(mp3_file, 'rb') as mp3:
        mp3_data = mp3.read()

    # Read the file to hide
    with open(file_to_hide, "rb") as hidden_file:
        data_to_hide = hidden_file.read()

    # Add a delimiter to mark the start of the hidden data
    delimiter = b'--HIDDEN-DATA-START--'

    # Append the hidden data to the MP3 file
    with open(output_file, 'wb') as output:
        output.write(mp3_data)
        output.write(delimiter)
        output.write(data_to_hide)

    print(f"File '{file_to_hide}' has been successfully hidden in '{output_file}'.")

def extract(mp3_file, output_file):
    if not os.path.exists(mp3_file):
        raise FileNotFoundError(f"MP3 file '{mp3_file}' not found.")
    
    # Read the MP3 file
    with open(mp3_file, 'rb') as mp3:
        mp3_data = mp3.read()

    # Find the delimiter that marks the start of the hidden data
    delimiter = b'--HIDDEN-DATA-START--'
    delimiter_index = mp3_data.find(delimiter)

    if delimiter_index == -1:
        raise ValueError("No hidden data found in the MP3 file.")

    # Extract the hidden data
    hidden_data = mp3_data[delimiter_index + len(delimiter):]

    # Write the hidden data to the output file
    with open(output_file, "wb") as output:
        output.write(hidden_data)

    print(f"Hidden data has been successfully extracted to '{output_file}'.")

def hide_file_in_mp3(mp3_file, file_to_hide, output_file):
    hide(mp3_file, file_to_hide, output_file)

def reveal_file_from_mp3(mp3_file, output_file):
    extract(mp3_file, output_file)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hide and extract files from MP3 files by appending hidden data.")
    parser.add_argument("mode", choices=["hide", "extract"], help="Mode: hide or extract")
    parser.add_argument("mp3_file", help="Input MP3 file")
    parser.add_argument("output_file", help="Output file")
    parser.add_argument("data", nargs="?", help="File to hide (for hide mode)")

    args = parser.parse_args()
    
    if args.mode == "hide":
        if not args.data:
            print("Please provide the file to hide.")
        else:
            hide_file_in_mp3(args.mp3_file, args.data, args.output_file)
    elif args.mode == "extract":
        reveal_file_from_mp3(args.mp3_file, args.output_file)
