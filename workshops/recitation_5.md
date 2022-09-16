graph TD

%% Insulin pump users today have to deal with numerous technical issues that greatly affect their quality of life.

%% Suppose the probability of failure for each component of this person's equipment is as follows:

pump["Insulin Pump<hr>&lambda; = 1/1000"]
monitor["Continuous<br>Glucose<br>Monitor<hr>&lambda; = 1/500"]
sync["Sync<br>with<br>Pump<hr>&lambda; = 1/20"]
battery["AA Battery<hr>&lambda; = 1/50"]
insulin["Insulin<br>Runs out<hr>&lambda; = 1/2"]
cathoder["Cathoder Set<hr>&lambda; = 1/50"]
inserter["Cathoder Inserter<hr>&lambda; = 1/500"]
charge["Monitor Charge<hr>&lambda; = 1/50"]
mcbatter["AA Batteries<br>for Charger<hr>&lambda; = 1/100"]

charge---mcbatter

remember["Remember<br>to Charge<hr>&lambda; = 1/10"]

cathoder---pump
inserter---cathoder

battery---pump
monitor---sync
sync---pump

monitor---remember
remember---charge

insulin---pump


