#!/usr/bin/env bash
set -Eeuo pipefail

# No command means "start Jupyter".
if [ "$#" -eq 0 ]; then
    set -- jupyter
fi

case "$1" in
    jupyter|sage-jupyter)
        shift
        exec sage -n jupyter \
            --no-browser \
            --ip=0.0.0.0 \
            --port=8888 \
            "$@"
        ;;

    sage)
        shift
        exec sage "$@"
        ;;

    python|sage-python)
        shift
        exec sage -python "$@"
        ;;

    bash|sh)
        exec "$@"
        ;;

    *.sage|*.py)
        exec sage "$@"
        ;;

    *)
        exec "$@"
        ;;
esac
