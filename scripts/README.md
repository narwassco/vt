# open-africa-uploader
This module will upload the file to [openAFRICA](https://open.africa) website

## Usage

First of all, please register your `CKAN_API_KEY` at secrets of Github settings.

```
pipenv install 
pipenv shell

python upload2openafrica.py --key ${CKAN_API_KEY} --pkg {your package url} --title {your package title} --file {relative path} --desc {description for file}
```

## Example

```bash
python upload2openafrica.py \
--key ${CKAN_API_KEY} \
--org "water-and-sanitation-corporation-ltd-wasac"
--pkg rw-water-vectortiles \
--title "Vector Tiles for rural water supply systems in Rwanda" \
--file ../data/rwss.mbtiles \
--desc "mbtiles format of Mapbox Vector Tiles which was created by tippecanoe."
```

## Using Github Action to upload

First of all, please create shell script for uploading.

```bash
vi upload_mbtiles.sh
```
```bash
#!/bin/bash

pipenv run python upload2openafrica.py \
  --key ${CKAN_API_KEY} \
  --org "water-and-sanitation-corporation-ltd-wasac"
  --pkg rw-water-vectortiles \
  --title "Vector Tiles for rural water supply systems in Rwanda" \
  --file ../data/rwss.mbtiles \
  --desc "mbtiles format of Mapbox Vector Tiles which was created by tippecanoe."
```

```bash
chmod +x upload_mbtiles.sh
```

Then, please create Github workflow file like the below example.

```bash
vi .github/workflows/python-openafrica.yml
```

```yaml
name: openAFRICA upload

on:
  push:
    branches: [ master ]
    paths:
      - "data/**"

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies

      run: |
        cd scripts
        pip install pipenv
        pipenv install
    - name: upload to openAFRICA
      env:
        CKAN_API_KEY: ${{secrets.CKAN_API_KEY}}
      run: |
        cd scripts
        ./upload_mbtiles.sh
```

Don't forget to register your CKAN API Key on your setting page of Github!

Enjoy!