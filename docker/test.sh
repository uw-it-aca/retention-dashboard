trap 'exit 1' ERR

#
# PRECONDITION: inherited env vars MUST include:
#      DJANGO_APP: django application directory name

# start virtualenv
source bin/activate

function run_test {
    echo "##########################"
    echo "TEST: $1"
    eval $1
}

run_test "pycodestyle ${DJANGO_APP}/ --exclude='migrations,resources,static'"

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

nvm install 14.15
nvm use node
node -v

npm install -g eslint@7.0.0 stylelint@13.3.3 eslint-plugin-vue@latest
npm install

run_test "eslint --ext .js,.vue retention_dashboard/static/retention_dashboard/js/"

run_test "stylelint 'retention_dashboard/**/*.vue' 'retention_dashboard/**/*.scss' "
run_test "coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

ls -lah
# put generaged coverage result where it will get processed
cp .coverage /coverage

exit 0
