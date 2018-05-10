from path import Path
from PIL import Image
import argparse
import os
from multiprocessing.dummy import Pool


def resize_from_obj(img, dest, target_size, keep_aspect_ratio=True,
                    add_padding=False, resample='BILINEAR', jpg_quality=95):
    """
    resizes PIL image object img with resample as resampling filer then saves it
    to dest
    img: PIL image object tor resize
    dest: filepath + filename where resized img will be saved
    target_size: (height,width) tupel of positive integers
    keep_aspect_ratio: when True aspect ratio of the image will be kept
    add_padding: when True and keep_aspect_ratio=True black padding will be added so the final image is of size target_size
    resample: PIL resampling methods, avail. options: LANCOS, NEAREST, BILINEAR, BICUBIC
    jpg_quality: int between 10 and 95; quality of saved jpg file
    """
    resample_options = {'LANCZOS': Image.LANCZOS,
                        'NEAREST': Image.NEAREST,
                        'BILINEAR': Image.BILINEAR,
                        'BICUBIC': Image.BICUBIC}
    try:
        resample = resample_options[resample]
    except KeyError:
        print("Invalid resample Function; using NEAREST")
        resample = Image.NEAREST

    if keep_aspect_ratio:
        img.thumbnail(target_size, resample)
    else:
        img = img.resize(target_size, resample)

    if add_padding:
        padding = Image.new('RGB',
                            target_size)
        padding.paste(img)
        img = padding

    img.save(dest, 'JPEG', quality=jpg_quality)

    return


def _helper_resize_from_path(args):
    img_path = args[0]
    img = Image.open(img_path)
    args[0] = img
    resize_from_obj(*args)
    return


def batch_resize(img_paths, dest_folder, target_size,
                 keep_aspect_ratio=True, add_padding=False, resample='BILINEAR',
                 jpg_quality=95, chunksize=16, processes=None):
    """
    resizes all images given in list img_paths using multithreading. I advise using
    Pillow-SMID for further speedup.
    img_paths: list of paths to images
    dest_folder: images will be saved here.
    target_size, keep_aspect_ratio, add_padding, resample, jpg_quality: see resize_from_obj
    chunksize=16 : see multiprocessing.pool.Pool.map
    processes: number of extra threads started. If processes is None then the number returned by os.cpu_count() is used.
    """
    if dest_folder is None:
        dest_folder = "./resize/"

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    total_imgs = len(img_paths)
    print("Resizing {} images... ".format(total_imgs))

    args = ([img_path, dest_folder + Path(img_path).name.lower(),
             target_size, keep_aspect_ratio, add_padding, resample, jpg_quality] for img_path in img_paths)

    pool = Pool(processes)
    pool.map(_helper_resize_from_path, args, chunksize)
    pool.close()

    print("Done!")


def resize_folder(img_folder, dest_folder, target_size, include_subfolders=True,
                  keep_aspect_ratio=True, add_padding=False,
                  resample='BILINEAR', jpg_quality=95, chunksize=16,
                  processes=None):
    """
    resizes all images folder img_folder using multithreading. For more info see batch_resize
    """

    if include_subfolders:
        img_paths = list(Path(img_folder).walkfiles('[!.]*.jpg'))
        img_paths += list(Path(img_folder).walkfiles('[!.]*.jpeg'))
        img_paths += list(Path(img_folder).walkfiles('[!.]*.png'))
    else:
        img_paths = list(Path(img_folder).files('[!.]*.jpg'))
        img_paths += list(Path(img_folder).files('[!.]*.jpeg'))
        img_paths += list(Path(img_folder).files('[!.]*.png'))

    batch_resize(img_paths, dest_folder, target_size=target_size,
                 keep_aspect_ratio=keep_aspect_ratio, add_padding=add_padding,
                 resample=resample, jpg_quality=jpg_quality,
                 chunksize=chunksize, processes=processes)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Simple command-line tool for fast bulk resizing of images using Pillow & multiprocessing')
    parser.add_argument('-dir', type=str, default=None,
                        help='Pass directory to resize the images in', required=True)
    parser.add_argument('-dest', type=str, default=None,
                        help='Pass directory to save resized the images in, if not specified dest will be ./resize/')
    parser.add_argument('-subf', action="store_true",
                        help='include images in subfolders')
    parser.add_argument('-w', type=int, default=None,
                        help='width of resized images', required=True)
    parser.add_argument('-hi', type=int, default=None,
                        help='height of resized images', required=True)
    parser.add_argument('-a', '--aspect', action="store_true",
                        help='resized images will retain aspect ratio')
    parser.add_argument('-p', '--padding', action="store_true",
                        help='adds black padding to resized images (when --aspect flag is set) so imgs will be of size target_size')
    parser.add_argument('-r', '--resample', type=str, default='NEAREST',
                        help='specify resampling methods from PIL: LANCZOS, NEAREST, BILINEAR, BICUBIC are valid options')
    parser.add_argument('-q', '--quality', type=int, default=80,
                        help='specify jpg quality for resized images from 0 to 95; default 80')
    args = parser.parse_args()
    target_size = (args.w, args.hi)
    include_subfolders = args.subf
    keep_aspect_ratio = args.aspect
    add_padding = args.padding
    resample = args.resample
    jpg_quality = args.quality

    print(args.dest)
    if args.dir is not None:
        resize_folder(args.dir, args.dest, target_size=target_size,
                      include_subfolders=include_subfolders,
                      keep_aspect_ratio=keep_aspect_ratio, add_padding=add_padding,
                      resample=resample, jpg_quality=jpg_quality)
