# Generating build first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
BUILD_PATH=$FRONTEND_PATH/dist/electron
RELEASES_TXT_FILENAME="releases.txt"
RELEASES_JSON_FILENAME="releases.json"

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
echo "$PACKAGE_VERSION" > ./build_number.txt

for directory in */ ; do
  echo ""
  echo "===== Processing ${directory} ====="

  DESTINATION="$BUILD_PATH/$directory"

  echo "Copying Install instruction to folder before zip.."
  if [[ $directory == *"linux"* ]]; then
    echo "Copying install instructions to folder..."
    cp ../../Install-Linux-tar.txt "$DESTINATION"
  fi

  echo "Copying build number file to application folder..."
  cp ./build_number.txt "$DESTINATION"

  echo "Copying LICENSE file to folder before zip it..."
  cp ../../LICENSE "$DESTINATION"

  echo "Zip folder with original name and version..."
  ZIP_FILE_NAME="${directory%/}-${PACKAGE_VERSION}.zip"
  zip -r "$ZIP_FILE_NAME"  "$DESTINATION" > /dev/null 2>&1

  rm -r "$directory"

  # Creating entry with comma separated
  # example: pmdragon-client-linux-x64, 78M, pmdragon-client-linux-x64-1.0.43.zip
  # We will parse this file using python then
  echo "${directory%/},$(du -hs "$ZIP_FILE_NAME" | cut -f 1),${ZIP_FILE_NAME}" >> "$RELEASES_TXT_FILENAME"
done

echo "Creating zips is completed."

# Args build_number releases_txt_path releases_json_path
python ~/projects/pmdragon/tools/scripts/electron/release_master.py  "$PACKAGE_VERSION" "$BUILD_PATH/$RELEASES_TXT_FILENAME" "$BUILD_PATH/$RELEASES_JSON_FILENAME"

echo "Connecting to send files to Source Forge..."
sftp cybersturmer@frs.sourceforge.net << EOF
    cd /home/frs/project/pmdragon
    put "$RELEASES_JSON_FILENAME"
    mkdir "$PACKAGE_VERSION"
    cd "$PACKAGE_VERSION"
    $(for file in *.zip ; do echo "put $file"; done)
    bye
EOF

echo "Files sent."