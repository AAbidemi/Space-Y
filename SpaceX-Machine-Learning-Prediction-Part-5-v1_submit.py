#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
#     </a>
# </p>
# 

# # **Space X  Falcon 9 First Stage Landing Prediction**
# 

# ## Assignment:  Machine Learning Prediction
# 

# Estimated time needed: **60** minutes
# 

# Space X advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because Space X can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against space X for a rocket launch.   In this lab, you will create a machine learning pipeline  to predict if the first stage will land given the data from the preceding labs.
# 

# ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing_1.gif)
# 

# Several examples of an unsuccessful landing are shown here:
# 

# ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)
# 

# Most unsuccessful landings are planed. Space X; performs a controlled landing in the oceans.
# 

# ## Objectives
# 

# Perform exploratory  Data Analysis and determine Training Labels
# 
# *   create a column for the class
# *   Standardize the data
# *   Split into training data and test data
# 
# \-Find best Hyperparameter for SVM, Classification Trees and Logistic Regression
# 
# *   Find the method performs best using test data
# 

# ## Import Libraries and Define Auxiliary Functions
# 

# In[1]:


get_ipython().system('pip install numpy')
get_ipython().system('pip install pandas')
get_ipython().system('pip install seaborn')
get_ipython().system('pip install scikit-learn')


# We will import the following libraries for the lab
# 

# In[2]:


# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier


# This function is to plot the confusion matrix.
# 

# In[3]:


def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show() 


# ## Load the dataframe
# 

# Load the data
# 

# In[4]:


data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")


# In[5]:


data.head()


# In[6]:


X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')


# In[7]:


X.head(100)


# ## TASK  1
# 

# Create a NumPy array from the column <code>Class</code> in <code>data</code>, by applying the method <code>to_numpy()</code>  then
# assign it  to the variable <code>Y</code>,make sure the output is a  Pandas series (only one bracket df\['name of  column']).
# 

# In[10]:


import pandas as pd
import numpy as np

# Create a NumPy array from the 'Class' column
Y = data['Class'].to_numpy()

# Verify the result
print(Y)


# ## TASK  2
# 

# Standardize the data in <code>X</code> then reassign it to the variable  <code>X</code> using the transform provided below.
# 

# In[11]:


# students get this 
# transform = preprocessing.StandardScaler()

# Create the StandardScaler transform
transform = preprocessing.StandardScaler()

# Fit and transform the data
X = transform.fit_transform(X)

# Verify the result
print(X)


# We split the data into training and testing data using the  function  <code>train_test_split</code>.   The training data is divided into validation data, a second set used for training  data; then the models are trained and hyperparameters are selected using the function <code>GridSearchCV</code>.
# 

# ## TASK  3
# 

# Use the function train_test_split to split the data X and Y into training and test data. Set the parameter test_size to  0.2 and random_state to 2. The training data and test data should be assigned to the following labels.
# 

# <code>X_train, X_test, Y_train, Y_test</code>
# 

# In[12]:


# Split the data into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Verify the result
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("Y_train shape:", Y_train.shape)
print("Y_test shape:", Y_test.shape)


# we can see we only have 18 test samples.
# 

# In[13]:


Y_test.shape


# ## TASK  4
# 

# Create a logistic regression object  then create a  GridSearchCV object  <code>logreg_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# 

# In[14]:


parameters ={'C':[0.01,0.1,1],
             'penalty':['l2'],
             'solver':['lbfgs']}


# In[15]:


parameters ={"C":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}# l1 lasso l2 ridge
lr=LogisticRegression()
# Define the logistic regression model
# logreg = LogisticRegression()


# We output the <code>GridSearchCV</code> object for logistic regression. We display the best parameters using the data attribute <code>best_params\_</code> and the accuracy on the validation data using the data attribute <code>best_score\_</code>.
# 

# In[19]:


# Create the GridSearchCV object
logreg_cv = GridSearchCV(lr, parameters, cv=5)

# Fit the model
logreg_cv.fit(X_train, Y_train)


# In[20]:


# Print the best parameters and accuracy
print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_)


# ## TASK  5
# 

# Calculate the accuracy on the test data using the method <code>score</code>:
# 

# In[21]:


# Calculate the accuracy on the test data
accuracy = logreg_cv.score(X_test, Y_test)

# Print the accuracy
print("Test Data Accuracy: ", accuracy)


