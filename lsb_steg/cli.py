
# """
# hide_stream
# ~~~~~~~~~~~~~

# This module provides the command line interface for:
#     - hiding and recovering data in .wav files
#     - hiding and recovering data in bitmap (.bmp and .png)
#       files
#     - hiding and recovering data in MP3 files
#     - detecting images which have been modified using the
#       LSB methods.

# Updated to use my custom MP3hide.py for MP3 steganography. cant make mp3stego-lib work. cant do lsb stego in mp3s due to the nature of the format.

# Commands:
#   mp3steg     Handles MP3 steganography operations using MP3hide.py
#   stegdetect  Shows the n least significant bits of image
#   steglsb     Hides or recovers data in and from an image
#   test        Runs a performance test and verifies decoding consistency
#   wavsteg     Hides or recovers data in and from a sound file

# Example usage:

#     MP3:

#     Hide: 
#             python3 cli.py mp3steg -h -i ./test.mp3 -s ./msg.txt -o ./test-steg.mp3
#     Reveal: 
    
#             python3 cli.py mp3steg -r -i c:\Users\abdul\OneDrive\Desktop\dev\IS_Project\hide_stream\lsb_steg\test-steg.mp3 -o msg-mp3.txt 

#     Image:

#     Hide: 
#             python3 cli.py steglsb -h -i test.png -s msg.txt -o test-steg.png
#     Reveal:

#             python3 cli.py steglsb -r -i test-steg.png -o msg.txt     
    
#     Wav:

#     Hide: 
#             python3 cli.py wavsteg -h -i ./test.wav -s ./msg.txt -o ./test-steg.wav
#     Reveal:
#             python3 cli.py wavsteg -r -i ./test-steg.wav -o ./msg-wav.txt -b 22

#             note: "-b" here is the number of bytes to recover. wav steg needs that parameter
    
#     StegDetect:

#             python3 cli.py stegdetect -i ./test.png

#     note: only for images. i outputs an image which shows possible areas in the image that maybe hiding data in them. uses reverse entropy analysis and looks for areas where the entropy is high and randomness is lower than the average

# We sum the least significant n bits of the RGB color channels for each pixel and normalize the result to the range 0-255. 
# This value is then applied to each color channel for the pixel. 
# Where n is the number of least significant bits to show, the following command will save the resulting image, appending "_nLSBs" to the file name.
            


# :copyright: (c) 2015 by R433.
# :license: MIT License, see LICENSE.md for more details.
# """
import logging
import click


import LSBSteg, StegDetect, WavSteg, bit_manipulation
from MP3hide import hide_file_in_mp3, reveal_file_from_mp3

# Enable logging output
logging.basicConfig(format="%(message)s", level=logging.INFO)
log = logging.getLogger("lsb_stego")
log.setLevel(logging.DEBUG)


@click.group()
@click.version_option()
def main() -> None:
    """Console script for HideStream."""


@main.command(context_settings=dict(max_content_width=120))
@click.option("--hide", "-h", is_flag=True, help="To hide data in an image file")
@click.option("--recover", "-r", is_flag=True, help="To recover data from an image file")
@click.option("--analyze", "-a", is_flag=True, default=False, show_default=True,
              help="Print how much data can be hidden within an image")
@click.option("--input", "-i", "input_fp", help="Path to a bitmap (.bmp or .png) image")
@click.option("--secret", "-s", "secret_fp", help="Path to a file to hide in the image")
@click.option("--output", "-o", "output_fp", help="Path to an output file")
@click.option("--lsb-count", "-n", default=2, show_default=True, help="How many LSBs to use", type=int)
@click.option("--compression", "-c", help="1 (best speed) to 9 (smallest file size)", default=1, show_default=True,
              type=click.IntRange(1, 9))
@click.pass_context
def steglsb(ctx: click.Context, hide: bool, recover: bool, analyze: bool, input_fp: str, secret_fp: str, output_fp: str,
            lsb_count: int, compression: int) -> None:
    """Hides or recovers data in and from an image"""
    try:
        if analyze:
            LSBSteg.analysis(input_fp, secret_fp, lsb_count)

        if hide:
            LSBSteg.hide_data(input_fp, secret_fp, output_fp, lsb_count, compression)
        elif recover:
            LSBSteg.recover_data(input_fp, output_fp, lsb_count)

        if not hide and not recover and not analyze:
            click.echo(ctx.get_help())
    except ValueError as e:
        log.debug(e)
        click.echo(ctx.get_help())


@main.command()
@click.option("--input", "-i", "image_path", help="Path to an image")
@click.option("--lsb-count", "-n", default=2, show_default=2, type=int, help="How many LSBs to display")
@click.pass_context
def stegdetect(ctx: click.Context, image_path: str, lsb_count: int) -> None:
    """Shows the n least significant bits of image"""
    if image_path:
        StegDetect.show_lsb(image_path, lsb_count)
    else:
        click.echo(ctx.get_help())


@main.command()
@click.option("--hide", "-h", is_flag=True, help="To hide data in a sound file")
@click.option("--recover", "-r", is_flag=True, help="To recover data from a sound file")
@click.option("--input", "-i", "input_fp", help="Path to a .wav file")
@click.option("--secret", "-s", "secret_fp", help="Path to a file to hide in the sound file")
@click.option("--output", "-o", "output_fp", help="Path to an output file")
@click.option("--lsb-count", "-n", default=2, show_default=True, help="How many LSBs to use", type=int)
@click.option("--bytes", "-b", "num_bytes", help="How many bytes to recover from the sound file", type=int)
@click.pass_context
def wavsteg(ctx: click.Context, hide: bool, recover: bool, input_fp: str, secret_fp: str, output_fp: str,
            lsb_count: int, num_bytes: int) -> None:
    """Hides or recovers data in and from a sound file"""
    try:
        if hide:
            WavSteg.hide_data(input_fp, secret_fp, output_fp, lsb_count)
        elif recover:
            WavSteg.recover_data(input_fp, output_fp, lsb_count, num_bytes)
        else:
            click.echo(ctx.get_help())
    except ValueError as e:
        log.debug(e)
        click.echo(ctx.get_help())


@main.command()
@click.option("--hide", "-h", is_flag=True, help="To hide a file in an MP3 file")
@click.option("--reveal", "-r", is_flag=True, help="To extract a hidden file from an MP3 file")
@click.option("--input", "-i", "input_fp", help="Path to the input MP3 file")
@click.option("--secret", "-s", "secret_fp", help="Path to the file to hide (required for hiding)", default=None)
@click.option("--output", "-o", "output_fp", help="Path to the output file")
@click.pass_context
def mp3steg(ctx: click.Context, hide: bool, reveal: bool, input_fp: str, secret_fp: str, output_fp: str) -> None:
    """Handles MP3 steganography operations using MP3hide.py"""
    try:
        if hide:
            if not secret_fp:
                click.echo("Please provide a file to hide using --secret/-s.")
            else:
                hide_file_in_mp3(input_fp, secret_fp, output_fp)
        elif reveal:
            reveal_file_from_mp3(input_fp, output_fp)
        else:
            click.echo(ctx.get_help())
    except Exception as e:
        log.error(f"Error: {e}")
        click.echo(ctx.get_help())


@main.command()
def test() -> None:
    """Runs a performance test and verifies decoding consistency"""
    bit_manipulation.test()


if __name__ == "__main__":
    main()
