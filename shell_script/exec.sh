#!/bin/bash
OUTPUT=$(ps aux |grep "python")
string='sub-elec110'
#echo ${OUTPUT}

if [[ $OUTPUT =~ $string ]]; then
    echo "run"
else
    echo 'TEST Start!'
    /home/houpc16/djangoenv/myvenv/bin/python3.8 /home/houpc16/djangoenv/shell_script/sub-elec110.py &
    /home/houpc16/djangoenv/myvenv/bin/python3.8 /home/houpc16/djangoenv/shell_script/sub-plug1-1.py &
    /home/houpc16/djangoenv/myvenv/bin/python3.8 /home/houpc16/djangoenv/shell_script/sub-plug1-2.py &
#    source /home/houpc16/djangoenv/myvenv/bin/activate
#    python /home/houpc16/djangoenv/shell_script/sub-elec110.py >/home/houpc16/shell_script/elec110.txt &
#    python /home/houpc16/djangoenv/shell_script/sub-plug1-1.py >/home/houpc16/shell_script/plug1-1.txt &
#    python /home/houpc16/djangoenv/shell_script/sub-plug1-2.py >/home/houpc16/shell_script/plug1-2.txt &
fi

exit 0
