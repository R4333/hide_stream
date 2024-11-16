# HideStream: LSB Steganography Tool Suite for PNG, BMP, WAV, and MP3 Files

## Group 38 Members

- **21L-5288** Muhammad Abdullah
- **21L-7577** Saad Ali
- **21L-1876** Zeeshan Hamid

## 1. Project Overview

**HideStream** is a versatile LSB steganography tool suite designed to securely embed and detect hidden data within various file formats, including PNG, BMP, WAV, and MP3. The tool suite will consist of four sub-tools: **WavSteg**, **LSBSteg**, **MP3Steg**, and **StegDetect**, each specifically designed to either embed hidden data or detect steganographic content within these formats. The primary objective is to create a robust, efficient, and user-friendly solution for steganography practitioners, researchers, and security enthusiasts.

## 2. Objectives

- **Develop a comprehensive LSB steganography suite** that supports various file types (PNG, BMP, WAV, and MP3).
- **Create individual tools for different formats** (WAV, MP3, PNG, BMP) to ensure optimized performance and functionality.
- **Implement a detection mechanism** to identify and analyze hidden data in these file formats, ensuring users can verify the integrity of media files.
- **Cross-Platform Compatibility** with Windows, macOS, and Linux platforms.

## 3. Sub-Tools

The project will include the following sub-tools:

1. **WavSteg**:
   - Purpose: To embed and extract hidden information within WAV audio files using LSB steganography.
2. **LSBSteg**:
   - Purpose: To apply LSB steganography on image files, particularly PNG and BMP formats.
3. **MP3Steg**:
   - Purpose: Hides data on MP3 files, ensuring data is hidden efficiently without significant impact on audio quality.
4. **StegDetect**:
   - Purpose: To detect and analyze steganographic content across supported file formats.

## 4. Features

### 1. WavSteg Features:

- Embeds secret messages within the LSBs of WAV audio samples.
- Customizable options for the number of bits used per sample to balance between capacity and audio quality.
- Supports extraction of embedded messages and verifies their integrity.
- Preserves audio fidelity while maximizing data hiding capacity.

### 2. LSBSteg Features:

- Enables embedding of hidden text or binary data within the LSBs of PNG and BMP image pixels.
- Supports both RGB and grayscale images, with adjustable bit depth usage.
- Capable of extracting hidden data from steganographic PNG and BMP images.
- Maintains image quality and file size while optimizing storage capacity.

### 3. MP3Steg Features:

- Embeds secret information within MP3 audio frames, optimizing for minimal audio quality loss.
- Adjustable embedding parameters to support various MP3 bit rates and formats.
- Provides message extraction functionality for retrieving and validating hidden data.
- Incorporates techniques to minimize artifacts and preserve original audio quality.

### 4. StegDetect Features:

- Scans PNG, BMP, WAV, and MP3 files for potential steganographic manipulation.
- Uses statistical analysis and pattern recognition to detect modified LSBs.
- Generates detailed reports indicating the likelihood and possible presence of hidden data.
- Compatible with multiple file formats, ensuring comprehensive coverage and reliable analysis.

## 5. Methodology

- **Research and Analysis**:
  - Study existing LSB steganography algorithms and techniques for each file type.
  - Analyze potential vulnerabilities and methods for optimizing steganographic capacity without compromising file quality.
- **Development and Implementation**:
  - Develop each sub-tool separately, ensuring each tool adheres to the format-specific requirements.
  - Integrate the tools into a cohesive suite with a unified user interface (CLI-based initially, with future GUI development).
- **Testing and Validation**:
  - Test the tools extensively with different file sizes and types to measure performance, capacity, and quality trade-offs.
  - Validate the detection tool (StegDetect) with known steganographic files to ensure accurate and reliable analysis.

## 6. Expected Outcomes

- A fully functional suite of tools capable of performing LSB steganography on PNG, BMP, WAV, and MP3 files.
- A detection tool that can analyze and verify the presence of hidden data in media files, with high accuracy and reliability.
- Comprehensive documentation covering installation, usage instructions, and technical details.

## 7. Future Scope

- **GUI Development**: Create a user-friendly graphical interface for non-technical users.
- **Expansion to Other Formats**: Expand steganography support to additional file formats like GIF, JPEG, and other audio/video formats.
- **Machine Learning Integration**: Enhance StegDetect using machine learning models to improve detection accuracy and reduce false positives.

## 8. Conclusion

This project will provide a powerful and versatile LSB steganography tool suite, enabling secure and efficient data hiding and detection across multiple file types. By supporting PNG, BMP, WAV, and MP3 formats, it offers flexibility for various use cases and caters to both technical and non-technical audiences. The proposed sub-tools and future developments ensure the project's relevance and adaptability in the rapidly evolving field of steganography.

```

```
