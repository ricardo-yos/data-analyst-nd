
### Data Dictionary

<code>
<strong>Variable</strong>   <strong>Definition</strong>	                                     <strong>Key</strong>
survival   Survival                                           0 = No, 1 = Yes
pclass     Ticket class                                       1 = 1st, 2 = 2nd, 3 = 3rd
sex        Sex	
Age        Age in years	
sibsp      # of siblings / spouses aboard the Titanic	
parch      # of parents / children aboard the Titanic	
ticket     Ticket number	
fare	   Passenger fare	
cabin      Cabin number	
embarked   Port of Embarkation                                C = Cherbourg, Q = Queenstown, S = Southampton
</code>

### Variable Notes

<code>
<strong>pclass</strong>: A proxy for socio-economic status (SES)
1st = Upper
2nd = Middle
3rd = Lower

<strong>age</strong>: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5

<strong>sibsp</strong>: The dataset defines family relations in this way...
Sibling = brother, sister, stepbrother, stepsister
Spouse = husband, wife (mistresses and fiancés were ignored)

<strong>parch</strong>: The dataset defines family relations in this way...
Parent = mother, father
Child = daughter, son, stepdaughter, stepson
Some children travelled only with a nanny, therefore parch=0 for them.
</code>
