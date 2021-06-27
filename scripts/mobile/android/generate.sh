# Let's generate apk first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
APK_BUILD_PATH=$FRONTEND_PATH/dist/cordova/android/apk/release

cd $FRONTEND_PATH || exit 0

# Patching version
npm version patch

# Updating build for mobile application
quasar build -m android

# Signing APK with key
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $FRONTEND_PATH/pmdragon.keystore $APK_BUILD_PATH/app-release-unsigned.apk pmdragon

# Let's optimize this archive
zipalign -v 4 $APK_BUILD_PATH/app-release-unsigned.apk $APK_BUILD_PATH/app-release-signed.apk