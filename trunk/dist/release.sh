#!/bin/sh
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

# Did they give a user to sign with?
user=""
case "$1" in
  -u)
    shift
    user="$1"
    shift
    ;;
esac

if test -z "${user}"; then
   # Do they have a default user already set?
   gpg_file=$HOME/.gnupg/gpg.conf
   if test -f $gpg_file; then
      if grep -q '^default-key' $gpg_file; then
         user=`grep '^default-key' $gpg_file | awk '{print $2}'`
         echo "Selected GPG default user of $user"
      fi
   fi
fi

if test -z "${user}"; then
  echo "must pass -u with a gpg id"
  exit 1
fi

cd ..

python setup.py sdist  --formats=gztar,zip
python setup.py bdist_egg

cd dist

./hash-sign.sh -u ${user} *.tar.gz *.zip
./hash-sign.sh -u ${user} *.egg
./hash-sign.sh -u ${user} *.asc
