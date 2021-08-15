# Generating build first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
BUILD_PATH=$FRONTEND_PATH/dist/electron

cd $FRONTEND_PATH || exit 0

# Updating build for Electron application
quasar build --mode electron --target all --arch all

PACKAGE_VERSION=$(cat package.json \
  | grep version \
  | head -1 \
  | awk -F: '{ print $2 }' \
  | sed 's/[",]//g' | xargs)

echo "Building version: v${PACKAGE_VERSION}..."

cd $BUILD_PATH || exit 0

# We don't need to pack this directory
rm -R UnPackaged

# Add build number to text file
echo "$PACKAGE_VERSION" > ../../build_number.txt

for directory in */ ; do
  echo ""
  echo "===== Processing ${directory} ====="

  # Creating entry with comma separated
  # example: pmdragon-client-linux-x64, pmdragon-client-linux-x64-1.0.43.zip
  # We will parse this file using python then
  echo "${directory%/},${directory%/}-${PACKAGE_VERSION}.zip" >> ../releases.txt

  echo "Copying Install instruction to folder before zip.."
  if [[ $directory == *"linux"* ]]; then
    echo "Copying install instructions to folder..."
    cp ../../Install-Linux-tar.txt "$BUILD_PATH/$directory"
  fi

  echo "Copying build number file to application folder..."
  cp ../../build_number.txt "$BUILD_PATH/$directory"

  echo "Copying LICENSE file to folder before zip it..."
  cp ../../LICENSE "$BUILD_PATH/$directory"

  echo "Zip folder with original name and version..."
  zip -r "${directory%/}-${PACKAGE_VERSION}.zip"  "$BUILD_PATH/$directory" > /dev/null 2>&1
done
