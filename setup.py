from setuptools import setup

APP_NAME = "MacBright"
APP = ['app.py']
OPTIONS = {
    'argv_emulation': True, 
    'includes': ['PyQt5'],
    'iconfile': 'images/macbright-yellow.icns',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "MacBright Brightness Slidebar",
        'CFBundleIdentifier': "com.macbright.brightnessslider",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Ron Reiter",
    }    
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)