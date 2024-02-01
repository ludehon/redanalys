import time
import json
from Summarizer import Summarizer
from RawParser import clean_str, read_json_file


"""
Slices a given text into multiple parts based on word count, with specified overlap between slices.

Parameters:
input_string (str): The text to be sliced.
slice_length (int): The total number of words in each slice.
overlap_percentage (float): The percentage of a slice that overlaps with the next slice.

Returns:
list: A list of sliced strings.
"""
def slice_text(input_string, slice_length, overlap_percentage):
    words = input_string.split()
    if (len(words) < slice_length):
        slice_length = int(slice_length/2)
    slices = []
    overlap = int(slice_length * overlap_percentage)
    for i in range(0, len(words), slice_length - overlap):
        slices.append(" ".join(words[i:i + slice_length]))
    return slices


"""
Summarize big text by slicing it
param summarizer: summarizer object calling LLM's API
param input_string: the text to slice and summarize
"""
def summarize_slices(summarizer, input_string):
    print(f"Processing input string, word count : {len(input_string.split(' '))}")
    summarized_slices = []
    for i, slice in enumerate(slice_text(input_string, 1000, 0.30)):
        print(f"    processing slice {i}")
        cleaned_slice = clean_str(slice, "\n")
        summarized_slice = summarizer.summarize_string(cleaned_slice)
        summarized_slices.append(summarized_slice)
    return " ".join(summarized_slices)


if __name__ == "__main__":
    filename = "hp1_c1_c7"
    credentials = read_json_file("credentials.json")
    instruction = "Summarize this story part in few and short sentences, keep the important highlights and ommit minor details : "
    su = Summarizer(credentials["host"], instruction, -1)

    with open(filename+".txt", 'r') as file:
        text = file.read()

    i = 1
    start_time = time.time()
    while (len(text.split(' '))>300):
        print(f"step {i}, wc is {len(text.split(' '))}")
        text = summarize_slices(su, text)
        with open(f"sum_{filename}_step{i}.txt", "a") as file:
            file.write(f"---step_{i} :\n{text}")
        i=i+1
    end_time = time.time()
    time_spent = end_time - start_time

    print(f"Time spent summarazing: {time_spent/60} minutes")

    print(f"step {i}, wc is {len(text.split(' '))}")
    with open(f"sum_{filename}.txt", "w") as file:
        file.write(text)