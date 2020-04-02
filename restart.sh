dos2unix *.sh
chmod +x *.sh
ps -ef | grep django3template | grep -v grep | awk '{print $2}' | xargs kill -9
cd /opt/django3template
if [ ! -d "./venv" ];then
    virtualenv -p python3 venv
fi
source ./venv/bin/activate
pip3 install -r requirements.txt
nohup gunicorn --config=./gunicorn.conf.py django3template.wsgi:application > nohup.out 2>&1 &
ps -aux | grep django3template