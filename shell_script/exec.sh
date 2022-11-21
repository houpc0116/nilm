#!/bin/bash
OUTPUT=$(ps aux |grep "python")
string='sub-elec110'
#echo ${OUTPUT}

if [[ $OUTPUT =~ $string ]]; then
    echo "run"
else
    echo 'TEST Start!'
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-elec110.py &
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-plug1-1.py &
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-plug1-2.py &
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-plug1-3.py &
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-elec220.py &
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-plug3-1.py &
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-plug3-2.py &
    /home/awinlab2/myvenv/bin/python3 /home/awinlab2/shell_script/sub-plug3-3.py &
#    source /home/houpc16/djangoenv/myvenv/bin/activate
#    python /home/houpc16/djangoenv/shell_script/sub-elec110.py >/home/houpc16/shell_script/elec110.txt &
#    python /home/houpc16/djangoenv/shell_script/sub-plug1-1.py >/home/houpc16/shell_script/plug1-1.txt &
#    python /home/houpc16/djangoenv/shell_script/sub-plug1-2.py >/home/houpc16/shell_script/plug1-2.txt &
fi

exit 0
