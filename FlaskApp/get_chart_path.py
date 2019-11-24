import os


class File:
    """File object contains path and date of file modification.

    Attributes:
        path (str):Path to file.
        date(str):Date of file modification.


    """

    def __init__(self, path, date):
        self.path = path
        self.date = date


def find_charts(path, quantity):
    """Find path to specified of newest chart images.

    Parameters:
        path (str):Path to file.
        quantity (inst):Number of newest charts to find.
    Returns:
        image_paths(list):List with paths to charts.


    """
    # list to sort images by date
    sort_paths = []
    # walk in img directory and write file path and date to list
    for roots, dirs, files in os.walk(path):
        for file in files:
            # relative path to file from 'static' folder
            image_path = f'{file}'
            # date of modification
            date = os.path.getctime(f'{path}/{file}')

            file_object = File(image_path, date)
            sort_paths.append(file_object)

    # sort list by file creation date
    sort_paths.sort(key=lambda x: x.date, reverse=True)
    # list to return
    image_paths = []
    interator = 0
    # loop to write number of newest 'File' object arguments to list to return
    for i in sort_paths:
        image_paths.append(i.path)
        if interator >= quantity-1:
            break
        interator += 1

    return image_paths


def get_chart_name(image_paths):
    """Get chart name from path.

    Parameters:
        image_paths (list):List with charts path.
    Returns:
        chart_name(list):List with names of charts.


    """
    # list to return charts name
    chart_name = []
    for i in image_paths:
        # split chart after third '_' and before '.'
        i = i.split('_', 3)[3].split('.', -1)[0]
        chart_name.append(i)

    return chart_name


if __name__ == "__main__":
    image_paths = (find_charts('static/img', 3))
    print(get_chart_name(image_paths))
