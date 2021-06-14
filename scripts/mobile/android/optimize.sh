# Let's optimize our APK before attaching it to Google Play
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
APK_BUILD_PATH=$FRONTEND_PATH/dist/cordova/android/apk/release

zipalign -v 4 $APK_BUILD_PATH/app-release-unsigned.apk $APK_BUILD_PATH/app-release-signed.apk