 # Details regarding files in the directory:
 buffer_fb.net is a netlist for simulating the unity feedback system
 rc_fb.net is a netlist for simulating the low pass RC feedback system.
 
 ee18btech11026_buffer.py is a python file to plot the ee18btech11026_buffer.dat  
 ee18btech11026_rc_fb.py is a python file to plot the ee18btech11026_rc_fb.dat  
  
 
 ## Instructions for Simulation and plotting the output.
 
 ### Setup
 --> In the terminal use the 'cd' command to move to the directory where .net files and .py files are present.  
 --> Make Sure that all the .net and .py files are present in your present directory . 'ls' command is used to list out the files in the present directory.
 
 
 ### Simulation : 
 -->Enter the following command . This simulates the 'buffer_fb.net' file and creates a 'ee18btech11026_buffer.dat' file.
 ``` 
ngspice buffer_fb.net
```

--> Exit from ngspice cmd line using the following code . This gets you back to the present working directory.
 ``` 
exit
```

--> Enter the following command . This runs  'ee18btech11026_buffer.py'  which plots a plot of 'ee18btech11026_buffer.dat' file
and save it as 'ee18btech11026_spice_result_buffer.pdf'
``` 
python3 ee18btech11026_buffer.py
```


 -->Enter the following command . This simulates the 'rc_fb.net' file and creates a 'ee18btech11026_rc_fb.dat' file.
 ``` 
ngspice rc_fb.net
```
--> Exit from ngspice cmd line using the following code . This gets you back to the present working directory.
 ``` 
exit
```
--> Enter the following command . This runs  'ee18btech11026_rc_fb.py'  which plots a plot of 'ee18btech11026_rc_fb.dat' file
and save it as 'ee18btech11026_spice_result_rc_bf_mag.pdf'
``` 
python3 ee18btech11026_rc_fb.py
```
