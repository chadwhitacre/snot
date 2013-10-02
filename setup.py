from setuptools import setup


setup( author = 'Chad Whitacre'
     , author_email = 'chad@zetaweb.com'
     , description="Snot is colored output from nose. Or, um, py.test."
     , entry_points = { 'nose.plugins.0.10': ['snot = snot:SnotNose']
                      , 'pytest11': ['snot = snot:SnotPyTest']
                       }
     , name='snot'
     , packages=['snot']
     , url = 'https://github.com/whit537/snot'
     , version = '1.0.0'
      )

