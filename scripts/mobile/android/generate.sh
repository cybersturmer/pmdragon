# How to call it: sh ./generate.sh -v patch -b yes
# Let's generate apk first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
BUILD_PATH=$FRONTEND_PATH/dist/capacitor/android/apk/release
BASE_PATH=~/projects/pmdragon/tools/scripts/mobile/android

set -ex
cd $FRONTEND_PATH || exit 0

# Check if keystore file is present
if [ ! -f "$BASE_PATH/pmdragon.keystore" ]; then
	ls "$BASE_PATH"
	echo "File $BASE_PATH/pmdragon.keystore does not exist, exiting..."
	exit 0
fi

# Check if password file exist
if [ ! -f "$BASE_PATH/password.txt" ]; then
	echo "File $BASE_PATH/password.txt does not exist, exiting..."
	exit 0
fi


# And flag all given arguments
while getopts v:b: flag
do
	case "${flag}" in
		v*) version=${OPTARG};;
		b*) build=${OPTARG};;
	esac
done

# Lets define how we map -v param to npm version command
case "${version}" in
	major|minor|patch|premajor|preminor|prepatch|prerelease)
		npm version "${version}";;
	*)
		echo "Skipping versioning...";;
esac




# Updating build for mobile application
case "${build}" in
	yes)
		quasar build -m capacitor -T android;;
	*)
		echo "Skipping build...";;
esac

# Let's optimize this archive
zipalign -v 4 $BUILD_PATH/app-release-unsigned.apk $BUILD_PATH/app-release-unsigned-packed.apk

# Signing APK with key
apksigner sign --ks "$BASE_PATH"/pmdragon.keystore --ks-pass file:"$BASE_PATH"/password.txt --v1-signing-enabled true --v2-signing-enabled true $BUILD_PATH/app-release-unsigned-packed.apk
cp $BUILD_PATH/app-release-unsigned-packed.apk $BUILD_PATH/app-release-signed-packed.apk
