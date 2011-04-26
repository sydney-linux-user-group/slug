#!/bin/bash

git submodule init
git submodule update

cd third_party

curl -O http://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz
tar -zxvf python-dateutil-1.5.tar.gz

curl -O http://pypi.python.org/packages/source/g/gaepytz/gaepytz-2011c.tar.gz
tar -zxvf gaepytz-2011c.tar.gz
rsync -Pa gaepytz-2011c/pytz/ ../pytz/

curl -O http://pypi.python.org/packages/source/M/Markdown/Markdown-2.0.3.tar.gz
tar -zxvf Markdown-2.0.3.tar.gz

curl -O http://www.dalkescientific.com/Python/PyRSS2Gen-1.0.0.tar.gz
tar -zxvf PyRSS2Gen-1.0.0.tar.gz

svn checkout http://python-datetime-tz.googlecode.com/svn/trunk/ python-datetime-tz

svn checkout -r 217 http://svn.osafoundation.org/vobject/trunk/ vobject

./mkzip
