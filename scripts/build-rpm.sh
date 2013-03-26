#!/bin/bash
NAME="combox"
platforms=(epel-6-i386 fedora-16-i386 fedora-17-i386 fedora-18-i386)

if [ -z $1 ]
then
  VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
else
  VERSION=$1
fi

if [ -z $2 ]
then
  RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`
else
  RELEASE=$2
fi

COMMIT=`git describe --long --match "release*" | awk -F"-" '{print $4}'`

echo ${VERSION}
echo ${RELEASE}

cd `dirname $0`
cd ..

sed "s/#VERSION#/${VERSION}/g" ${NAME}.spec.template > $HOME/rpmbuild/SPECS/${NAME}.spec
sed -i "s/#RELEASE#/${RELEASE}/g" $HOME/rpmbuild/SPECS/${NAME}.spec
sed -i "s/#COMMIT#/${COMMIT}/g" $HOME/rpmbuild/SPECS/${NAME}.spec


tar -cvzf $HOME/rpmbuild/SOURCES/${NAME}-${VERSION}-${RELEASE}.tar.gz * \
--exclude .git \
--exclude build \
--exclude dist \
--exclude deb_dist \
--exclude combox.egg-info


rpmbuild -ba $HOME/rpmbuild/SPECS/${NAME}.spec

if [ -f "/usr/bin/mock" ]
then
for platform in "${platforms[@]}"
do
    /usr/bin/mock -r ${platform} --rebuild $HOME/rpmbuild/SRPMS/${NAME}-${VERSION}-${RELEASE}*.src.rpm
done
fi
