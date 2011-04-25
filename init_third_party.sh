#!/bin/bash

git submodule init
git submodule update

cd third_party

curl -O http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz
tar -zxvf python-dateutil-1.5.tar.gz

rm -rf pytz
bzr branch lp:pytz

svn checkout http://python-datetime-tz.googlecode.com/svn/trunk/ python-datetime-tz

curl -O http://pypi.python.org/packages/source/i/icalendar/icalendar-2.1.tar.gz
tar -zxvf icalendar-2.1.tar.gz

curl -O http://pypi.python.org/packages/source/M/Markdown/Markdown-2.0.3.tar.gz
tar -zxvf Markdown-2.0.3.tar.gz

./mkzip
