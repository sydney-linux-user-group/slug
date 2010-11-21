#!/bin/bash

git submodules init
git submodules update

cd third_party

curl -O http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz
tar -zxvf python-dateutil-1.5.tar.gz

bzr branch lp:pytz

svn checkout http://python-datetime-tz.googlecode.com/svn/trunk/ python-datetime-tz
