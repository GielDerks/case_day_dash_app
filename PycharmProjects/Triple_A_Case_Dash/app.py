# coding: utf-8

import dash
from dash.dependencies import Input, Output
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import dash_table_experiments as dt
from sklearn.model_selection import cross_val_score
from sklearn.metrics import fbeta_score, make_scorer

app = dash.Dash(__name__)
server = app.server

app.config['suppress_callback_exceptions']=True

# Describe the layout, or the UI, of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),

   # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])

# read data
#dataset = pd.read_csv("dataset.csv")

claim_data = pd.read_csv("claim_data.csv")
policy_data = pd.read_csv("policy_dataset_fraud.csv")
data_load = pd.read_csv("datasetv2.csv", delimiter=';')
y=data_load['FraudFound_P']
del data_load['FraudFound_P']
del data_load['PolicyNumber']
X=pd.get_dummies(data_load)

feature_choice = []
for x in X.columns:
    dict1 = {}
    dict1["label"] = x
    dict1["value"] = x
    feature_choice.append(dict1)

# X_validation = pd.read_csv("X_validation.csv")
#policy_data = pd.read_csv("policy_data.csv")

trends_numbers = pd.read_excel("trend_excel_fraud.xlsx")

claims_input=[]
for x in claim_data.columns:
    dict1 = {}
    dict1["label"] = x
    dict1["value"] = x
    claims_input.append(dict1)

policy_input=[]
for x in policy_data.columns:
    dict2 = {}
    dict2["label"] = x
    dict2["value"] = x
    policy_input.append(dict2)

# fraud_dataset

# # read data for tables (one df per table)
# df_fund_facts = pd.read_csv('https://plot.ly/~bdun9/2754.csv')
# df_price_perf = pd.read_csv('https://plot.ly/~bdun9/2756.csv')
# df_current_prices = pd.read_csv('https://plot.ly/~bdun9/2753.csv')
# df_hist_prices = pd.read_csv('https://plot.ly/~bdun9/2765.csv')
# df_avg_returns = pd.read_csv('https://plot.ly/~bdun9/2793.csv')
# df_after_tax = pd.read_csv('https://plot.ly/~bdun9/2794.csv')
# df_recent_returns = pd.read_csv('https://plot.ly/~bdun9/2795.csv')
# df_equity_char = pd.read_csv('https://plot.ly/~bdun9/2796.csv')
# df_equity_diver = pd.read_csv('https://plot.ly/~bdun9/2797.csv')
# df_expenses = pd.read_csv('https://plot.ly/~bdun9/2798.csv')
# df_minimums = pd.read_csv('https://plot.ly/~bdun9/2799.csv')
# df_dividend = pd.read_csv('https://plot.ly/~bdun9/2800.csv')
# df_realized = pd.read_csv('https://plot.ly/~bdun9/2801.csv')
# df_unrealized = pd.read_csv('https://plot.ly/~bdun9/2802.csv')

#df_graph = pd.read_csv("https://plot.ly/~bdun9/2804.csv")

# reusable componenets
def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

# includes page/full view
def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='https://image.ibb.co/j5vUD8/AAA.jpg',

                                style={
                             'height': '55',
                             'width': '125'
                         })  # 529 × 234 = 2,26
        ], className="two columns padded"),

    ], className="row gs-header")
    return logo

# includes page/full view
# def get_logo():
#     logo = html.Div([
#             html.Img(src='https://image.ibb.co/j5vUD8/AAA.jpg', style={
#                              'height': '110',
#                              'width': '250',
#                              'float': 'right',
#                              'position': 'absolute',
#                          })  # 529 × 234 = 2,26
#         ])
#     return logo

def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'Fraud Analytics Case Study')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header padded")
    return header


