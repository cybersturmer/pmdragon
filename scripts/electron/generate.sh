# Generating build first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
BUILD_PATH=$FRONTEND_PATH/dist/electron
set -ex

cd $FRONTEND_PATH || exit 0

# Updating build for Electron application
quasar build --mode electron --target all --arch all

cd $BUILD_PATH || exit 0

# We don't need to pack this directory
rm -R UnPackaged

for directory in */ ; do
  # Copy Install instruction to folder before zip
  if [[ $directory == *"linux"* ]]; then
    cp ../../Install-Linux-tar.txt "$BUILD_PATH/$directory"
  fi

  # Copy LICENSE file to folder before zip it
  cp ../../LICENSE "$BUILD_PATH/$directory"

  # Zip folder with original name
  zip -r "${directory%/}.zip"  "$BUILD_PATH/$directory"
done