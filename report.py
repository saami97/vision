import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import webbrowser
import datetime as dt

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['*' + '-' * width + '*']
    for s in lines:
        res.append('|' + (s + ' ' * width)[:width] + '|')
    res.append('*' + '-' * width + '*')
    return '\n'.join(res)

def generateReport(scores,averageScore,preDuplicates,postDuplicates,noMatch=0,matches=0):
    
    now = dt.datetime.now()
    filename = now.strftime("%Y-%m-%d%H:%M")
    filename = "Reports/"+filename+".txt"
    fileopen = open(filename,"w")

    reportString = "Report Generated on {time}\n\n"
    reportString = reportString.format(time=now)
    fileopen.write(reportString)
    if(len(scores) > 0):
        fileopen.write("****************** Number of Regenerated Images: "+str(len(scores))+" *****************\n")
        for score in scores:
            fileopen.write("Compare Score - "+str(score)+"\n")

    box = bordered("Average Score is: "+str(averageScore))
    fileopen.write(box)
    fileopen.write("\n\n\n************Highlights************\n\n\n")
    if(averageScore < 1 and matches <= 0):
        fileopen.write("- The Faces are highly similar.\n")
    elif(averageScore==0 and matches > 0):
        fileopen.write("- Number of Matches Found: "+str(matches)+"\n")
    else:
        fileopen.write("- The Faces maybe are not similar.\n")
    if(matches > 0):
        fileopen.write("- The Faces maybe are not similar.\n")
    fileopen.write("- Number of pre duplicates found: "+str(preDuplicates)+"\n")
    fileopen.write("- Number of post duplicates found: "+str(postDuplicates)+"\n")
    fileopen.write("\n\n**************** Report End ****************")
    fileopen.close()
    webbrowser.open(filename)
    showGraph([matches,preDuplicates,postDuplicates,noMatch])

def showGraph(scores):
    objects = ('Similar','Pre Duplicates','Post Duplicates','Disimilar')
    yaxis = np.arange(len(objects))
    plt.bar(yaxis, scores, align='center', alpha=0.5)
    plt.xticks(yaxis, objects)
    plt.ylabel('Image Count')
    plt.title('Batch Analysis')

    plt.show()