def get_menu():

    menu = html.Div([

        dcc.Link('Introduction   ', href='/overview', className="tab first"),

        dcc.Link('Machine Learning Workflow  ', href='/price-performance', className="tab"),

        dcc.Link('The Data Set   ', href='/portfolio-management', className="tab"),

        dcc.Link('Modelling   ', href='/fees', className="tab"),

        dcc.Link('Evaluation   ', href='/distributions', className="tab"),

        dcc.Link('Conclusions   ', href='/news-and-reviews', className="tab")

    ], className="row ")

    return menu

## Page layouts
overview = html.Div([  # page 1


        html.Div([

            # Header

            get_header(),
            #get_logo(),

            html.Br([]),
            get_menu(),

            # Row 3

            html.Div([

                html.Div([

                    html.H6('1. Introduction',
                            className="gs-header gs-text-header padded"),

                    html.Br([]),

                    html.P("\
                            In this case we focus on a major issue for insurance companies: Fraudulent Claims."),
                    html.P("\
        Fraud, or criminal deception, is a costly problem for insurance companies and leads to losses of over billions of Euros."),
                    html.P("\
        The cost of fraud is twofold:"),

                    html.I("1. The direct cost of covering expenses for fraudulent claims"),
                    html.Br([]),
                    html.I("2. The cost of fraud prevention and detection."),

                    html.P("\
        Furthermore, these fraudulent also have a social-economic impact since the insurance companies costs or fraud are passed on to the policy holder by means of a higher premium \
        Insurance companies want to keep their premiums, for similar products, as low as possible compared to competitors in order to \
        attract new customers and increase marketshare. Therefore, fraud detection is a very important subject for insurance companies."),

                ], className="six columns"),

                html.Div([
                    html.H6(["2. About Fraud Detection"],
                            className="gs-header gs-table-header padded"),
                    html.Br([]),
                    html.P("\
                    Fraud detection systems based on data have been around for while. \
                    However, substantional improvements have been made in recents years with the introduction of new and improved fraud detection algorithms."),
                    html.P("\
                    Furthermore, insurers have become more and more data-driven organizations collecting large amounts of data. \
                    This data can be collected from their own systems, but also from open data sources or bought from data providers. \
                    The current challenge for insurers is to leverage the new advancements in machine learning and \
                    the ever-growing data available in order to improve their fraud detection systems."),

                ], className="six columns"),

            ], className="row"),

            # Row 4

            html.Div([

                html.Div([
                    html.H6('3. About the Case',
                            className="gs-header gs-text-header padded"),
                    html.Br([]),

                html.P("\
                We'll work with a dataset describing insurance transactions publicly available at Oracle Database Online Documentation (2015). \
                The dataset with claims data from an car insurance company that contains both fraudulent and valid claims. \
                This dataset is often used in scientific papers in the fraud prediction domain. \
                The data is from an American car insurance company and dates from around the year 2000."),

                html.P("\
                            In this case you are going to develop a prototype of a predictive machine learning model that can be embedded in a car insurer's fraud detection system."),

                html.P("\
                For the next two hours, You will:"),

                html.I("\
                Be divided in teams"),
                html.Br([]),
                html.I("\
                Develop a model that, as accurately as possible, identifies fraudulent claims"),
                html.Br([]),
                html.I("\
                Compare your model's performance to other groups."),
                html.Br([]),
                html.I("\
                Maybe win a prize :) "),
                html.Br([]),

                ], className="six columns"),

                html.Div([
                    html.H6("4. The Data Set",
                            className="gs-header gs-table-header padded"),
                    html.P(" sometext"),
                    html.Table(make_dash_table(trends_numbers)),
                ], className="six columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")


pricePerformance = html.Div([  # page 2

    html.Div([
        ], className="subpage")

    ], className="page")


portfolioManagement = html.Div([ # page 3


        html.Div([

            # Header

            #get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6(["The Data Set"],
                            className="gs-header gs-table-header padded")
                ], className="twelve columns"),

            ], className="row "),

            html.P("The insurers administration system consists of two datasets. The first dataset (Policy Data Set) contains information about the policy and contains 14 columns and 49128 records. Some of the variables are for example: The brand of the car, the policy holder's gender and age, the price, etc. This data is all gathered by the insurance company when you subscribe to their policy."),
            html.P("The second dataset (Claims Data Set) contains information about the claim and contains 18 columns and 12335 entries. This data is gathered by the insurance company at the moment that a policy holder files a claim. Some of the variables are for example: The date, the kind of area the accident took place, if a police report was filed, if witnesses were present, etc."),
            html.Br([]),
            html.P("Select a dataset in the dropdown below to show the data in the table below. The dropdown below the datatable shows all column for the chosen dataset. The left graph shows the distribution of the chosen column in the dataset. The right column shows the fraud percentage for every categorie in that column."),
            html.P("This step in the process is called Exploratory Data Analysis (EDA). Exploratory Data Analysis (EDA) refers to using techniques to display data in such a way that interesting features will become apparent. Unlike classical methods which usually begin with an assumed model for the data, EDA techniques are used to encourage the data to suggest models that might be appropriate"),
            html.Br([]),
            html.H6("Which interesting pattern did you find?"),

            html.Br([]),

            dcc.Dropdown(
                id='dropdown_dataset',
                options=[
                    {'label': 'Claims Data Set', 'value': 'Claims Data Set'},
                    {'label': 'Policy Data Set', 'value': 'Policy Data Set'}],
                value='Claims Data Set'
            ),

            html.Br([]),

            html.Div([
                html.Div([
                    dt.DataTable(
                        rows=claim_data.to_dict('records'),
                        sortable=True,
                        editable=False,
                        filterable=False,
                        #column_widths=30,
                        #row_selectable=True,
                        #header_row_height=30,
                        #row_height=30,
                        id='DataTable'),
                ], className="twelve columns"),
                #
                # html.Div([
                #     html.H6(""),
                # ], className="one columns"),

            ], className="row "),

            html.Br([]),

            dcc.Dropdown(
                id='dropdown_column_viz',
                options=[claims_input
                ],
                value=claims_input[0]
            ),

            html.Br([]),

            html.Div([

                html.Div([
                    dcc.Graph(
                        id='graph_data_viz1',
                        style={'height': '55vh'})
                ], className="six columns"),

                html.Div([
                    dcc.Graph(
                        id='graph_data_viz2',
                        style={'height': '55vh'})
                ], className="six columns"),


            ], className="row "),


            html.Br([]),

        ], className="subpage")

    ], className="page")

## Call back graph_data_viz1

@app.callback(
    dash.dependencies.Output('graph_data_viz1', 'figure'),
    [dash.dependencies.Input('dropdown_column_viz', 'value'),
     dash.dependencies.Input('dropdown_dataset', 'value')])
def update_figure_company(column, dataset):

    #Bar chart met gemiddelde van sector en gemiddelde van branche met naam van de branche

    # list with categorical

    print(dataset, column)
    if type(column) == dict:
        column = column['value']


    if dataset == 'Policy Data Set':
        data = policy_data
    else:
        data = claim_data

    data['count'] = 1

    grouper = data.groupby(column).count().reset_index()
    #print(grouper)
    categories = list(grouper[column])
    values = list(grouper['count'])

    return {
            'data': [
                {'x': categories, 'y': values, 'type': 'bar'},
            ],
            'layout': {'margin': {'l': 40, 'r': 40, 't': 30, 'b': 150}, 'title': 'Category Distribution',
                       'yaxis' : {'title':'Count'}}
        }

# Callback graph_data_viz
@app.callback(
    dash.dependencies.Output('graph_data_viz2', 'figure'),
    [dash.dependencies.Input('dropdown_column_viz', 'value'),
     dash.dependencies.Input('dropdown_dataset', 'value')])
def update_figure_company(column, dataset):

    #Bar chart met gemiddelde van sector en gemiddelde van branche met naam van de branche

    # list with categorical

    print(dataset, column)
    if type(column) == dict:
        column = column['value']


    if dataset == 'Policy Data Set':
        data = policy_data
    else:
        data = claim_data

    data['count'] = 1

    grouper = data.groupby(column).sum().reset_index()
    print(grouper)

    categories = grouper['FraudFound_P'] / grouper['count'] * 100
    print(categories)
    values = list(categories)
    categories = list(grouper[column])

    return {
            'data': [
                {'x': categories, 'y': values, 'type': 'bar'},
            ],
            'layout': {'margin': {'l': 40, 'r': 40, 't': 30, 'b': 150}, 'title': 'Distribution of Fraud Cases per Categorie',
                       'yaxis' : {'title':'Percentage of total claims marked as Fraudulent %'}}
        }

# Callback DataTable
@app.callback(
    dash.dependencies.Output('DataTable', 'rows'),
    [dash.dependencies.Input('dropdown_dataset', 'value')])
def set_rows_dt(dataset):

    if dataset == 'Policy Data Set':
        return policy_data.to_dict('records')
    else:
        return claim_data.to_dict('records')

#update columns dataset tab

@app.callback(
    dash.dependencies.Output('dropdown_column_viz', 'options'),
    [dash.dependencies.Input('dropdown_dataset', 'value')])
def set_columns(dataset):

    if dataset == 'Policy Data Set':
        return policy_input
    else:
        return claims_input

@app.callback(
    dash.dependencies.Output('dropdown_column_viz', 'value'),
    [dash.dependencies.Input('dropdown_dataset', 'value')])
def set_columns(dataset):

    if dataset == 'Policy Data Set':
        return policy_input[0]
    else:
        return claims_input[0]

feesMins = html.Div([  # page 4

        html.Div([

            # Header

            #get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6(["Feature Selection"],
                            className="gs-header gs-table-header padded")
                ], className="twelve columns"),

            ], className="row "),

            html.Br([]),

            html.P('Feature selection is: \
                    Selecting the variables which will be used in the model Feature engineering is: \
                    Creating new features that make machine learning algorithms workFeature engineering is \
                    fundamental to the application of machine learning, and is both difficult and expensive. \
                    Coming up with features is difficult, time-consuming and requires expert knowledge.'),

            html.P('The features in your data are important to the predictive models you use and will influence the results you are going to achieve. \
                    The quality and quantity of the features will have great influence on whether the model is good or not'),

            html.P('Some of the steps in feature engineering: \
                    1. Brainstorming or Testing features \
                    2. Deciding what features to create \
                    3. Creating features \
                    4. Checking how the features work with your model \
                    5. Improving your features if needed \
                    6 . Go back to brainstorming/creating more features until the work is do'),


            html.Div([

                html.Div([
                    dcc.Dropdown(
                        id='dropdown_feature_selection',

                        options=[
                            {'label': '5', 'value' : '5'},
                            {'label':'10', 'value' :  '10'},
                            {'label':'25', 'value' :  '25'},
                            {'label':'50', 'value' :  '50'},
                            {'label':'75', 'value' : '75'},
                            {'label':'100', 'value' :  '100'},
                            {'label':'150', 'value' :  '150'},
                            {'label':'200', 'value' :  '200'},
                            {'label':'250', 'value' :  '250'},
                        ],
                        value='10')
                ], className="six columns"),

                html.Div([
                    dcc.Dropdown(
                        id='chosen_features',
                        options=feature_choice,
                        multi=True,
                        value=['Age', 'Year']
                    )
                ], className="six columns"),

            ], className="row "),


            html.Br([]),


            dcc.Graph(
                id='graph_feature_selection',
                style={'height': '55vh'})
            #],
            # className="twelve columns"),

        ], className="subpage")

    ], className="page")


