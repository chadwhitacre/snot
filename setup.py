from setuptools import setup


setup( author = 'Chad Whitacre'
     , author_email = 'chad@zetaweb.com'
     , description="Snot is colored output from nose."
     , entry_points = { 'nose.plugins.0.10': ['snot = snot:Snot'] }
     , name='snot'
     , py_modules=['snot']
     , url = 'https://github.com/whit537/snot'
     , version = '0.1'
      )

