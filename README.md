# Email od Andrzeja

Jest dodany parametr umożliwiający korekcję zniekształceń obrazu do realtime-panorama-stitching, ale to w praktyce nie zadziała, bo czas przetwarzania korekcji jest za długi i cały algorytm nie będzie działał w czasie rzeczywistym (nie podając parametrów związanych z korekcją algorytm realjtime-panorama-stitching działa bez korekcji). 

Wywołując program można podać albo adresy kamer IP albo indeksy kamer lokalnych albo nazwy plików wideo. Niestety te pliki z hokeja w mp4 nie działają, ale po zamianie na pliki *.mov to wszystko jest OK, więc być może wymaga to jeszcze jakiejś konfiguracji driverów. Jednak to jest już poza zakresem naszych działań. Zawsze możecie podpiąć kamery IP lub kamery lokalne lub przekonwertować mp4 do mov.

Plik konfiguracyjny korekty zniekształceń obrazu (JSON) generowany jest przez program calibrate i jest on parametrem dla undistort (sprawdzenie wyniku korekcji) oraz realtime-panorama-stitching.

Opis parametrów poszczególnych programów jest w README.md.

# Java

## Open CV (Scala)

### Install Open CV on Mac

- `xcode-select --install`
- `brew install ant`
- `brew edit opencv`
- In the text editor that will open, change the line: `-DBUILD_opencv_java=OFF` in `-DBUILD_opencv_java=ON`
- `brew install --build-from-source opencv`

It should be installed in: `/usr/local/Cellar/opencv/4.1.2`

> Na razie to nie działa

# Python

## Calibrate fisheye



**calibrate** - program for camera calibration
`calibrate -row <int> -col <int> -calibrationDataFile <string>`

where:

- `row` & `col` - number of rows and colums of chessboard patern
- `calibrationDataFile` - output json file name with calibration parameters
- calibration images should be in the `./image` folder

**undistort** - DEMO program for visualization of the undistortion result of calibration algorithm
`undistort -imgHeight <int> -imgWidth <int> -calibrationDataFile <string>`

where:

- `imgHeight` & `imgWidth` - size of the output image
- `calibrationDataFile` - input json file name with calibration parameters
- the first image in the `./image` folder will be undistorted


[Medium tutorial - part 1](https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0), [Medium tutorial - part 2](https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-part-2-13990f1b157f)

## Image stitching
It works without any changes.

This is from: https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/

## Realtime panorama stitching

**realtime_stitching** - two images stitching in a real-time

`realtime_stitching -src [file | cam] -leftStream <int | string> -rightStream <int | string> -imgHeight <int> -imgWidth <int> -calibrationDataFile <string>`

where:

- `src` - video stream source: file vs. local camera (0, 1) or IP camera (http address)
- `leftStream`, `rightStream` - file names or local camera ids (0, 1) or http addresses,
- `imgHeight` & `imgWidth` - size of the output image
- `calibrationDataFile` - input json file name with calibration parameters


This is from: https://www.pyimagesearch.com/2016/01/25/real-time-panorama-and-image-stitching-with-opencv/

### Requirements

`pip install opencv-contrib-python`
