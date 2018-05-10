# speedy_resizer
Simple command-line tool or module for fast bulk resizing of images using Pillow & multiprocessing

# requirements
python >=3.5
Pillow or Pillow-SIMD for further speedup

# useage
```
python3 resize.py [-h] -dir DIR [-dest DEST] [-subf] -w W -hi HI [-a] [-p] [-r RESAMPLE] [-q QUALITY]

optional arguments:
-h, --help            show this help message and exit
-dir DIR              Pass directory to resize the images in
-dest DEST            Pass directory to save resized the images in, if not specified dest will be ./resize/
-subf                 include images in subfolders
-w W                  width of resized images
-hi HI                height of resized images
-a, --aspect          resized images will retain aspect ratio
-p, --padding         adds black padding to resized images (when --aspect flag is set) so imgs will be of size target_size
-r RESAMPLE, --resample RESAMPLE specify resampling methods from PIL: LANCZOS, NEAREST, BILINEAR, BICUBIC are valid options
-q QUALITY, --quality QUALITY specify jpg quality for resized images from 0 to 95; default 80
```
