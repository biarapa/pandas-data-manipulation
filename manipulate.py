import pandas as pd 
import numpy as np

df = pd.read_csv('~/Downloads/csv-to-pandas/income.csv')

#1. get variable names
df.columns

#2. knowing variable types
df.dtypes

#3. changing data types
df['Y2002'] = df['Y2002'].astype(float)

#4. view dimensions or shape of data (rows, columns)
df.shape

#5. view only some rows
df.head()
df.head(3)      #first 3 rows
df.tail()
df.tail(4)      #last 4 rows
df[0:5]         #alternatively, first 5 rows    
df.iloc[0:6]    #alternatively, first 6 rows 

#6. define categorical variable
s = pd.Series([1,2,3,1,2], dtype='category')

#7. extract unique values
df['Index'].unique()        #select unique value from Index column
df['Index'].nunique()       #count unique value from Index column

#8. generate cross tab. create a bivariate frequency distribution
pd.crosstab(df['Index'], df['State'])

#9. create a frequency distribution
df['Index'].value_counts(ascending=True)        #frequency of column Index

#10. draw the samples
df.sample()
df.sample(n=5)              #get 5 random rows
df.sample(frac = 0.2)       #get 20% random rows

#11. selecting only a few of the columns
df[['Index', 'State', 'Y2008']]

#11.a loc & iloc function
df.loc[:,['Index', 'State']]        #selecting all rows
df.loc[0:2,['Index', 'State']]      #selecting rows index 0 to 2
df.loc[:,'Index':'State']           #selecting all rows
df.iloc[:,0:5]                      #select column 1 to 5, only integer

#12. renaming the variables
df.rename(columns={'Index':'ID'}, inplace=True)        #rename specific column. inplace = alter the original dataset. default in pandas is False
#df.columns=['column A', 'Column B']                     #rename all columns

df.columns = df.columns.str.replace('Y', 'Year')        #rename column use specific char

#13. setting one column in the dataFrame as the index
df.set_index('ID', inplace=True)       #set index in column ID
#df.reset_index(inplace=True)          #reset all indexed column


#14. removing columns and rows
#df.drop('Year2002', axis=1, inplace=True)   #drop column, axis=0 operation should take place horizontally. inplace means dropping is applied to the new df
df.drop(['Year2003', 'Year2004'], axis=1)   #drop multiple column

#15. sorting data
df.sort_values('ID', ascending=False, inplace=True)

#16. create new variables
df['add'] = df['Year2004'] + df['Year2004']         #create new column 'add'
df['diff'] = df.eval('Year2004-Year2003')           #alternatively
ratio = df.assign(ratio = df['Year2004']/df['Year2003'])    #alternatively

#17. aggregation
df.describe()                       #count, mean, std, min, quartile and max, numeric only
df.describe(include=['object'])     #only fro strings/objects
df.mean()                           #specific aggr
df.median()
df.agg(['mean', 'max'])

df['Year2002'].mean()          #for specific column
df.loc[:,['Year2002', 'Year2008']].max()

#18. group by function
df.groupby('ID')['Year2002', 'Year2003'].min()
df.groupby(['ID', 'State'], as_index=False).min()           #group by more than 1 column. as_index = enable the column become an index in the new df

#19. filtering
df[df['State'] == 'Alabama']
df.loc[df['State']=='Alabama',:]                #alternatively
df.loc[df['State']=='Alabama',:].Year2002       #select year 2002 where state = alabama
df.loc[(df['State']=='Alabama') & (df.Year2003 > 5000000),:]
df.loc[df.State.isin(['Alabama', 'New York']), :]
df.query('Year2002>100000 & Year2003>1500000')      #alternatively

#20. missing values
df.isnull()
df.notnull()
df.isnull().sum()               #number of missing values
df[df.State.isnull()]

df.dropna(how='any').shape      #drop missing values in any rows
df.dropna(how='all').shape      #drop missing values in the missing row

#drop missing values in specific list or columns
df.dropna(subset=['Year2002', 'State'], how='any').shape
df.dropna(subset=['Year2002', 'State'], how='all').shape

#replacing missing values by 'UNKNOWN'
df['State'].fillna(value='UNKNOWN', inplace=True)

#21. duplicate values
df.loc[df.duplicated(), :]
df.loc[df.duplicated(keep='first'), :]          #first is unique value, the rest is duplicates
df.loc[df.duplicated(keep='last'), :]           #last is unique, its repetitions are considered as duplicates
df.loc[df.duplicated(keep=False), :]            #all duplicates, including unique, considered as duplicates
df.drop_duplicates(keep='first', inplace=True)

#22. ranking
df.rank()
df.rank(ascending=1)

#23. calculating the cumulative sum
df['Year2002'].cumsum()

#24. calculating the precentiles
df.quantile(0.5)
df.quantile([0.1, 0.2, 0.5])
df.quantile(0.55)


#25. if else condition
def states(row):
    if row['State'] in ['Alabama', 'New York']:
        return 'You live in this state'
    else:
        return 'Get out of this state'
df['home'] = df.apply(states, axis=1)

#alternatively using numpy np
df['home_np'] = np.where(df['State'].isin(['Alabama', 'New York']), 'Yes np', 'no np')


#26 multiple if else

def year(row):
    if row['Year2002'] < 1200000:
        return 'Poor'
    elif row['Year2002'] > 1200000 and row['Year2002'] <= 1500000:
        return 'Middle class'
    else:
        return 'rich'
df['Category'] = df.apply(year, axis=1)

#alternatively using numpy np
conditions = [
    (df['Year2002'] < 1200000),
    (df['Year2002'] > 1200000) & (df['Year2002'] <= 1500000)
    ]
choices = ['poor', 'middle']    
df['categoryNp'] = np.select(conditions, choices, default='rich')

#27. select numeric/categorical columns
dataNumeric = df.select_dtypes(include=[np.number])
dataCat = df.select_dtypes(include=['object'])

#28. concatenating
students = pd.DataFrame({'Names': ['John','Mary','Henry','Augustus','Kenny'],
                         'Zodiac Signs': ['Aquarius','Libra','Gemini','Pisces','Virgo']})
marks = pd.DataFrame({'Names': ['John','Mary','Henry','Augustus','Kenny'],
                          'Marks' : [50,81,98,25,35]})

studentMark = pd.concat([students, marks])           #by default axis = 0, new df will be added row-wise
students.append(marks)                               #alternatively
studentMark = pd.concat([students, marks], axis=1)   #join column

#using dictionary
studentMarkDict = {'x':students, 'y':marks}
result = pd.concat(studentMarkDict)


#29. merge or join on the basis of common variable
dataMerge = pd.merge(students, marks, on='Names')                    #similar to SQL join
dataMergeInner = pd.merge(students, marks, on='Names', how='inner')
dataMergeOuter = pd.merge(students, marks, on='Names', how='outer')
dataMergeLeft = pd.merge(students, marks, on='Names', how='left')
dataMergeRight = pd.merge(students, marks, on='Names', how='right', indicator=True)     #indictor indicates whether the values are present in both, left or right df.


print(dataMergeRight)     