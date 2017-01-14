if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Mac OS X
    brew update
    brew install python3
    brew tap Homebrew/python
    pip3 install -U pip wheel
    brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi
    pip3 install hg+http://bitbucket.org/pygame/pygame
    pip3 install pytest
else
    # Linux
    pip3 install -U pip wheel
    pip3 install -r requirements.txt
fi
