import os
import random
import numpy as np
import pandas as pd
from multiprocessing import Pool
from joblib import dump, load
from itertools import repeat
from sklearn import metrics
from sklearn import datasets
from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from upsetplot import from_memberships
from sklearn.metrics import RocCurveDisplay, auc
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import average_precision_score, precision_recall_curve
data_dir = '/path/to/data'
data_dir = '/allen/programs/celltypes/workgroups/mct-t200/marcus/VGT/TIGRE3_data/results/NJJ_dream_paper/github/'
out_dir = 'path/to/out_folder'
os.chdir(out_dir)

groups_file = data_dir+'/groups.txt' #sets of variables for testing
groups = pd.read_table(groups_file)

data = pd.read_csv( data_dir+"/enhancer_genomic_data.csv") #all mouse
data = data[data["LABEL_Specificity"] != "Mixed_Target"] #remove mixed target to simplify

#subset data
data['Species']= "Mouse"
data_for_merge = data.copy() #just to add enhancer ID back in later

#prep data
data = data[['log10_POLR2A','H3K4me3_FC','H3K27Ac_FC','CTCF_FC','percent_matching_bps','ON_target','num_at_stretches','max_scaled_acc_mouse','log10_acc_ms','log10_acc_hm','log10_H3K4me3','log10_H3K27Ac','log10_CTCF','LABEL_STRENGTH_BRIGHT_V_OTHER','max_correlation','max_cor_Archr','SIGNAL_specificity','LABEL_Brightness_NUMERIC',"SIGNAL_PRESENCE",'Species','distToTSS','accessibility_mouse','accessibility_human','max_ABC','N_loops','Perc.Ident','Alignment.Length','gini_index','cor_ms_hm','peak_score','fdr','GC.content']]
#numeric features to normalize and scale
norm_scale = ['log10_POLR2A','H3K4me3_FC','H3K27Ac_FC','CTCF_FC','percent_matching_bps','num_at_stretches','max_scaled_acc_mouse','log10_acc_ms','log10_acc_hm','log10_H3K4me3','log10_H3K27Ac','log10_CTCF','max_correlation','max_cor_Archr','distToTSS','accessibility_mouse','accessibility_human','max_ABC',"N_loops",'Perc.Ident','Alignment.Length','gini_index','cor_ms_hm','peak_score','fdr','GC.content']

y4 = data['ON_target'] #on target only
y4 = y4.astype('category').to_numpy()

#examine missing values
# summarize the number of rows with missing values for each column
for i in data.columns:
    n_miss = data[[i]].isnull().sum()
    perc = n_miss / data.shape[0] * 100
    print(''.join([i,': ',str(n_miss[0]),'_percent missing: ', str(perc[0]) ]))

#impute any missing values using KNNimputer
data = data[norm_scale]
data.replace(0, np.nan)
data = data.replace({np.nan:None})
imputer = KNNImputer(n_neighbors=5, weights='uniform', metric='nan_euclidean')
imputer.fit(data)
#transform the dataset
data = imputer.transform(data)

#normalize and scale numeric features
scaler = preprocessing.MinMaxScaler()
d = scaler.fit_transform(data)
scaled_df = pd.DataFrame(d, columns=norm_scale)
X = scaled_df
P = X
data_for_merge.index = X.index
X["Enhancer_ID"] = data_for_merge['Enhancer_ID']

#set random seed and other settings
random.seed(1000)
np.random.seed(1000)

#for final test
X_train4,X_test4,y_train4,y_test4 = train_test_split(X,y4,test_size = 0.30,stratify=y4) # signal specificity

