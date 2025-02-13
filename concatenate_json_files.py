import json

file_paths = ["article_data.json", "article_data2.json", "article_data3.json"]

def concatenate_json_files(file_paths, output_file="combined.json"):
    """
    Concatenates the contents of multiple JSON files into a single JSON array.

    Args:
        file_paths: A list of paths to the JSON files.
        output_file: The name of the output file. Defaults to "combined.json".
    """
    combined_data = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    combined_data.extend(data)
                elif isinstance(data, dict):
                    combined_data.append(data) # Treat dictionaries as single-element lists
                # else:  # Optionally handle other types (but it might break JSON structure)
                #     combined_data.append(data)


        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return  # Exit if a file is not found
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file: {file_path}")
            return  # Exit if invalid JSON is encountered

    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

    print(f"Successfully concatenated JSON files into {output_file}")


if __name__ == "__main__":
    # Example usage:
    # file_paths = ["article_data.json", "article_data2.json", "article_data3.json"]

    # Create some dummy JSON files (for a quick test)
    # data1 = [{"id": 1, "name": "Alice"}]
    # data2 = [{"id": 2, "name": "Bob"}, {"id": 3, "name": "Charlie"}]
    # data3 = {"key": "value"} # Example with a dictionary

    # with open("file1.json", "w") as f:
    #     json.dump(data1, f)
    # with open("file2.json", "w") as f:
    #     json.dump(data2, f)
    # with open("file3.json", "w") as f:
    #     json.dump(data3, f)

    concatenate_json_files(file_paths)