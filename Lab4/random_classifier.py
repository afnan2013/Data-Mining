import pandas as df
from sklearn.ensemble import RandomForestClassifier

dtest = df.read_excel('CT_DD Test Results.xlsx', sheet_name='Sheet1')
dtrain = df.read_excel('CT_DD Train Results.xlsx', sheet_name='Sheet1')

x_train = dtrain.iloc[1:, 1:].values
x_class = dtrain.iloc[1:,0].values
y_test = dtest.iloc[1:, 1:].values
y_class = dtest.iloc[1:, 0].values

classification = RandomForestClassifier(n_estimators=100)
classification.fit(x_train, x_class)
y_predict = classification.predict(y_test)
for i in range(len(y_class)):
    print("Actual = ",y_class[i], "  Predicted = ", y_predict[i])
print(y_predict)