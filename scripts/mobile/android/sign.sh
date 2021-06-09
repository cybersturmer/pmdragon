# By this we can sign unsigned apk
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore pmdragon.keystore app-release-unsigned.apk pmdragon