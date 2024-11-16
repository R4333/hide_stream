from mp3stego import Steganography


def hide_message(input_mp3, output_mp3, message):
    """Hide a message in an MP3 file."""
    stego = Steganography(quiet=True)
    stego.hide_message(input_mp3, output_mp3, message)


def reveal_message(input_mp3, output_txt):
    """Reveal a hidden message from an MP3 file."""
    stego = Steganography(quiet=True)
    stego.reveal_massage(input_mp3, output_txt)


def encode_wav_to_mp3(input_wav, output_mp3, bitrate=320):
    """Encode a WAV file into an MP3 file."""
    stego = Steganography(quiet=True)
    stego.encode_wav_to_mp3(input_wav, output_mp3, bitrate)


def decode_mp3_to_wav(input_mp3, output_wav):
    """Decode an MP3 file into a WAV file."""
    stego = Steganography(quiet=True)
    stego.decode_mp3_to_wav(input_mp3, output_wav)


def clear_hidden_message(input_mp3, output_mp3):
    """Clear a hidden message from an MP3 file."""
    stego = Steganography(quiet=True)
    stego.clear_file(input_mp3, output_mp3)
