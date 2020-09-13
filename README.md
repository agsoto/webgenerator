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
```
Then install the dependencies
```bash
pip install requirements.txt
```

Finally you two choices, the first is to set your driver path in the code when creating an instance of ScreenShutter:
```bash
ScreenShutter(driver_path="path-to-executable-driver")
```
And the second is to [set your enviroment variables](https://zwbetz.com/download-chromedriver-binary-and-add-to-your-path-for-automated-functional-testing/) for Windows and Mac. And for linux you can create a symbolic link `ln -s path-to-executable-driver chromedriver`.
    
## Execution
There's a code example of the use of the generator in the Main.py file. Once you're all set just run:
```bash
> python ./Main
```
