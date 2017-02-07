for i in 161 162 163 165 166 171 173 177 178
do
	ip=10.121.1.$i
	echo "------ $ip -- `ssh root@$ip "hostname"` ------"
	#scp /etc/ntp.conf root@$ip:/etc/ntp.conf
	ssh root@$ip "date"
	#ssh root@$ip "service ntp status"
	ssh root@$ip "ntpq -p"
done
