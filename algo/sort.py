import os

def merge_sort(file_names):
    if len(file_names) > 1:
        mid = len(file_names) // 2  # Find the middle index
        left_half = file_names[:mid]  # Divide list into halves
        right_half = file_names[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:  # Compare alphabetically
                file_names[k] = left_half[i]
                i += 1
            else:
                file_names[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            file_names[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            file_names[k] = right_half[j]
            j += 1
            k += 1

    return file_names

def sort_text_files_by_name(directory):
    try:
        # Get a list of all text files in the directory
        text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        # Sort the text files using merge sort
        sorted_files = merge_sort(text_files)

        return sorted_files

    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# test
if __name__ == "__main__":
    directory_path = input("Enter the directory path containing text files: ")
    sorted_files = sort_text_files_by_name(directory_path)
    print("Sorted text files:")
    for file in sorted_files:
        print(file)
