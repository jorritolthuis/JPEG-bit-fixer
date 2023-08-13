# JPEG bit fixer

This is a simple tool written in Python to fix bit flips in JPEG or JPG files. It can be used to fix corrupted images, caused for example by bit rot or (in my case) broken DRAM. It displays the image in hexadecimal, and allows the user to edit this. The program will then write the edited image to a new file.

It is primarily intended for fixing bit flips, as it does not check for the validity of the JPEG file. So removing or adding bytes will result in a corrupted image.

Do not name the input image `edited_image.jpg`, as this will be overwritten. Otherwise, the program will never overwrite or change the original input file.

## Usage

```
python3 fix_jpeg.py
```

### Example
The program is currently set up to fix the `DSC_0274.JPG` image. Run the program, select this image, and press the 'Render' button. The image will be displayed in a separate window, and will be written to the `edited_image.jpg` file.

### Performance
General photos are so large that this program runs into severe processing time issues. The workaround for this are the `prefix_bound` and `suffix_bound` variables. These are values between 0 and 1 to limit the number of hexadecimal values that are displayed. The prefix is not displayed in hexadecimal, same for the suffix. These are later added back on when showing and saving the image.

In my experience, performance is acceptable up to about 250 000 hexadecimal characters, but fewer is better (and easier to manage when editing). The easiest way to identify the bounds is by trying some bit flips and seeing where the image starts to change (first left-to-right, then down). Especially changes from `00` to `FF` and vice versa are easier to spot. It might take some tries to find bytes change change the luminance (as those changes are easiest to spot).