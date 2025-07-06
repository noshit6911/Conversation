import os

def precise_split(source_file, output_dir, num_files):
    """
    Splits a source text file into a specified number of smaller files with
    as even a distribution of lines as possible.

    Args:
        source_file (str): The path to the source file to be split.
        output_dir (str): The directory where the split files will be saved.
        num_files (int): The number of files to split the source into.
    """
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)
        lines_per_file = total_lines // num_files
        remainder = total_lines % num_files

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        start_index = 0
        for i in range(1, num_files + 1):
            # Distribute the remainder lines one by one to the first few files
            chunk_size = lines_per_file + (1 if i <= remainder else 0)
            end_index = start_index + chunk_size
            
            output_filename = os.path.join(output_dir, f'flow_{i}.md')
            with open(output_filename, 'w', encoding='utf-8') as out_f:
                out_f.writelines(lines[start_index:end_index])
            
            print(f"Created {output_filename} with {chunk_size} lines.")
            start_index = end_index

        print(f"\nSuccessfully split '{source_file}' into {num_files} files in '{output_dir}'.")
        # Verification step
        print("Verifying split...")
        combined_lines = []
        for i in range(1, num_files + 1):
            with open(os.path.join(output_dir, f'flow_{i}.md'), 'r', encoding='utf-8') as f:
                combined_lines.extend(f.readlines())
        
        if lines == combined_lines:
            print("Verification successful: All content is perfectly preserved.")
        else:
            print("Verification failed: Content mismatch detected.")

    except FileNotFoundError:
        print(f"Error: The source file '{source_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    SOURCE = 'Entire GPT Convo.md'
    OUTPUT = 'secondary book sections'
    NUMBER_OF_FILES = 10
    
    precise_split(SOURCE, OUTPUT, NUMBER_OF_FILES) 