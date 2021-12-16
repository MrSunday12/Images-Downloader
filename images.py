from argparse import ArgumentParser, Namespace
from os import getcwd, name, path, mkdir, remove
from subprocess import check_output, run, CalledProcessError, STDOUT
from contextlib import suppress

def parse_args() -> Namespace:
    """Parsers the arguments provided to the script using 'argparse'
    
    Returns:
        Namespace: a namepsace containing the arguments parsed
    """

    parser = ArgumentParser()
    
    src_group = parser.add_mutually_exclusive_group(required=True)

    src_group.add_argument('-i', action='store', nargs='+', dest='images', metavar='image1:tag image2:tag',
                    help='The images provided as a list from command line')
    src_group.add_argument('-f', action='store', dest='file', metavar='images.txt',
                    help='The images provided as list from txt file')
    
    parser.add_argument('-p',  type=str, default='.', dest='path', metavar='.',
                    help='<Not Required> The path to save the images to')

    parser.add_argument('-e', type=str, default='docker', dest='extension', metavar='docker',
                    help='<Not Required> The extension to use for saved images')

    parser.add_argument('-r', action='store_true', dest='redownload',
                    help='<Not Required> Enable to redownload any images that were previously downloaded')

    return parser.parse_args()


def download_image(image: str, image_path: str, extension: str, redownload: bool) -> None:
    """Uses docker to download an image to a file
    
    Parameters:
        image (str): the name of the image to download
        image_path (str): The path of where to save the image
        extension (str): The extension to use for saving the image
        redownload (bool): Whether to redownload the image if it was previously downloaded
    """

    if ":" not in image:
        image = image.strip() + ":latest"
    
    image_full_path = path.join(image_path, f"{image}.{extension}".replace('/', '.')).replace(':', '.')
    image_downloaded = path.isfile(image_full_path)

    if image_downloaded and redownload:
        print("Image already downloaded, redownloading it")
        with suppress(FileNotFoundError):
            remove(image_full_path)
    elif image_downloaded:
        print("Image already downloaded, skipping it")
        return

    image_pulled = True
    try:
        check_output(["docker", "inspect", image, "--format=exists"],
            stderr=STDOUT, timeout=3, universal_newlines=True)
    except CalledProcessError:
        image_pulled = False
        
    error_pulling = False
    if not image_pulled:
        print(f"Pulling image: {image}")
        try:
            run(["docker",  "pull", image], check=True)
            error_pulling = True
        except CalledProcessError:
            error_pulling = False
    else:
        print(f"Image '{image}' already present on machine")

    if error_pulling: 
        print(f"Image '{image}' was not pulled successfully, skipping it")
        return

    print(f"Downloading '{image}' image to: '{image_full_path}'")
    run(["docker",  "save",  "-o", image_full_path, image])


def main():
    args = parse_args()
    #print(args)

    if not path.exists(args.path):
        mkdir(args.path)

    if args.images:
        for image in args.images:
            print("-" * 50)
            download_image(image, args.path, args.extension, args.redownload)
    elif args.file:
        if path.isfile(args.file):
            with open(args.file, mode="r", encoding='utf-8') as file:
                for image in file.readlines():
                    print("-" * 50)
                    download_image(image.strip(), args.path, args.extension, args.redownload)
        else:
            print(f"Error: no such file '{args.file}'")
            return
    else:
        print("Error: Neither 'images' or 'file' was chosen")
        return


if __name__ == "__main__":
    main()
