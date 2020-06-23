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

wait_for()
{
	echo "Waitting for $1 seconds"
	sleep 1
	for ((i=$1-1; i>=1; i--)); do
		echo "$i seconds remained"
		sleep 1
	done
}


kill_process otEcSender.py

nohup python3 ot/otEcSender.py > log/ecSender.txt 2>&1 &

wait_for 2
python3 ecServer.py

python3 ecClient.py

kill_process otEcSender.py