#functions
def grid_search_forest_return_AUC_and_error(vars_to_include, X, y,description,scoring_stat):
    X = X[vars_to_include]
    from sklearn.pipeline import Pipeline
    pipe = Pipeline([('classifier' , RandomForestClassifier())])

    # Create param grid.
    param_grid = [
        {'bootstrap': [True],
        'max_depth': [ 4,6,8],
        'max_features': [None],
        'max_leaf_nodes':[50,100],
        'min_samples_split': [2, 3, 6],
        'n_estimators': [ 10,50, 100,200],
        'class_weight':["balanced"]}]   

    # Createc grid search object
    #adjusting based on stack overflow post... 09/18/2023
    gcv = GridSearchCV(RandomForestClassifier(), param_grid = param_grid, cv = 10, verbose=True, n_jobs=30, scoring = scoring_stat,return_train_score = True)
    gcv.fit(X,y)
    classifier = gcv.best_estimator_
    #if saving model
    #model_file = "_".join(map(str, vars_to_include))+'random_forest_model.joblib'
    #model_file = '/allen/programs/celltypes/workgroups/mct-t200/marcus/VGT/TIGRE3_data/results/machine_learning_models/_'+description+"_"+model_file
    #dump(classifier, model_file) #if saving
    return gcv

def get_mean_test_score(gcv):
    mean_test_score = gcv.cv_results_['mean_train_score'][gcv.best_index_]
    return(mean_test_score)

def get_std_mean_test_score(gcv):
    std_test_score = gcv.cv_results_['std_train_score'][gcv.best_index_]
    return(std_test_score)

def get_precision(gcv, X, y):
    model = gcv.best_estimator_
    y_predictions = model.predict(X[model.feature_names_in_])
    scores = precision_score(y,y_predictions, average = 'binary')
    return scores

def get_recall(gcv, X, y):
    model = gcv.best_estimator_
    y_predictions = model.predict(X[model.feature_names_in_])
    scores = recall_score(y,y_predictions, average = 'binary')
    return scores

def check_if_all_equal(lst):
    if len(lst) < 0:
        res = True
    res = all(ele == lst[0] for ele in lst)
 
    if(res):
        decision = "exclude"
    else:
        decision = "keep"
    return decision

def get_PR_AUC_test(gcv,X, y):
    model = gcv.best_estimator_
    y_predictions = model.predict(X[model.feature_names_in_])
    precision, recall, thresholds = precision_recall_curve(y, y_predictions)
    #Use AUC function to calculate the area under the curve of precision recall curve
    pr_auc = auc(recall, precision)
    return pr_auc

def determine_to_exclude(gcv,X):
    model = gcv.best_estimator_
    y_predictions = model.predict(X[model.feature_names_in_])
    decision = check_if_all_equal(y_predictions)
    return decision

def get_cv_score(gcv, description):
    mean_train_score = gcv.cv_results_['mean_train_score'][gcv.best_index_]
    std_train_score = gcv.cv_results_['std_train_score'][gcv.best_index_]
    mean_test_score = gcv.cv_results_['mean_test_score'][gcv.best_index_]
    std_test_score = gcv.cv_results_['std_test_score'][gcv.best_index_]
    var = ','.join(gcv.feature_names_in_)
    df = pd.DataFrame({'vars':var,'mean_train_score':[mean_train_score],'std_train_score': [std_train_score], 'mean_test_score':[mean_test_score],'std_test_score':[std_test_score]})
    df['description'] = description
    df.index = df['vars']
    return df

def get_AUC(gcv,X, y):
    model = gcv.best_estimator_
    y_probs = model.predict_proba(X[model.feature_names_in_])
    y_probs = y_probs[:,1]
    fpr, tpr, thresholds = metrics.roc_curve(y, y_probs, pos_label=1)
    auc = metrics.auc(fpr, tpr)
    return auc
########################
#random forest auc
########################
scoring_stat = 'f1_macro'

### added this block to change how precision was calculated - based on gcv results
groups = pd.read_table(groups_file)
groups = from_memberships(groups.groups.str.split(','), data=groups)
group_list = pd.read_table(groups_file)
group_list = group_list.groups.str.split(',')

