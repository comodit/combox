#!/bin/bash
echo "Building combox from master"

cd `dirname $0`
cd ..

git checkout master
git pull

NAME="combox"
VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`

./scripts/build-rpm.sh

deploy-trunk /var/lib/mock/epel-6-i386/result/${NAME}-${VERSION}-${RELEASE}.el6.noarch.rpm /public/centos
deploy-trunk /var/lib/mock/fedora-18-i386/result/${NAME}-${VERSION}-${RELEASE}.fc18.noarch.rpm /public/fedora/18

updaterepo
