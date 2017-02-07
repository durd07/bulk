for i in 161 162 163 165 166 171 172 173 177 178
do
	ip=10.121.1.$i
	echo "------ $ip -- `ssh root@$ip "hostname"` ------"
	#scp /etc/ntp.conf root@$ip:/etc/ntp.conf
	#ssh root@$ip "service ntp restart"
	#ssh root@$ip "ntpstat"
	ssh root@$ip "date"
done
