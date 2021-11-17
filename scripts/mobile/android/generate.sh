# How to call it: generate.sh -v patch -b yes
# Let's generate apk first
FRONTEND_PATH=~/projects/pmdragon/pmdragon-client
BUILD_PATH=$FRONTEND_PATH/dist/capacitor/android/apk/release
SCRIPT_PATH="$(pwd)"/scripts/mobile/android

set -ex
cd $FRONTEND_PATH || exit 0

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
apksigner sign --ks "$SCRIPT_PATH"/pmdragon.keystore --ks-pass file:"$SCRIPT_PATH"/password.txt --v1-signing-enabled true --v2-signing-enabled true $BUILD_PATH/app-release-unsigned-packed.apk
cp $BUILD_PATH/app-release-unsigned-packed.apk $BUILD_PATH/app-release-signed-packed.apk
