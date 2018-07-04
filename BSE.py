

import lxml.html
import requests
import pandas as pd
from datetime import datetime


def get_data():
    
    try:
        r = requests.get("https://www.bseindia.com/sensexview/IndexHighlight.aspx")
        r.raise_for_status()
    except requests.exceptions.HTTPError as errhttp:
        print("HTTP ERROR")
    except requests.exceptions.ConnectionError as errConn:
        print("CONNECTION ERROR")
    except requests.exceptions.Timeout as errTimeOut:
        print("TIMEOUT ERROR")
    except requests.exceptions.RequestException as err:
        print("REQUEST ERROR")
        
        
    root = lxml.html.fromstring(r.text)
    
    col = [[] for i in range(14)]
    
    for x in root.xpath("//*[@id = 'ctl00_ContentPlaceHolder1_gvRealTime']/.//td[@class = 'TTRow_left']/..//td[1]/a"):
        col[1].append(x.text)
    
    
    for i in range(2,13):
        for r in root.xpath("//*[@id = 'ctl00_ContentPlaceHolder1_gvRealTime']/.//td[@class = 'TTRow_left']/..//td[%s]" %i):
            col[i].append(r.text)
            #print (col[i])
    
    
    col[0] = ["BSE India" for i in range(len(col[1]))]

    col[13] = [datetime.now().strftime('%B %d, %Y  %H:%M:%S%p') for i in range(len(col[1]))]
    #print(col[0])  
    #print(col)
    
    data = {"Source":col[0], "Index":col[1], "Open":col[2],"High":col[3], "Low":col[4], "Current Value":col[5], "Prev Close":col[6], "Ch(pts)":col[7], "ch(%)":col[8],"52 Week high":col[9], "52 Weeek low":col[10], "Turn Over (Rs Cr)":col[11], "% In Total Turn Over":col[12], "Date-Time":col[13]}
    
    df_NaN = pd.DataFrame(data, columns = ["Index", "Open", "High", "Low", "Current Value", "Prev Close", "Ch(pts)", "ch(%)", "52 Week high", "52 Weeek low", "Turn Over (Rs Cr)", "% In Total Turn Over", "Source", "Date-Time"])
    
    #"""required column in which you want NaN as String give it below in vlaues dict"""
    #values = {"Open" : "Null"}
    df = df_NaN.fillna(value = "Data Missing")
    return df
    
def put_data(data_frame):
    try:
        data_frame.to_csv("C:\\Users\\garima.misra\\Practice\\trailBSI8.csv", sep = ',')
    except Exception:
        print("We will get back to you soon...")
        
def main():
    df = get_data()
    put_data(df)
 
    
if __name__ == '__main__':
    main()
