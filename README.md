# WeChat multilateration

This Frida script is part of an experiment to locate WeChat users using [multilateration](https://en.wikipedia.org/wiki/True-range_multilateration). For more information, see [this Observable notebook](https://observablehq.com/@ltrgoddard/wechat-multilateration).

## Requirements

- Python 3
- Frida
- An Android phone connected via USB, with WeChat installed and the screen unlocked

## Usage

`./collect-data.py [number of points to sample] [bounding box in min_lon,min_lat,max_lon,max_lat format] > data.jsonl`
