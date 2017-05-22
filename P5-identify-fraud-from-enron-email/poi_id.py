#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'salary', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options']  # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Print the number of data points
#print len(data_dict.keys())

### Print the number of features
#print len(data_dict.values()[0])

### Count the total number of missing data in the dataset
'''count = 0
for n in data_dict:
    name = data_dict[n]
    for f in name:
        feature = name[f]
        if feature == 'NaN':
            count += 1

print "The dataset have " + str(count) + " missing values"'''

### Count the missing data for each person
'''for n in data_dict:
    name = data_dict[n]
    count = 0
    for f in name:
        feature = name[f]
        if feature == 'NaN':
            count += 1
    print str(n) + ": " + str(count)'''

### Count the missing data for each feature
'''missing_data = {}
for n in data_dict:
    name = data_dict[n]
    for f in name:
        feature = name[f]
        if feature == 'NaN':
            if f in missing_data:
                missing_data[f] = missing_data[f] + 1
            else:
                missing_data[f] = 1

print missing_data'''

### Task 2: Remove outliers
data_dict.pop("TOTAL", 0)
data_dict.pop("LOCKHART EUGENE E", 0)
data_dict.pop("THE TRAVEL AGENCY IN THE PARK", 0)

### Features Selection

### List of financial features
financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']

### List of email features
email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi'] 

### POI label
poi  = ['poi']

### Concatenation of all features lists
features = poi + financial_features + email_features

### Select the best Feature Selector using Pipeline
'''import sklearn.pipeline
import sklearn.feature_selection
import sklearn.ensemble

select = sklearn.feature_selection.SelectKBest()
clf = sklearn.ensemble.RandomForestClassifier()

steps = [('feature_selection', select),
        ('random_forest', clf)]

pipeline = sklearn.pipeline.Pipeline(steps)'''

### Convert the features in dictionary format into a numpy array
data = featureFormat(data_dict, features)
poi, all_features = targetFeatureSplit(data)

### 
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
all_features = scaler.fit_transform(all_features)

### Cross validation
from sklearn.cross_validation import train_test_split
feature_train, feature_test, target_train, target_test = \
    train_test_split(all_features, poi, test_size=0.3, random_state=42)

### Find the best parameters using Grid Search combined with Pipeline
'''import sklearn.grid_search

parameters = dict(feature_selection__k=[2, 3, 5, 8], 
              random_forest__n_estimators=[25, 50, 100, 200],
              random_forest__min_samples_split=[2, 3, 4, 5, 10])
cv = sklearn.grid_search.GridSearchCV(pipeline, param_grid=parameters)

cv.fit(feature_train, target_train)

prediction = cv.predict(feature_test)

target_names = ['SelectKBest', 'RandomForest']

report = sklearn.metrics.classification_report(target_test, prediction, target_names=target_names)

print report

print cv.best_params_'''

### Print the score of each feature using the function SelectKBest
'''import sklearn.feature_selection

select = sklearn.feature_selection.SelectKBest(k=2)
select.fit(feature_train, target_train)

scores = select.scores_

list_features = financial_features + email_features
for feature, score in zip(list_features, scores):
    print feature, round(score, 4)'''

### Task 3: Create new feature(s)
'''def SalaryProportionBonus(salary, bonus):
    proportion = 0.
    if (salary == "NaN" or bonus == "NaN"):
        return 0
    else:
        proportion = salary/(bonus*1.0)
    return proportion

for name in data_dict:
    data_point = data_dict[name]
    
    salary = data_point["salary"]
    bonus = data_point["bonus"]
    
    salary_in_proportion_to_bonus = SalaryProportionBonus(salary, bonus)
    data_point["salary_in_proportion_to_bonus"] = salary_in_proportion_to_bonus'''
    
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from sklearn.cross_validation import StratifiedShuffleSplit
cv = StratifiedShuffleSplit(labels, 1000, random_state = 42)

for train_idx, test_idx in cv: 
    feature_train = []
    feature_test  = []
    target_train   = []
    target_test    = []
    for ii in train_idx:
        feature_train.append( features[ii] )
        target_train.append( labels[ii] )
    for jj in test_idx:
        feature_test.append( features[jj] )
        target_test.append( labels[jj] )

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

### Trying Naive Bayes Classifier
import sklearn.naive_bayes

clf = sklearn.naive_bayes.GaussianNB()

### Trying Decision Tree Classifier
'''import sklearn.tree

clf = sklearn.tree.DecisionTreeClassifier(min_samples_split = 90, class_weight = {1:10})'''

### Trying Random Forest Classifier
'''import sklearn.ensemble

clf = sklearn.ensemble.RandomForestClassifier(min_samples_split = 80, n_estimators = 5, class_weight = {1:10})'''

### Trying Support Vector Classifier
'''import sklearn.svm

clf = sklearn.svm.SVC(kernel='rbf', class_weight = {1:10}, C = 1e-8)'''

### Tunning the Decision Tree Classifier
'''import sklearn.grid_search
import sklearn.tree

parameters = {'min_samples_split':[20, 30, 40, 50, 60, 80, 90], 'class_weight':[{1:2}, {1:5}, {1:10}, {1:20}]}

clf = sklearn.grid_search.GridSearchCV(sklearn.tree.DecisionTreeClassifier(), parameters, scoring = 'recall')
clf.fit(feature_train, target_train)

print clf.best_estimator_'''

### Tunning the Random Forest Classifier
'''import sklearn.grid_search
import sklearn.ensemble

parameters = {'min_samples_split':[20, 30, 40, 50, 60, 80, 90], 'n_estimators':[2, 5, 10, 25, 50], 'class_weight':[{1:2}, {1:5}, {1:10}, {1:20}]}

clf = sklearn.grid_search.GridSearchCV(sklearn.ensemble.RandomForestClassifier(), parameters, scoring = 'recall')
clf.fit(features, labels)

print clf.best_estimator_'''

### Tunning the Support Vector Classifier
'''import sklearn.grid_search
import sklearn.svm

parameters = {'C':[1e-8, 1e-6, 1e-2, 1], 'class_weight':[{1:2}, {1:5}, {1:10}, {1:20}]}

clf = sklearn.grid_search.GridSearchCV(sklearn.svm.SVC(kernel = 'rbf'), parameters, scoring = 'recall')
clf.fit(features, labels)

print clf.best_estimator_'''

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
