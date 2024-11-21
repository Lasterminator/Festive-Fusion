import os

files = os.listdir()

# #this renumbers the file if there is a missing file in the sequence
# for x, file in enumerate(files):
#   if file != "renamer.py":
#     num = (file[0:-4])
#     #if num > 18:
#     while not os.path.exists(f'{x}.png'):
#       os.rename(file, f'{x}.png')

# Get list of PNG files excluding the renamer script
png_files = [f for f in files if f.endswith('.png')]
png_files.sort(key=lambda x: int(x.split('.')[0]))

# Rename files sequentially from 0 to n
for i, file in enumerate(png_files):
    new_name = f'{i}.png'
    if file != new_name:
        os.rename(file, new_name)

