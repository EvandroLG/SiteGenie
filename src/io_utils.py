def read_file(file_path):
    """
    Reads the contents of a file and returns it as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The contents of the file as a string.
        None: If the file is not found.

    Raises:
        Exception: If an unexpected error occurs while reading the file.
    """

    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        raise e