def get_stats_pr(gcv, X_train, y_train, X_test, y_test,description,scoring_stat):
    try:
        classifier = gcv.best_estimator_
        X_train = X_train[classifier.feature_names_in_]
        X_test = X_test[classifier.feature_names_in_]
        classifier.fit(X_train,y_train)
        y_probs = classifier.predict_proba(X_test)
        y_probs = y_probs[:,1]
        precision, recall, thresholds = metrics.precision_recall_curve(y_test, y_probs, pos_label=1,drop_intermediate=False)
        fpr, tpr, thresholds = metrics.roc_curve(y_test, y_probs, pos_label=1,drop_intermediate=False)
        pr_data = pd.DataFrame({'precision_scores':precision,'recall_scores':recall,'fpr':fpr,'tpr':tpr})
        pr_data['vars'] = ','.join(classifier.feature_names_in_)
        print(pr_data.head())
    except Exception:
        pr_data = pd.DataFrame()
        pass
    return(pr_data) #test return both dataframes

def get_stats_probs(gcv, X_train, y_train, X_test, y_test,description,scoring_stat,Enhancer_IDs):
    try:
        classifier = gcv.best_estimator_
        X_train = X_train[classifier.feature_names_in_]
        X_test = X_test[classifier.feature_names_in_]
        classifier.fit(X_train,y_train)
        y_probs = classifier.predict_proba(X_test)
        y_probs = pd.DataFrame({'probability_0':y_probs[:,0],'probability_1': y_probs[:,1]})
        y_probs['vars'] = ','.join(classifier.feature_names_in_)
        y_probs["Enhancer_ID"] = Enhancer_IDs
    except Exception:
        y_probs = pd.DataFrame()
        y_probs['vars'] = ','.join(classifier.feature_names_in_)
        y_probs["Enhancer_ID"] = Enhancer_IDs
        pass
    return(y_probs) #test return both dataframes

#generate and test models - specificity 
with Pool() as pool:
    gcvs_spec =  list(pool.starmap(grid_search_forest_return_AUC_and_error, zip(group_list, repeat(X_train4[norm_scale]), repeat(y_train4),repeat("specificity_"),repeat(scoring_stat))))

with Pool() as pool:
    oob_test_precision_scores = list(pool.starmap(get_precision, zip(gcvs_spec, repeat(X_test4[norm_scale]), repeat(y_test4))))
    train_recall_scores = list(pool.starmap(get_recall, zip(gcvs_spec, repeat(X_train4[norm_scale]), repeat(y_train4))))
    test_recall_scores = list(pool.starmap(get_recall, zip(gcvs_spec, repeat(X_test4[norm_scale]), repeat(y_test4))))
    test_AUC2 = list(pool.starmap(get_AUC, zip(gcvs_spec, repeat(X_test4[norm_scale]), repeat(y_test4))))
    mean_test_score = list(pool.starmap(get_mean_test_score, zip(gcvs_spec)))
    std_test_score = list(pool.starmap(get_std_mean_test_score, zip(gcvs_spec)))
    test_PR_AUC = list(pool.starmap(get_PR_AUC_test, zip(gcvs_spec, repeat(X_test4[norm_scale]), repeat(y_test4))))
    exclude = list(pool.starmap(determine_to_exclude, zip(gcvs_spec, repeat(X_test4[norm_scale]))))

with Pool() as pool:
    stats_spec = pd.concat(pool.starmap(get_cv_score, zip(gcvs_spec,repeat('specificity_auc'))))


stats_spec['test_precision'] = oob_test_precision_scores
stats_spec['train_AUC'] = mean_test_score 
stats_spec['train_recall'] = train_recall_scores
stats_spec['test_recall'] = test_recall_scores
stats_spec['test_AUC'] = test_AUC2
stats_spec['test_PR_AUC'] = test_PR_AUC
stats_spec['exclude'] = exclude
stats_spec = stats_spec[stats_spec['exclude'] == "keep"]
stats_spec = stats_spec.sort_values('test_AUC', ascending = False)
stats_spec.to_csv('random_forest_models_optimized_for_on_target_specificity_stats.csv')

#determine the best model and use gcv.best_estimator_.feature_importances to get importances
#example #pd.DataFrame({'features':gcvs_spec[2].best_estimator_.feature_names_in_, "importance": gcvs_spec[2].best_estimator_.feature_importances_}).to_csv('/allen/programs/celltypes/workgroups/mct-t200/marcus/VGT/TIGRE3_data/results/scikit_learn_optimize_using_f1/random_forest_spec_enhancers_best_model_feature_importances_V6.csv')