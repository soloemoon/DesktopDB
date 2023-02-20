# DesktopDB

## Summary
Desktop Database (DesktopDB) is a simple and lightweight GUI application that allows flat files (excel and csv) to be converted into desktop databases (parquet files) that can be queried and appended to. With DesktopDB, technical and non-technical users are enabled to harness the power of Python to instill good data practices and unlock a wider range of analysis, like historical analysis.

The following can be done with flat files:
* Convert all flat file(s) into individual parquet files 
* Convert all flat file(s) into a single parquet file
* Append flat file(s) to an existing parquet file


## Use Case

Consider the scenario where a monthly excel file containing interest rate data is received and stored in a folder on the company's network drive. Your company has ten years of excel files and your boss asks for a trend analysis of the last five years to be done. Because this data is not in a database you'll be spending the afternoon preparing the data for use by copying and pasting data out of 60 spreadsheets into a single file. DesktopDB can eliminate this sort of task forever! 

Using DesktopDB we now have a single parquet file containing all of our rate information that can be used in the future. As we get new rate files, we can use DesktopDB to add these to our existing parquet file, ensuring we always have an up-to-date database that can be queried in a variety of ways. Our parquet file can even be added to the company's on-prem or cloud datawarehouse with ease.

## Why Not Excel/CSV?

Data belongs in databases. Unfortunately many don't have the option to store flat file data in a databsase making Excel the default data storage tool. This is bad for a few reasons:
- Excel has size limitations. It cannot grow as your data grows preventing historical data from being tracked in a single location.
- Excel does not perform well as files grow in size. A 400MB excel file can bring your PC to a crawl. Databases are performant at much larger sizes.
- Excel can be easily altered leading to inaccurate data. 
- Excel cannot be easily queried for a desired slice of information. Significant filtering must be performed which can lead to errors.
- Excel is not easily transferrable to a proper database. There are no standardds enforced in spreadsheets.
- Excel is infinitely expansive. How many of you have seen files named like excel_file_final.xlsx and excel_file_final(v2).xlsx? There is no single source of truth.
- Excel often can only be accessed by one person at a time, making collaboration difficult.

Databases eliminate these issues. With a database you have an infinite amount of storage that remains performant and transferrable. Databases enforce good practices, reduce confusion, and create a single source of truth. No more wondering which file information came from or why its taking so long to open a file.  

## Why Parquet

Parquet is a column-oriented file format designed for efficient data storage and retrieval. It can handle complex data in bulk and provides better performance than CSVs. Data can be added to parquet files and queried, similar to a database. Parquet files are supported by a wide variety of tools making them likely usable with the software your company is using.
