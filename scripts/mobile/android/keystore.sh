# Generating key for signing android application
# https://docs.oracle.com/javase/8/docs/technotes/tools/unix/keytool.html
keytool -genkeypair -v -keystore pmdragon.keystore -alias pmdragon -keyalg RSA -keysize 2048 -validity 10000
