# Generating build first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
BUILD_PATH=$FRONTEND_PATH/dist/electron
set -ex

cd $FRONTEND_PATH || exit 0

# Updating build for Electron application
quasar build --mode electron --target all --arch all

cd $BUILD_PATH || exit 0
rm -R UnPackaged # We don't need to pack this directory

for directory in */ ; do
  zip -r "${directory%/}.zip"  "$BUILD_PATH/$directory"
done