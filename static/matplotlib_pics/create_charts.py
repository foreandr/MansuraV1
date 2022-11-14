
import matplotlib.pyplot as plt
# x axis values
x = ["uploader", "voters[0]","voters[1]","voters[2]","voters[..]"]
# corresponding y axis values
y = [10,8,6,4,2]
  
# plotting the points 
plt.step(x, y)
  
# naming the x axis
plt.xlabel('CHRONOLOGICAL ORDER OF VOTE')
# naming the y axis
plt.ylabel('DISTRIBUTION')
  
# giving a title to my graph
plt.title('LOG EQUAL DISTRIBUTION (steps can be arbitrary sized)')
  
# function to show the plot
plt.gca().axes.get_yaxis().set_visible(False)
plt.savefig('chart_locations/linetest.png')