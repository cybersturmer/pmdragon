# Generating build first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
SCRIPTS_PATH=~/projects/pmdragon/tools/scripts/electron
BUILD_PATH=$FRONTEND_PATH/dist/electron
INSTALLERS_PATH="installers"
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

mkdir installers

for directory in */ ; do
  if [[ "$directory" == 'installers/' ]]; then
    continue
  fi

  echo ""
  echo "===== Processing ${directory} ====="

  DESTINATION="$BUILD_PATH/$directory"

  echo "Copying Install instruction to folder before zip.."
  if [[ $directory == *"linux"* ]]; then
    echo "Copying install instructions to folder..."
    cp ../../Install-Linux-tar.txt "$DESTINATION"

    echo -n "Creating deb file for Debian based Linux OS..."

    case $directory in
      "pmdragon-client-linux-ia32/")
        echo "$directory"
        ORIG_DEB_FILENAME="pmdragon-client_${PACKAGE_VERSION}_i386.deb"
        NEW_DEB_FILENAME="pmdragon-client-i386.deb"
        electron-installer-debian --src "$directory" --arch i386 --config "${FRONTEND_PATH}/deb_config.json"
        mv "./$INSTALLERS_PATH/$ORIG_DEB_FILENAME" "./$INSTALLERS_PATH/$NEW_DEB_FILENAME"
        echo "Debian i386 .deb,$(du -hs "./$INSTALLERS_PATH/$NEW_DEB_FILENAME" | cut -f 1),${NEW_DEB_FILENAME}" >> "$RELEASES_TXT_FILENAME"
        ;;
      "pmdragon-client-linux-armv7l/")
        echo "$directory"
        ORIG_DEB_FILENAME="pmdragon-client_${PACKAGE_VERSION}_arm.deb"
        NEW_DEB_FILENAME="pmdragon-client-arm.deb"
        electron-installer-debian --src "$directory" --arch arm --config "${FRONTEND_PATH}/deb_config.json"
        mv "./$INSTALLERS_PATH/$ORIG_DEB_FILENAME" "./$INSTALLERS_PATH/$NEW_DEB_FILENAME"
        echo "Debian arm .deb,$(du -hs "./$INSTALLERS_PATH/$NEW_DEB_FILENAME" | cut -f 1),${NEW_DEB_FILENAME}" >> "$RELEASES_TXT_FILENAME"
        ;;
      "pmdragon-client-linux-arm64/")
        echo "$directory"
        ORIG_DEB_FILENAME="pmdragon-client_${PACKAGE_VERSION}_arm64.deb"
        NEW_DEB_FILENAME="pmdragon-client-arm64.deb"
        electron-installer-debian --src "$directory" --arch arm64 --config "${FRONTEND_PATH}/deb_config.json"
        mv "./$INSTALLERS_PATH/$ORIG_DEB_FILENAME" "./$INSTALLERS_PATH/$NEW_DEB_FILENAME"
        echo "Debian arm64 .deb,$(du -hs "./$INSTALLERS_PATH/$NEW_DEB_FILENAME" | cut -f 1),${NEW_DEB_FILENAME}" >> "$RELEASES_TXT_FILENAME"
        ;;
      "pmdragon-client-linux-x64/")
        echo "$directory"
        ORIG_DEB_FILENAME="pmdragon-client_${PACKAGE_VERSION}_amd64.deb"
        NEW_DEB_FILENAME="pmdragon-client-amd64.deb"
        electron-installer-debian --src "$directory" --arch amd64 --config "${FRONTEND_PATH}/deb_config.json"
        mv "./$INSTALLERS_PATH/$ORIG_DEB_FILENAME" "./$INSTALLERS_PATH/$NEW_DEB_FILENAME"
        echo "Debian x64 .deb,$(du -hs "./$INSTALLERS_PATH/$NEW_DEB_FILENAME" | cut -f 1),${NEW_DEB_FILENAME}" >> "$RELEASES_TXT_FILENAME"
        ;;
      *)
        echo "skipped"
    esac

  fi

  echo "Copying build number file to application folder..."
  cp ./build_number.txt "$DESTINATION"

  echo "Copying LICENSE file to folder before zip it..."
  cp ../../LICENSE "$DESTINATION"

  echo "Zip folder with original name and version..."
  ZIP_FILE_NAME="${directory%/}.zip"
  zip -r "$ZIP_FILE_NAME"  "$DESTINATION" > /dev/null 2>&1

   rm -r "$directory"

  # Creating entry with comma separated
  # example: pmdragon-client-linux-x64, 78M, pmdragon-client-linux-x64-1.0.43.zip
  # We will parse this file using python then
  echo "${directory%/},$(du -hs "$ZIP_FILE_NAME" | cut -f 1),${ZIP_FILE_NAME}" >> "$RELEASES_TXT_FILENAME"
done

echo "Creating zips is completed."

# Args build_number releases_txt_path releases_json_path
python "$SCRIPTS_PATH/release_master.py"  "$PACKAGE_VERSION" "$BUILD_PATH/$RELEASES_TXT_FILENAME" "$BUILD_PATH/$RELEASES_JSON_FILENAME"

echo "Connecting to send files to Source Forge..."
sftp cybersturmer@frs.sourceforge.net << EOF
    cd /home/frs/project/pmdragon
    put "$RELEASES_JSON_FILENAME"
    mkdir "$PACKAGE_VERSION"
    cd "$PACKAGE_VERSION"
    $(for file in *.zip ; do echo "put $file"; done)
    lcd installers
    $(for file in *.deb ; do echo "put $file"; done)
    bye
EOF

echo "Files sent."