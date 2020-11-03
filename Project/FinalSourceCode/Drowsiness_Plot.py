import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation #animation library is used here
from datetime import datetime
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
def animate(i):
    ftemp = 'ear.csv' #CSV file which is getting written parallely
    fh = open(ftemp) #Open the CSV file
    xs=[]
    ys=[]
    for line in fh:
        pieces = line.split(',') # Splits the data from the csv file
        value = pieces[0]
        timeB=  pieces[1]
        timeA= timeB[:8]
        time_string = datetime.strptime(timeA,'%H:%M:%S')
        ys.append(float(value)) # Appending the value along the y-axis
        xs.append(time_string) # Plotting the time along the x-axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax1.clear() # Keep clearing the values
        ax1.plot(xs,ys,'c',linewidth = 3.3) # Plot the graph
        plt.title('EAR Values')
        plt.xlabel('Time')

ani = animation.FuncAnimation(fig, animate, interval = 500) #The animation function keeps updating as and when the values get updated.
plt.show() # Plot gets displayed in real-time


