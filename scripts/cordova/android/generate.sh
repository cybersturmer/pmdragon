# How to call it: generate.sh -v patch -b yes
# Let's generate apk first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
BUILD_PATH=$FRONTEND_PATH/dist/capacitor/android/apk/release

while getopts v:b: flag
do
	case "${flag}" in
		v*) version=${OPTARG};;
		b*) build=${OPTARG};;
	esac
done

# Lets define how we map -v param to npm version command
case "${version}" in
	major)
		npm version major;;
	minor)
		npm version minor;;
	patch)
		npm version patch;;
	premajor)
		npm version premajor;;
	preminor)
		npm version preminor;;
	prepatch)
		npm version prepatch;;
	prerelease)
		npm version prerelease;;
	*)
		echo "Skipping versioning...";;
esac


set -ex

cd $FRONTEND_PATH || exit 0

# Updating build for mobile application
case "${build}" in
	yes)
		quasar build -m capacitor -T android;;
	*)
		echo "Skipping build...";;
esac

# Signing APK with key
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $FRONTEND_PATH/pmdragon.keystore $BUILD_PATH/app-release-unsigned.apk pmdragon

# Let's optimize this archive
zipalign -v 4 $BUILD_PATH/app-release-unsigned.apk $BUILD_PATH/app-release-signed.apk
rm $BUILD_PATH/app-release-unsigned.apk
