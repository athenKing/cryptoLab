
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
		  echo "$val is not running"
		fi
	done
}

kill_process sender.py iknpAlice.py iknpBob.py aliceServer.py

nohup python3 ot/simplest/sender.py > log/sender.txt 2>&1 &
nohup python3 ot/iknpAlice.py > log/iknpAlice.txt 2>&1 &
nohup python3 ot/iknpBob.py > log/iknpBob.txt 2>&1 &
nohup python3 aliceServer.py > log/aliceServer.txt 2>&1 &

echo "Waitting for 4 seconds to make server fully started"
sleep 1
echo "3 seconds remained"
sleep 1
echo "2 seconds remained"
sleep 1
echo "1 seconds remained"
sleep 1
echo "Gonna start client"

python3 bobClient.py

kill_process sender.py iknpAlice.py iknpBob.py aliceServer.py

