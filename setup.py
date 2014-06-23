from setuptools import setup

setup(name="skype-bot",
      version="1.0",
      description="Dynamic Skype Bot",
      url="https://github.com/Jake0oo0/SkypePython",
      author="Jake0oo0",
      author_email="jake0oo0andminecraft@gmail.com",
      license="BSD",
      packages=['commands', 'util'],
      entry_points={
          "console_scripts": ["skype=JakeBot:main"]
      },
      classifiers=["Operating System :: POSIX",
                   "Operating System :: Microsoft :: Windows",
                   "Environment :: Console",
                   "Development Status :: 5 - Production/Stable",
                   "Topic :: Internet :: WWW/HTTP",
                   "Topic :: Multimedia :: Sound/Audio",
                   "Topic :: Multimedia :: Video",
                   "Topic :: Utilities"]
)