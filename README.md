# WebGenerator
Generate easily probabilistic dataset of web interfaces and content. The datasetter allows you to generate HTML files, their corresponding screenshots and a JSON file with the labeled HTML elements. This way you can train supervised and non-supervised models. You can also set probabilities and options generation of the batch to suit your needs.

<img src="https://imgur.com/a6o62Da.png" alt="Example 3" width="250">

This development is kindly supported by the awesome [SDAS Group](https://www.sdas-group.com/).

## Some selected examples
<img src="https://i.imgur.com/rlsanuU.png" alt="Example 1" width="300">
<img src="https://i.imgur.com/GnxOmgp.png" alt="Example 2" width="300">
<img src="https://i.imgur.com/vELUSQZ.png" alt="Example 3" width="300">

A full dataset of 1000 elements with 800x600 size generated with the tool can be [shown here](https://github.com/agsoto/webgenerator/tree/master/ExampleDataSetWebGenerator) and can be  [downloaded here](https://drive.google.com/file/d/1qjjkD57NaW9l8Oa16icjYRCgn2TDa0bW/view?usp=sharing). In this dataset you will find a folder with CSS, js, HTML files, image folders and JSON files. The html directory has html files rw prefix with the name (rw_0.html, row_1.html,.., row_n.html). Inside the CSS folder, the Bootstrap distribution file with the web page's color palette and another file with the necessary CSS rules for the sidebar and extra required styling. The js folder contains the needed JQuery and Bootstraps Javascript files.



# Requirements
* Python >= 3.7 ([download here](https://www.python.org/downloads/))
* Pip >= 20.0.2 ([installation instructions here](https://pip.pypa.io/en/stable/installing/))
* Chrome / Chromium browser
* Chrome driver

## Browser and driver
The chrome driver allows Web Generator manage instances of the browser to take the screenshots and create tags annotations of the inner html elements.

1. If you have a Chrome or Chromium browser installed you can skip this step. Otherwise
 you can download either a setup or a zip file with the software. In this case we recommend downloading
 Chromium from [this builds website](https://chromium.woolyss.com/). You should select "Archive" (Zip folder) or Installer.
2. Next you have to download the Chrome Driver from [here](https://chromedriver.chromium.org/). **Make sure
 you have SAME VERSIONS for the driver and the browser**. Once downloaded the driver, extract and put the file in your browser's executable folder. If you installed Chrome the path could be `C:/Program Files/Google/Chrome/Application`.

 You can always check the official [documentation of Selenium](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver)

# Installation
Simply git clone this repository or download the zip folder: 
```bash
git clone https://github.com/agsoto/webgenerator.git
cd webgenerator
```
Then install the dependencies
```bash
pip install -r requirements.txt
```
Since screen capturing feature depends on Selenium Driver, you should add the path to the system's enviroment variables. Look how to [set your enviroment variables](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/) on Windows and Mac. Or if your'e using linux you can create a symbolic link: 
`ln -s path-to-executable-driver chromedriver`.

However if you don't want to add an eviroment variable, when using the class ScreenShutter, you can set the path to the driver this way:
```bash
ScreenShutter(driver_path="path-to-executable-driver")
```
This optional parameter could be set as it appears in [line 18 of Main.py](https://github.com/agsoto/webgenerator/blob/master/Main.py#L18) file.

    
## Execution
There's a code example of the use of the generator in the [Main.py](https://github.com/agsoto/webgenerator/blob/master/Main.py) file. Once you're all set just run:
```bash
python ./Main

```

## Potential Applications

This dataset has a potential applications for will generate GUI web,       [here](https://github.com/agsoto/webgenerator/tree/master/PotentialApplications) you will find three deep learning models examples.

- GAN: To generate GUI web images through web generator images.
- Fast RCNN: To detect components in web page's images.
- Pix2Pix: To generate GUI web images through images's edges (canny mask).

### GAN

<img src='https://raw.githubusercontent.com/agsoto/webgenerator/master/PotentialApplications/Images/gan.png' />

### Faster RCNN

<img src='https://raw.githubusercontent.com/agsoto/webgenerator/master/PotentialApplications/Images/frcnn.png' width=60%/>

### Pix2Pix

<img src='https://raw.githubusercontent.com/agsoto/webgenerator/master/PotentialApplications/Images/p2p.png' width=60%/>

# Generation Probabilities
The parameters for the WebLayoutProbabilities object (that is used for the generation), are described below.
| Param # | Name               | Type    | Description                                                                                                                             |
|---------|--------------------|---------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 1       | with_sidebar_p     | float   | Probability that the Sidebar is present                                                                                                 |
| 2       | with_header_p      | float   | Probability that the Header is present                                                                                                  |
| 3       | with_navbar_p      | float   | Probability that the Navbar is present                                                                                                  |
| 4       | with_footer_p      | float   | Probability that the Footer is present                                                                                                  |
| 5       | layouts_p          | list[4] | List with the probabilities for each possible layout. The sum of the probabilities should be 1                                         |
| 6       | boxed_body_p       | float   | Probability that the page's Body is boxed inside a container                                                                            |
| 7       | big_header_p       | float   | Probability of having a big header (A big header is considered 50% or more of the screen height)                                        |
| 8       | sidebar_first_p    | float   | Probability of the Sidebar being at the left side of the Body                                                                           |
| 9       | navbar_first_p     | float   | Probability of the Navbar being above the header                                                                                        |
| 10      | bg_color_classes_p | list[3] | List with the probabilities for the combination of CSS Bootstrap's background color classes. The sum of the probabilities should be 1  |