@app.callback(
    dash.dependencies.Output('graph_feature_selection', 'figure'),
    [dash.dependencies.Input('dropdown_feature_selection', 'value'),
     dash.dependencies.Input('chosen_features', 'value')])
def feature_selection(n_estimators, features):

    # Build a forest and compute the feature importances
    forest = RandomForestClassifier(n_estimators=int(n_estimators), class_weight= 'balanced')
    print(features)
    print(n_estimators)

    #select column based on dropdown selectors
    if len(features) == 1 or len(features) == 0:
        X_train = X[['Age', 'Year']]
    else:
        X_train = X[features]

    # Fit forest

    forest.fit(X_train, y)

    # calculate feature importances

    importances = forest.feature_importances_

    # calculate std

    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)

    indices = np.argsort(importances)[::-1]

    list_col = []
    for f in range(X_train.shape[1]):
        list_col.append(list(X_train.columns)[indices[f]])
        # print("%d. feature %f (%f)" % (f + 1, list(X.columns)[indices[f]], importances[indices[f]]))

    list4 = []
    std_list = []
    for x in indices:
        list4.append(importances[x])
        std_list.append(std[x])

    # Plot the feature importances of the forest
    df = pd.DataFrame({"importance": list4, 'columns': list_col, 'std':std_list})



    return {
            'data': [
                {'x': df['columns'], 'y': df["importance"], 'type': 'bar',
                 'error_y' : {'type': 'data', 'array' : df['std'], 'visible' : True}
                 },
            ],
            'layout': {'margin': {'l': 40, 'r': 40, 't': 30, 'b': 150}, 'title': 'Relative Feature Importance',
                       'yaxis' : {'title':'Feature Importance'}}
        }


