#!/bin/sh

USER=${1}
USERID=${2}
CMD=${3}

usage() {
	echo "usage: ./run-as.sh <USER> <USERID> <CMD>"
}

[ -z ${USER} ] && {
	usage
	echo "[ERROR] USER is not specified"
	exit 1
}  

[ -z ${USERID} ] && {
	usage
	echo "[ERROR] USERID is not specified"
	exit 1
}  

[ -z ${CMD}} ] && {
	usage
	echo "[ERROR] CMD is not specified"
	exit 1
}  

echo "[INFO] Prepare to run '${CMD}' from user: ${USER}/${USERID}"

adduser -D -g '' -u ${USERID} ${USER}
exec su -c "${CMD}" ${USER} 

