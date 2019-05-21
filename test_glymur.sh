


result=""
versions="0.8.0 0.8.1 0.8.2 0.8.3 0.8.4 0.8.5 0.8.6 0.8.7 0.8.8 0.8.9 0.8.10"

for version in $versions; do
    echo "Test glymur $version"
    pip install --user --upgrade --no-deps glymur==$version
    ./run_tests.py fabio.test.testjpeg2kimage
    if [ $? == 0 ]; then
        test="OK"
    else
        test="ERROR"
    fi
    result="$result\nGlymur $version: $test"
done

printf "$result\n"


