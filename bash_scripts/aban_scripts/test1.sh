#!/usr/bin/env bash

sleep 5
touch text
echo 'this is just some text' > text
touch something/somethingelse   # We try to touch a file which can't be done and we get error. Hence, it will be forwarded to stderr
mkdir tmp
cd tmp
sleep 10
expr ${1} / 0 > somefile.txt    # Has an error, let's see what it does!
mkdir innertmp
cd innertmp
touch calculation_result
expr ${1} / ${2} > calculation_result
touch not_included.txt
echo "This file won't be downloaded" > not_included.txt
echo 'Hello everyone!'  # Just something for stdout
sleep 5