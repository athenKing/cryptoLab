
kill_all()
{
	PID=`ps -eaf | grep sender.py | grep -v grep | awk '{print $2}'`
	if [[ "" !=  "$PID" ]]; then
	  echo "killing $PID"
	  kill -9 $PID
	fi

	PID=`ps -eaf | grep otExtSender.py | grep -v grep | awk '{print $2}'`
	if [[ "" !=  "$PID" ]]; then
	  echo "killing $PID"
	  kill -9 $PID
	fi

	PID=`ps -eaf | grep fmSender.py | grep -v grep | awk '{print $2}'`
	if [[ "" !=  "$PID" ]]; then
	  echo "killing $PID"
	  kill -9 $PID
	fi
}

kill_all

nohup python3 ot/simplest/sender.py > log/sender.txt 2>&1 &

nohup python3 ot/otExtSender.py > log/extSender.txt 2>&1 &

nohup python3 fmSender.py > log/fmSender.txt 2>&1 &

python3 fmReceiver.py

kill_all