distributions = html.Div([  # page 5

        html.Div([

           html.Div([

            # Header

            #get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            ], className="row "),

            # Row 1

            html.Div([

                html.Div([
                    html.H6(["Model Building"],
                            className="gs-header gs-table-header padded")
                ], className="twelve columns"),

            ], className="row "),

            html.Br([]),

            html.Div([

                html.Div([
                     html.H6(['Choose features to train model:']),
                ], className="eight columns"),

              ], className="row"),

                html.Br([]),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='chosen_features_model',
                        options=feature_choice,
                        multi=True,
                        value=['Age', 'Year']
                    )
                ], className="eight columns"),

            ], className='row'),

            html.Br([]),

            html.Div([
                html.Div([

                 html.H6(['N Estimators']),

                ], className="two columns"),

                html.Div([
                    html.H6(['Max Tree Depth']),
                ], className="two columns"),

                html.Div([
                    html.H6(['K-Fold Cross-Validation']),
                ], className="two columns"),
                html.Div([
                    html.H6('', id='depth_text'),
                ], className="three columns"),
        ], className = 'row'),

            html.Br([]),

            html.Div([

                    html.Div([

                        dcc.Dropdown(
                            id='dropdown_n_estimators_model',
                            options=[
                                {'label': '5', 'value': '5'},
                                {'label': '10', 'value': '10'},
                                {'label': '25', 'value': '25'},
                                {'label': '50', 'value': '50'},
                                {'label': '75', 'value': '75'},
                                {'label': '100', 'value': '100'},
                                {'label': '150', 'value': '150'},
                                {'label': '200', 'value': '200'},
                                {'label': '250', 'value': '250'},
                            ],
                            value='10')

                    ], className="two columns"),

                    html.Div([

                        dcc.Dropdown(
                            id='max_depth_slider',
                            options=[
                                {'label': '5', 'value': '5'},
                                {'label': '10', 'value': '10'},
                                {'label': '25', 'value': '25'},
                                {'label': '50', 'value': '50'},
                                {'label': '75', 'value': '75'},
                                {'label': '100', 'value': '100'},
                                {'label': '150', 'value': '150'},
                                {'label': '200', 'value': '200'},
                                {'label': '250', 'value': '250'},
                            ],
                            value='10')

                ] , className="two columns"),

                html.Div([

                    dcc.Dropdown(
                        id='cross_validation',
                        options=[
                            {'label': '5', 'value': '5'},
                            {'label': '10', 'value': '10'}],
                        value='10',
                    )
                ], className="two columns"),


                html.Div([

                    dcc.Slider(
                        id='max_leaf_nodes',
                        min=2,
                        max=150,
                        step=1,
                        value=50,
                    )
                ], className="three columns"),

            ], className="row "),

            html.Br([]),

            html.Br([]),

            html.Div([
                html.Div([
                    dt.DataTable(
                        rows=pd.DataFrame({'Turn': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                                           'Score': [0.7700404858299595, 0.8097165991902834, 0.7909238249594813, 0.7664233576642335, 0.7907542579075426, 0.7850770478507705, 0.7656123276561233, 0.7956204379562044, 0.7793998377939984, 0.7769667477696675]
                                                }).to_dict('records'),
                        columns=['Turn', 'Score'],
                        sortable=True,
                        editable=False,
                        filterable=False,

                        id='DataTable_cv'),

                ], className="twelve columns"),

            ], className="row "),

            html.Br([]),



        ], className="subpage")

    ], className="page")

