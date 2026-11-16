# Assignment-2---FINE-3300
This program replicates the Bank of Canada's Inflation Calculator using Python. Unlike the calculator on the official website, this program uses the monotly CPI data to calculate changes in the strength and valuation of money over time. 

This program uses Pandas to manipulate the data downloaded from the csv file and also uses Matplotlib to create the graphs for visual purposes. 

The program lies in the file labeled "inflation_calculator.py" and the monthly CPI data from the Bank of Canada is in a "data" folder, for separation and organization, labeled "inflation_data.py". After running the code to check for any issues it also created a new folder named "images" which has a copy of the graph created from the Matplotlip library. 

The graph the program creates is uploaded to the GitHub repository under the folder "images" as I could not upload it to this readme file. If you open it up in the repository you'll be able to view the entire graph. I wanted to rename the file as well to be more relevant like "CCPI vs Annual Inflation Rate" but it ended up corrupting the file and wouldn't allow it to be opened. 

HOW TO USE THE CALCULATOR: 

When you first begin to run the program, it'll open up the graph to display to the user, in order to continue using this calculator, you will need to close the window (not minimize, actually close the window) and then the calculator function will run. The program will prompt you for the original amount. It will then prompt you to input the year and month in a YYYY-MM format, when inputting this information you must include the "-" between the year and the month, relating to the original amount inputted. The program will then ask what day and year you would like the original amount to be converted to using the amounts listed in the CSV file downloaded from the Bank of Canada's website. 

After receiving those 3 pieces of information, the program gathers the CPI information, performs the calculations, and displays the calculation results. The results include the original price, the new price, the change in percentage, the number of years that lapsed between the original date and the new date, the CPI for the original date, and the CPI for the new date. It also provides the base level CPI for additional information. 