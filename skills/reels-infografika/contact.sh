#!/bin/zsh
# ./contact.sh grafika.mp4 [шаг_сек=1.5] → contact.jpg — кадр каждые N сек, смотреть Read'ом ПЕРЕД показом
ffmpeg -v error -y -i "$1" -vf "fps=1/${2:-1.5},scale=320:-1,tile=7x7" -frames:v 1 "${1%.*}_contact.jpg" && echo "${1%.*}_contact.jpg"