@app.callback(
    dash.dependencies.Output('DataTable_cv', 'rows'),
    [dash.dependencies.Input('max_leaf_nodes', 'value'),
     dash.dependencies.Input('max_depth_slider', 'value'),
     dash.dependencies.Input('chosen_features_model', 'value'),
     dash.dependencies.Input('dropdown_n_estimators_model', 'value'),
     dash.dependencies.Input('cross_validation', 'value')])
def run_model(max_leaf_nodes, max_depth_slider, chosen_features_model, dropdown_n_estimators_model, cross_validation):
    print(max_leaf_nodes, max_depth_slider, chosen_features_model, dropdown_n_estimators_model, cross_validation)
    print("hoi")
    # Build a forest and compute the feature importances
    forest = RandomForestClassifier(n_estimators=int(dropdown_n_estimators_model), class_weight='balanced')

    #select column based on dropdown selectors
    if len(chosen_features_model) == 1 or len(chosen_features_model) == 0:
        X_train = X[['Age', 'Year']]
    else:
        X_train = X[chosen_features_model]

    # Fit forest
    print(X_train[0:3])
    forest.fit(X_train, y)

    #train model and output datatable

    ftwo_scorer = make_scorer(fbeta_score, beta=1)

    scores = cross_val_score(forest, X_train, y, cv=int(cross_validation), scoring=ftwo_scorer)
    print(scores)

    list4 = []
    list5 = []

    for x in range(1, len(list(scores))+1):
        list4.append(scores[x-1])
        list5.append(str(x))

    # list5.append('Average')
    # list4.append(scores.mean())
    # list5.append('Standard Deviation')
    # list4.append(scores.std())
    # print(list4, list5)

    df = pd.DataFrame({'Turn' : list5,'Score':list4})
    print(list(df['Turn']), list(df['Score']))
    return df.to_dict('records')

@app.callback(
    dash.dependencies.Output('depth_text', 'children'),
    [dash.dependencies.Input('max_leaf_nodes', 'value')])
def update_slider1_test(value):
    return 'Max Leaf Nodes = {} Splits'.format(str(value))

newsReviews = html.Div([  # page 6

        html.Div([

            # Header
        html.Div([
            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),


            ], className="row ")

        ], className="subpage")

    ], className="page")

noPage = html.Div([  # 404

    html.P(["404 Page not found"])

    ], className="no-page")



# Update page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/overview':
        return overview
    elif pathname == '/price-performance':
        return pricePerformance
    elif pathname == '/portfolio-management':
        return portfolioManagement
    elif pathname == '/fees':
        return feesMins
    elif pathname == '/distributions':
        return distributions
    elif pathname == '/news-and-reviews':
        return newsReviews
    else:
        return noPage



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/gielderks/pen/odryNY.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js"]

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(debug=True)
