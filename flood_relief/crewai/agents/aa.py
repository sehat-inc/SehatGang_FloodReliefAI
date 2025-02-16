def read_file_as_string(file_path):
    """
    Reads the content of a file and returns it as a string.

    Parameters:
    file_path (str): The path to the file to be read.

    Returns:
    str: The content of the file as a single string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None
    except IOError:
        print(f"An error occurred while reading the file at {file_path}.")
        return None
    
file_path = "../knowledge/data.txt"
json_content = read_file_as_string(file_path=file_path)
print(json_content)


print(json_content)