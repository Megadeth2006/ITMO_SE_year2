#!/bin/sh

set -eu

root="/home/studs/s465635/opi/lab2"
zips="$root/zips"
commits="$root/commits"
tmp="$root/tmp_prepare_commits"

die() {
    echo "Ошибка: $*" >&2
    exit 1
}

[ -d "$zips" ] || die "не найдена папка с архивами: $zips"

rm -rf "$commits"
rm -rf "$tmp"

mkdir -p "$commits"
mkdir -p "$tmp"

i=0
while [ "$i" -le 56 ]; do
    zipPath="$zips/commit$i.zip"
    dst="$commits/commit$i"
    tempDir="$tmp/commit$i"

    [ -f "$zipPath" ] || die "не найден архив: $zipPath"

    echo "Распаковка commit$i.zip"

    rm -rf "$dst"
    rm -rf "$tempDir"

    mkdir -p "$dst"
    mkdir -p "$tempDir"

    tar -xf "$zipPath" -C "$tempDir" || die "не удалось распаковать: $zipPath"

    count=$(find "$tempDir" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')
    firstItem=$(find "$tempDir" -mindepth 1 -maxdepth 1 | sed -n '1p')

    if [ "$count" -eq 1 ] && [ -d "$firstItem" ]; then
        sourceDir="$firstItem"
    else
        sourceDir="$tempDir"
    fi

    find "$sourceDir" -mindepth 1 -maxdepth 1 ! -name ".git" -exec cp -R -p {} "$dst" \;

    i=$((i + 1))
done

rm -rf "$tmp"

echo "Готово. Архивы распакованы в папку: $commits"