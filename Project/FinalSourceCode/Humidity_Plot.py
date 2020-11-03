#Import the relevant library files
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from datetime import datetime

#Initialise variable values
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
def animate(i):
    #CSV file which is getting written parallely
    ftemp = '/home/pi/SourceCode/humid.csv'
    fh = open(ftemp)
    xs=[]
    ys=[]
    for line in fh:
	# Splits the data from the csv file
        pieces = line.split(',')
        degrees = pieces[0]
        timeB=  pieces[1]
        timeA= timeB[:8]
            #print timeA
            #print time_string
        time_string = datetime.strptime(timeA,'%H:%M:%S')
	# Appending the value along the y-axis
        ys.append(degrees)
	# Plotting the time along the x-axis
        xs.append(time_string)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax1.clear()
        ax1.plot(xs,ys,'c',linewidth = 3.3)
        plt.title('Humidity')
        plt.xlabel('Time')

#The animation function keeps updating as and when the values get updated.
ani = animation.FuncAnimation(fig, animate, interval = 1000)
# Plot gets displayed in real-time
plt.show()
