import os

# removes extensions from images
def remove_extension():
    filenames = os.listdir('.')
    image_extensions = ['jpg', 'jpeg', 'png', 'tiff', 'gif', 'bmp', 'bpg']
    for filename in filenames:
        idx = filename.rfind('.')
        ext = filename[idx+1:]
        if (idx != -1 and ext in image_extensions):
            os.rename(filename, filename[:idx])

if __name__ == '__main__':
    remove_extension()
