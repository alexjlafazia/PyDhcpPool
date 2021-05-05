from netmiko import ConnectHandler
import pandas as pd
import getpass, re
from datetime import datetime

start_timeall = datetime.now()

####################################################################
#Adds DHCP Option 43
#Including: Turns on and off the DHCP pool to enable configuration
#Changed Option 43 to new controller
####################################################################

def DhcpPool():

    df = pd.read_csv('inventory.csv')

    site = input("Enter site: ")

    layer = input("Enter layer (L2/L3): ")

    iplist = (site.lower()+layer.upper())

    x = (df[iplist])

    usr = input("Enter Username: ")

    PassWD = getpass.getpass()

    for n in (x):

        try:

            if '10' in n:

                ip = n

                start_time = datetime.now()

                net_connect = ConnectHandler(device_type='hp_procurve', ip=ip, username=usr, password=PassWD, fast_cli=True)

                dhcpPool = ["dhcp-server disable", "dhcp-server pool Ruckus-AP-MGMT", "option 43 ip 10.1.32.75", "dhcp-server enable"]

                prompt = net_connect.find_prompt()
                net_connect.send_config_set(dhcpPool)
                net_connect.save_config()
                net_connect.disconnect()

                end_time = datetime.now()
                
                #Prints output of switch
                with open('output.txt', 'r') as output:
                    print(output.read())

                #Notifies user of completion
                hostname = prompt[:-1]
                print("\n")
                print("#" * 30)
                print (hostname + " " + "-" + " " + "Complete")
                print('Duration: {}'.format(end_time - start_time))
                print("#" * 30)

        except TypeError:
            continue
        except:
            print("\n")
            print("#" * 30)
            print ('Failed to connect to ' + ip)
            print("#" * 30)

DhcpPool()

end_timeall = datetime.now()

#Prints overall time of script
print("\n")
print("#" * 30)
print ("Script" + " " + "Complete")
print('Duration: {}'.format(end_timeall - start_timeall))
print("#" * 30)