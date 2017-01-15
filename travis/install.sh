if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Mac OS X
    brew update
    brew install python3
    brew tap Homebrew/python
    pip3 install -U pip wheel
    pip3 install -r requirements.txt
else
    # Linux
    pip3 install -U pip wheel
    pip3 install -r requirements.txt
fi
