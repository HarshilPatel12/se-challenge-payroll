import csv;
import operator;
import os;



def getPayrollReport():
    '''
    Algorithm is very simple to generate a report. This function will go through
    all the csv files present in the 'uploads' folder will be gone through one
    by one. In each file, it will read the record line by line and create a json
    entry for each record being placed in either first half or the second half
    of the month.Once the records are all in the json file, the second half of the
    algorithm will go through each record and collapse it so that the records
    are grouped based on first half and second half of the month are combined. 
    Comparing each element with every other, when it finds 2 entries that have 
    same pay periods, the amounts are added into one entry while the other is
    put amount at 0. The third portion will take all the entries with amount
    paid as 0 and filter it out. The complexity of this algorithm is 
    O(n) + O(n^2) + O(n) >= O(n^2) per file.
    Let x = the number of files and the algorithm would be O(x(n^2)) 
    '''
    
    payrollReport = {}
    employeeReports = []
    
    result = {}
    dirPath = r"./uploads"
    for filename in os.listdir(dirPath):
        nfilename = os.path.join(dirPath, filename) 
        with open(nfilename, 'r') as times:
            employeeTime = list(csv.reader(times))
            temp = {}
            employeeTime = employeeTime[1:]
            # Populate the json first, with all the records and amounts calculated for the hours
            for data in employeeTime:
                date = data[0].split("/")
                employeeId = int(float(data[2]))
                temp = {}
                # Insert the employeeId, this is a normal parse
                temp["employeeId"] = employeeId
                # Determine the pay for the first or second half
                payPeriod = {}
                days = "31"
                if(date[1] == "4" or date[1] == "6" or date[1] == "9" or date[1] == "11"):
                    days = "30"
                if(date[1] == "2"):
                    days = "28"
                # This is the first half the month
                if(int(date[0]) >= 1 and int(date[0]) <= 15):
                    payPeriod["startDate"] = date[2] + "-" + date[1] + "-" + "01"
                    payPeriod["endDate"] =  date[2] + "-" + date[1] + "-" + "15"
                else:
                    payPeriod["startDate"] = date[2] + "-" + date[1] + "-" + "16"
                    payPeriod["endDate"] =  date[2] + "-" + date[1] + "-" + days 
                
                # Add the amount for the following pay period
                amountPaid = 0
                rate = 0
                if(data[3] == 'A'):
                    rate = 20
                else:
                    rate = 30
                amountPaid = float(data[1]) * rate
                temp["payPeriod"] = payPeriod
                temp["amountPaid"] = "$"+ str(amountPaid)
                employeeReports.append(temp)
                payrollReport["employeeReports"] = employeeReports
                
                
                                
                
    # Once the list of dict is populated, we will have multiple paid amount values for the same employee id and can be collaped to first half or
    # second half of the month
    totData = employeeReports
    for i in range(0, len(employeeReports), 1):
        for j in range(0, len(employeeReports),1):
            if(i != j):
                firstData = totData[i]
                secondData = totData[j]
                if(firstData["employeeId"] == secondData["employeeId"]):
                    # If the id and the date are same then add the amount into one entry and make the second entry paid amount 0
                    if(firstData["payPeriod"] == secondData["payPeriod"]):
                        firstAmount = firstData["amountPaid"]
                        secondAmount = secondData["amountPaid"]
                        
                        val = "$" + str(float(firstAmount[1:]) + float(secondAmount[1:]))
                        firstData["amountPaid"] = val
                        secondData["amountPaid"] = "0.0"
    # Filter the amounts that have paid amount 0, as all the amounts are added into one entry                     
    employeeReports = []
    for records in totData:
        if(records["amountPaid"] != '0.0'):
            employeeReports.append(records)
           
    employeeReports.sort(key=lambda i: i['employeeId'])
    # Create the final result for the return       
    result["employeeReports"] = employeeReports
    finalResult = {}
    finalResult["payrollReport"] = result
    # print(finalResult)
    return finalResult
                            
                        

        
        
        
    
            
            
        