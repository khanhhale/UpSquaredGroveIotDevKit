import smbus
import subprocess

#for busnum in range(0,11):
if(True):
   command = '''
   for((c=0x03;c<=0x77;c++)) 
    do 
     for((i=0x00;i<=0x02;i++)) 
      do sudo i2cget -y 2 $c $i w
     done 
   done
   '''
   #command.format(busnum)

   process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
   out, err = process.communicate(command)
   print out

'''
   bus = smbus.SMBus(busnum) # 1 indicates /dev/i2c-1
   for device in range(128):
      try:
         
         #bus.read_byte(device)
         #print(hex(device))

      except: # exception if read_byte fails
         pass
'''
