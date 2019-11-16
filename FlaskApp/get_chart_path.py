import os


# class to collect name and time of modification of file
class File:

    def __init__(self, path, date):
        self.path = path
        self.date = date

# look for new generated charts in specified folder
def find_charts(path, quantity):

    # list to sort images by date
    sort_paths = []
    # walk in img directory and write file path and date to list
    for roots, dirs, files in os.walk(path):
        
        for file in files:
            # relative path to file from 'static' folder
            image_path = f'img/{file}'
            # date of modification
            date = os.path.getctime(f'{path}/{file}')

            file_object = File(image_path, date)
            sort_paths.append(file_object)

    # sort list by file creation date
    sort_paths.sort(key=lambda x: x.date, reverse=True)
    # list to return
    image_paths = []
    interator = 0
    # loop to write 3 newest 'File' object arguments to list to return
    for i in sort_paths:
        image_paths.append(i.path)
        if interator>=quantity-1:
            break
        interator+=1
    
    return image_paths
    

if __name__ == "__main__":
    print(find_charts('static/img',6))