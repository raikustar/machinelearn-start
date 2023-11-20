import sqlite3
import pandas as pd
# 
#cur.execute("CREATE TABLE movie(title, year, score)")
#res = cur.execute("SELECT name FROM sqlite_master")
#cur.execute("DELETE FROM movie WHERE rowid = 2")
#res = cur.execute("SELECT rowid, title, year, score FROM movie")

#cur.execute("DELETE FROM housing WHERE rowid = 3")
    #cur.execute("DELETE FROM housing WHERE rowid BETWEEN 546 AND 644")
    #cur.execute("SELECT DISTINCT price, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, parking, prefarea, furnish_furnished, furnish_semifurnished, furnish_unfurnished FROM housing")


conn = sqlite3.connect('test_database.db') 
cur = conn.cursor()


csvDataSet = pd.read_csv("Housing.csv")

def toNumericalValue():
    newData = csvDataSet
    toNumVal = ("mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "prefarea")
    for i in toNumVal:
        newData[i] = newData[i].map({"yes": 1, "no": 0})

    workedData = pd.get_dummies(data=newData, columns=["furnishingstatus"], prefix=["furnish"])

    catToNum = ("furnish_furnished", "furnish_semifurnished", "furnish_unfurnished")
    for i in catToNum:
        workedData[i] = workedData[i].map({True:1, False:0})

    return workedData

processed_Data = toNumericalValue()
df = pd.read_sql_query("SELECT * FROM housing", conn)

# Create table from csv

def createTable():
    columnNames = processed_Data.columns.values.tolist()
    str = "CREATE TABLE housing (test INTEGER)"
    cur.execute(str)
    
    for item in columnNames:
        altr = f"ALTER TABLE housing ADD COLUMN '{item}' "
        cur.execute(altr)
    
    dropCol = "ALTER TABLE housing DROP COLUMN test"
    cur.execute(dropCol)
    
    loopData()

def loopData():
    for data in range(0, len(processed_Data)):
        addEntry(processed_Data.loc[data].price, processed_Data.loc[data].area, processed_Data.loc[data].bedrooms, processed_Data.loc[data].bathrooms, processed_Data.loc[data].stories, processed_Data.loc[data].mainroad, processed_Data.loc[data].guestroom, processed_Data.loc[data].basement, processed_Data.loc[data].hotwaterheating, processed_Data.loc[data].parking, processed_Data.loc[data].prefarea, processed_Data.loc[data].furnish_furnished, processed_Data.loc[data].furnish_semifurnished, processed_Data.loc[data].furnish_unfurnished)


def addEntry(price, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, parking, prefarea, furnish_furnished, furnish_semifurnished, furnish_unfurnished):
    #insertToString = "price", "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement", "hotwaterheating", "parking", "prefarea", "furnish_furnished", "furnish_semifurnished", "furnish_unfurnished"
    str = f"INSERT INTO housing(price, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, parking, prefarea, furnish_furnished, furnish_semifurnished, furnish_unfurnished) VALUES ({price}, {area}, {bedrooms}, {bathrooms}, {stories}, {mainroad}, {guestroom}, {basement}, {hotwaterheating}, {parking}, {prefarea}, {furnish_furnished}, {furnish_semifurnished}, {furnish_unfurnished})"
    cur.execute(str)
    
def main():
    #createTable()
    #cur.execute('DROP TABLE housing')
    
    print(df)
    conn.commit()

if __name__ == "__main__":
    main()