# Lets look at the confusion matrix:
# 

# In[22]:


yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# Examining the confusion matrix, we see that logistic regression can distinguish between the different classes.  We see that the problem is false positives.
# 
# Overview:
# 
# True Postive - 12 (True label is landed, Predicted label is also landed)
# 
# False Postive - 3 (True label is not landed, Predicted label is landed)
# 

# ## TASK  6
# 

# Create a support vector machine object then  create a  <code>GridSearchCV</code> object  <code>svm_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# 

# In[23]:


parameters = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()


# In[24]:


# Create a GridSearchCV object with cv=10
svm_cv = GridSearchCV(svm, parameters, cv=10)

# Fit the GridSearchCV object to find the best parameters
svm_cv.fit(X_train, Y_train)


# In[25]:


print("tuned hpyerparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)


# ## TASK  7
# 

# Calculate the accuracy on the test data using the method <code>score</code>:
# 

# In[27]:


# Calculate the accuracy on the test data
accuracy = svm_cv.score(X_test, Y_test)

# Print the accuracy
print("Test Data Accuracy: ", accuracy)


# We can plot the confusion matrix
# 

# In[28]:


yhat=svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# ## TASK  8
# 

# Create a decision tree classifier object then  create a  <code>GridSearchCV</code> object  <code>tree_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# 

# In[29]:


parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()


# In[30]:


# Create a GridSearchCV object with cv=10
tree_cv = GridSearchCV(tree, parameters, cv=10)

# Fit the GridSearchCV object to find the best parameters
tree_cv.fit(X_train, Y_train)


# In[31]:


print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)


# ## TASK  9
# 

# Calculate the accuracy of tree_cv on the test data using the method <code>score</code>:
# 

# In[32]:


# Calculate the accuracy on the test data
accuracy = tree_cv.score(X_test, Y_test)

# Print the accuracy
print("Test Data Accuracy: ", accuracy)


# We can plot the confusion matrix
# 

# In[33]:


yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# ## TASK  10
# 

# Create a k nearest neighbors object then  create a  <code>GridSearchCV</code> object  <code>knn_cv</code> with cv = 10.  Fit the object to find the best parameters from the dictionary <code>parameters</code>.
# 

# In[34]:


parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN = KNeighborsClassifier()


# In[36]:


# Create a GridSearchCV object with cv=10
knn_cv = GridSearchCV(KNN, parameters, cv=10)

# Fit the GridSearchCV object to find the best parameters
knn_cv.fit(X_train, Y_train)


# In[37]:


print("tuned hpyerparameters :(best parameters) ",knn_cv.best_params_)
print("accuracy :",knn_cv.best_score_)


# ## TASK  11
# 

# Calculate the accuracy of knn_cv on the test data using the method <code>score</code>:
# 

# In[38]:


# Calculate the accuracy on the test data
accuracy = knn_cv.score(X_test, Y_test)

# Print the accuracy
print("Test Data Accuracy: ", accuracy)


# We can plot the confusion matrix
# 

# In[39]:


yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)


# ## TASK  12
# 

# Find the method performs best:
# 

# In[41]:


# Calculate the accuracy on the test data
logreg_accuracy = logreg_cv.score(X_test, Y_test)
svm_accuracy = svm_cv.score(X_test, Y_test)
tree_accuracy = tree_cv.score(X_test, Y_test)
knn_accuracy = knn_cv.score(X_test, Y_test)


# In[42]:


# Print the accuracies
print("Logistic Regression Test Data Accuracy: ", logreg_accuracy)
print("SVM Test Data Accuracy: ", svm_accuracy)
print("Decision Tree Test Data Accuracy: ", tree_accuracy)
print("KNN Test Data Accuracy: ", knn_accuracy)


# In[43]:


# Based on the test data accuracy scores above, the Decision Tree model performs the best with an accuracy of 0.8889.


# ## Authors
# 

# [Pratiksha Verma](https://www.linkedin.com/in/pratiksha-verma-6487561b1/)
# 

# <!--## Change Log--!>
# 

# <!--| Date (YYYY-MM-DD) | Version | Changed By      | Change Description      |
# | ----------------- | ------- | -------------   | ----------------------- |
# | 2022-11-09        | 1.0     | Pratiksha Verma | Converted initial version to Jupyterlite|--!>
# 

# ### <h3 align="center"> IBM Corporation 2022. All rights reserved. <h3/>
# 
