#!/bin/bash
#
# use case:
#   to backup dir /path/to/dir/ rotatedly to /path/to/dir.{1..5}/ with rsync,
#   run as: ./rsync-dir-rotate.sh /path/to/dir/ 5

path=${1%/}
num_rotates=${2:-5}

#exec &> /tmp/rotate-`date +%F`.log

[ ! -d "${path}" ] && {
  echo "Usage: ${0} <path> [num-rotates]"
  echo "Invalid dir: ${path}"
  exit 1
}

echo "Rotating ${path} with ${num_rotates} rotates..."

i=$(( ${num_rotates} - 1 ))
while (( $i > 0 )); do
  j=$(( i+1 ))
  k="${path}.${i}/"
  [ -d "$k" ] && rsync -ah --stats --delete "${k}" "${path}.${j}"
  (( i=i-1 ))
done
rsync -ah --stats --delete ${path}/ ${path}.1
