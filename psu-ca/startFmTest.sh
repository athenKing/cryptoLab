kill_process()
{
	for val in $@
	do
		PID=`ps -eaf | grep $val | grep -v grep | awk '{print $2}'`
		if [ "" !=  "$PID" ]
		then
		  echo "killing $val"
		  kill -9 $PID
		else
		  echo "$val process unfound"
		fi
	done
}

kill_process sender.py otExtSender.py fmSender.py

nohup python3 ot/simplest/sender.py > log/sender.txt 2>&1 &
nohup python3 ot/otExtSender.py > log/extSender.txt 2>&1 &
nohup python3 fmSender.py > log/fmSender.txt 2>&1 &

python3 fmReceiver.py

kill_process sender.py otExtSender.py fmSender.py