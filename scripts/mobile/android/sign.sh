# By this we can sign unsigned apk
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
APK_BUILD_PATH=$FRONTEND_PATH/dist/cordova/android/apk/release

jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $FRONTEND_PATH/pmdragon.keystore $APK_BUILD_PATH/app-release-unsigned.apk pmdragon