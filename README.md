# JPEG bit fixer

This is a simple tool written in Python to fix bit flips in JPEG or JPG files. It can be used to fix corrupted images, caused for example by bit rot or (in my case) broken DRAM. It displays the image in hexadecimal, and allows the user to edit this. The program will then write the edited image to a new file.

It is primarily intended for fixing bit flips, as it does not check for the validity of the JPEG file. So removing or adding bytes will result in a corrupted image.

Do not name the input image `edited_image.jpg`, as this will be overwritten. Otherwise, the program will never overwrite or change the original input file.

## Usage

```
python3 fix_jpeg.py
```

Three GUI windows will open: The HEX editor, the image preview, and the configuration. The HEX editor is used to edit the image in binary. The image preview shows the current image state. The configuration window allows the user to set the prefix and suffix bounds, and the zoom level.

### Example
The program is currently set up to fix the `DSC_0274.JPG` image. Run the program, select this image, and press the 'Render' button. The image will be displayed in a separate window. It is zoomed in to the part where the image is gets corrupted (to zoom out, set Zoom X and Y to `0`, and Zoom width and height to `1`). The displayed image is always written to the `edited_image.jpg` file.

The prefix and suffix bounds are applied when the "Open Image" button is used. The correct range has been selected for prefix and suffix to zoom in on the corrupted hex part of the image. To fix this image, make the following change:
```
55934CAAAB8520
      |
      V  
55934C2AAB8520
```

This change is one bit: We change `A` (`1010`) to `2` (`0010`). To make this change, click on the `A` in the image, and type `2`. After pressing "Render Image", the problem will be fixed

### Performance
General photos are so large that this program runs into severe processing time issues. The workaround for this are the `prefix_bound` and `suffix_bound` variables. These are values between 0 and 1 to limit the number of hexadecimal values that are displayed. The prefix is not displayed in hexadecimal, same for the suffix. These are later added back on when showing and saving the image.

Performance seems to be acceptable up to about 250 000 hexadecimal characters (125KB), but fewer is better (and easier to manage when editing). The easiest way to identify the bounds is by trying some bit flips and seeing where the image starts to change (first left-to-right, then down). Especially changes from `00` to `FF` and vice versa are more likely to be easy to spot. A simple [binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) is the quickest way to narrow down the prefix/suffix bounds.