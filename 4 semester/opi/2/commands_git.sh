red="red <red.tune-it.ru>" # первый пользователь
blue="blue <blue.tune-it.ru>" # второй пользователь

commit() { # функция, отвечающая за коммит
    rm -rf ./*

    cp -r ../commits/commit$1/* .

    git add .
    git commit --allow-empty -m "r$1" --author="$2"
}

rm -rf git_dir
mkdir git_dir
cd git_dir
git init

# подготовка директории

git checkout -b "r0"
commit 0 "$red"

git checkout -b "r1"
commit 1 "$red"

git checkout -b "r2"
commit 2 "$blue"

git checkout -b "r3"
commit 3 "$blue"
commit 4 "$blue"

git checkout "r0"
commit 5 "$red"

git checkout -b "r6"
commit 6 "$red"

git checkout "r0"
commit 7 "$red"

git checkout "r1"
commit 8 "$red"

git checkout -b "r9"
commit 9 "$blue"

git checkout "r2"
commit 10 "$blue"
commit 11 "$blue"

git checkout "r3"
commit 12 "$blue"

git checkout "r2"
commit 13 "$blue"
commit 14 "$blue"

git checkout "r0"
commit 15 "$red"
commit 16 "$red"

git checkout "r1"
commit 17 "$red"

git checkout "r3"
commit 18 "$blue"

git checkout "r1"
commit 19 "$red"
commit 20 "$red"

git checkout "r2"
commit 21 "$blue"

git checkout "r9"
commit 22 "$blue"

git checkout "r2"
commit 23 "$blue"

git checkout "r0"
commit 24 "$red"

git checkout "r3"
git merge --no-commit -s ours "r6"
commit 25 "$blue"

git checkout -b "r26"
commit 26 "$red"

git checkout "r1"
commit 27 "$red"

git checkout "r3"
commit 28 "$blue"

git checkout "r2"
commit 29 "$blue"

# r30 и r33 идут от r6

git checkout "r6"
git checkout -b "r30"
commit 30 "$red"

git checkout "r26"
commit 31 "$red"

git checkout "r9"
commit 32 "$blue"

git checkout "r30"
commit 33 "$red"

git checkout "r26"
git merge --no-commit -s ours "r30"
commit 34 "$red"

git checkout "r2"
commit 35 "$blue"

git checkout "r1"
commit 36 "$red"
commit 37 "$red"

git checkout "r0"
commit 38 "$red"

git checkout "r3"
commit 39 "$blue"

git checkout "r26"
commit 40 "$red"

git checkout "r9"
commit 41 "$blue"

git checkout "r1"
commit 42 "$red"

git checkout "r3"
commit 43 "$blue"

git checkout "r2"
commit 44 "$blue"

git checkout "r0"
commit 45 "$red"

git checkout "r2"
commit 46 "$blue"

git checkout "r3"
git merge --no-commit -s ours "r2"
commit 47 "$blue"

git checkout "r0"
commit 48 "$red"

git checkout "r26"
commit 49 "$red"

git checkout "r3"
commit 50 "$blue"
commit 51 "$blue"

git checkout "r26"
git merge --no-commit -s ours "r3"
commit 52 "$red"

git checkout "r1"
git merge --no-commit -s ours "r26"
commit 53 "$red"

commit 54 "$red"

git checkout "r9"
git merge --no-commit -s ours "r1"
commit 55 "$blue"

git checkout "r0"
git merge --no-commit -s ours "r9"
commit 56 "$red"

# проверка результата

git log --graph --oneline --decorate --all --topo-order
git log --graph --oneline --decorate --all --topo-order > git-graph.txt
git log --pretty=format:"%h %d %an %s" --all --topo-order > git-commits.txt