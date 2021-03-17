# Site Source Comparator
## Main objective
This is a script that compares two pages in terms of:
* text content
* number of images
* alt attribute presence
* page title accordance

## Prerequisites
### Docker
Docker version 20.10.2, build 2291f61

## Environmental variables
All environmental variables are defined in *root/.env* file.

## Input
By default, URL pairs should be provided in *root/input/input_data.csv* file.

## Executing the script

**Note:** Make sure that *root/output* folder is present in your filesystem before executing the script

From the root folder:
Build docker image from Dockerfile
```
docker build -t site-source-comparator .
```
Run image as a container, execute script and save results
```
docker run -t -v ${PWD}:/compare-the-page site-source-comparator
```

## Results
By default, results are stored in *site_comparison_results.csv* file in the *root/output* folder.  
Results row's order: {*URL before migration*},{*URL after migration*},{*text content % difference*},{*images number difference*},{*images with missing alt attribute*},{*images with empty alt attribute*},{*page title accordance*}
