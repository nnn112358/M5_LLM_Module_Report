https://x.com/washishi/status/1866229894763708587?s=46

#!/bin/bash
cd `dirname $0`
WIFI_IP=`ip address  show dev wlan0 | grep "inet "|awk -F/ '{print $1}'|sed 's/ *inet //'`
if [ _$WIFI_IP != "_" ]
  then
( echo open localhost 10001;
  sleep 1;
  echo '{"request_id":"1","work_id":"audio","action":"setup","object":"audio.setup","data":{"capcard":0,"capdevice":0,"capVolume":0.5,"playcard": 0,"playdevice": 1,"playVolume":0.5}}';
  sleep 1;
  echo '{"request_id":"2","work_id":"tts","action":"setup","object":"tts.setup","data":{"model":"single_speaker_english_fast","response_format":"tts.base64.wav","input":"tts.utf-8.stream","enoutput":true, "enkws": true}}';
  sleep 1;
  echo '{"request_id":"3","work_id":"tts.1001","action":"inference","object":"tts.utf-8", "data":"Wi-Fi IP Address is '$WIFI_IP'"}'
  sleep 10;
  echo '{"request_id":"4","work_id":"sys","action":"reset"}';
) | tee | telnet > talk_ip.log 2>&1
fi
