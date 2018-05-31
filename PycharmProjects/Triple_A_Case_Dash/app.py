# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os

import dash_table_experiments as dt

app = dash.Dash(__name__)
server = app.server

app.config['suppress_callback_exceptions']=True

# Describe the layout, or the UI, of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])

# read data
#dataset = pd.read_csv("dataset.csv")

claim_data = pd.read_csv("claim_data.csv")
policy_data = pd.read_csv("policy_data.csv")

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

# read data for tables (one df per table)
df_fund_facts = pd.read_csv('https://plot.ly/~bdun9/2754.csv')
df_price_perf = pd.read_csv('https://plot.ly/~bdun9/2756.csv')
df_current_prices = pd.read_csv('https://plot.ly/~bdun9/2753.csv')
df_hist_prices = pd.read_csv('https://plot.ly/~bdun9/2765.csv')
df_avg_returns = pd.read_csv('https://plot.ly/~bdun9/2793.csv')
df_after_tax = pd.read_csv('https://plot.ly/~bdun9/2794.csv')
df_recent_returns = pd.read_csv('https://plot.ly/~bdun9/2795.csv')
df_equity_char = pd.read_csv('https://plot.ly/~bdun9/2796.csv')
df_equity_diver = pd.read_csv('https://plot.ly/~bdun9/2797.csv')
df_expenses = pd.read_csv('https://plot.ly/~bdun9/2798.csv')
df_minimums = pd.read_csv('https://plot.ly/~bdun9/2799.csv')
df_dividend = pd.read_csv('https://plot.ly/~bdun9/2800.csv')
df_realized = pd.read_csv('https://plot.ly/~bdun9/2801.csv')
df_unrealized = pd.read_csv('https://plot.ly/~bdun9/2802.csv')

df_graph = pd.read_csv("https://plot.ly/~bdun9/2804.csv")

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

        dcc.Link('Fees & Minimums   ', href='/fees', className="tab"),

        dcc.Link('Distributions   ', href='/distributions', className="tab"),

        dcc.Link('News & Reviews   ', href='/news-and-reviews', className="tab")

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

            # Header
            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row ``

            html.Div([

                html.Div([
                    html.H6(["Current Prices"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_current_prices))

                ], className="six columns"),

                html.Div([
                    html.H6(["Historical Prices"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_hist_prices))
                ], className="six columns"),

            ], className="row "),

            # Row 2

            html.Div([

                html.Div([
                    html.H6("Performance",
                            className="gs-header gs-table-header padded"),
                    dcc.Graph(
                        id='graph-4',
                        figure={
                            'data': [
                                go.Scatter(
                                    x = df_graph['Date'],
                                    y = df_graph['Vanguard 500 Index Fund'],
                                    line = {"color": "rgb(53, 83, 255)"},
                                    mode = "lines",
                                    name = "Vanguard 500 Index Fund"
                                ),
                                go.Scatter(
                                    x = df_graph['Date'],
                                    y = df_graph['MSCI EAFE Index Fund (ETF)'],
                                    line = {"color": "rgb(255, 225, 53)"},
                                    mode = "lines",
                                    name = "MSCI EAFE Index Fund (ETF)"
                                )
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                width = 700,
                                height = 200,
                                font = {
                                    "family": "Raleway",
                                    "size": 10
                                  },
                                 margin = {
                                    "r": 40,
                                    "t": 40,
                                    "b": 30,
                                    "l": 40
                                  },
                                  showlegend = True,
                                  titlefont = {
                                    "family": "Raleway",
                                    "size": 10
                                  },
                                  xaxis = {
                                    "autorange": True,
                                    "range": ["2007-12-31", "2018-03-06"],
                                    "rangeselector": {"buttons": [
                                        {
                                          "count": 1,
                                          "label": "1Y",
                                          "step": "year",
                                          "stepmode": "backward"
                                        },
                                        {
                                          "count": 3,
                                          "label": "3Y",
                                          "step": "year",
                                          "stepmode": "backward"
                                        },
                                        {
                                          "count": 5,
                                          "label": "5Y",
                                          "step": "year"
                                        },
                                        {
                                          "count": 10,
                                          "label": "10Y",
                                          "step": "year",
                                          "stepmode": "backward"
                                        },
                                        {
                                          "label": "All",
                                          "step": "all"
                                        }
                                      ]},
                                    "showline": True,
                                    "type": "date",
                                    "zeroline": False
                                  },
                                  yaxis = {
                                    "autorange": True,
                                    "range": [18.6880162434, 278.431996757],
                                    "showline": True,
                                    "type": "linear",
                                    "zeroline": False
                                  }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )
                ], className="twelve columns")

            ], className="row "),

            # Row 3

            html.Div([

                html.Div([
                    html.H6(["Average annual returns--updated monthly as of 02/28/2018"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_avg_returns), className="tiny-header")
                ], className=" twelve columns"),

            ], className="row "),

            # Row 4

            html.Div([

                html.Div([
                    html.H6(["After-tax returns--updated quarterly as of 12/31/2017"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_after_tax), className="tiny-header")
                ], className=" twelve columns"),

            ], className="row "),

            # Row 5

            html.Div([

                html.Div([
                    html.H6(["Recent investment returns"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_recent_returns), className="tiny-header")
                ], className=" twelve columns"),

            ], className="row "),

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
                    html.H6(["The Data Set"],
                            className="gs-header gs-table-header padded")
                ], className="twelve columns"),

            ], className="row "),

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
                dcc.Graph(
                    id='graph_data_viz1',
                    style={'height': '80vh', 'width': '55vw'})
            ], className="six columns"),

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
    print(grouper)
    categories = list(grouper[column])
    values = list(grouper['count'])

    return {
            'data': [
                {'x': categories, 'y': values, 'type': 'bar'},
            ],
            'layout': {'margin': {'l': 40, 'r': 40, 't': 30, 'b': 150}, 'title': 'Distribution',
                       'yaxis' : {'title':'Count'}}
        }

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

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6(["Expenses"],
                            className="gs-header gs-table-header padded")
                ], className="twelve columns"),

            ], className="row "),

            # Row 2

            html.Div([

                html.Div([
                    html.Strong(),
                    html.Table(make_dash_table(df_expenses)),
                    html.H6(["Minimums"],
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_minimums))
                ], className="six columns"),

                html.Div([
                    html.Br([]),
                    html.Strong("Fees on $10,000 invested over 10 years"),
                    dcc.Graph(
                        id = 'graph-6',
                        figure = {
                            'data': [
                                go.Bar(
                                    x = ["Category Average", "This fund"],
                                    y = ["2242", "329"],
                                    marker = {"color": "rgb(53, 83, 255)"},
                                    name = "A"
                                ),
                                go.Bar(
                                    x = ["This fund"],
                                    y = ["1913"],
                                    marker = {"color": "#ADAAAA"},
                                    name = "B"
                                )
                            ],
                            'layout': go.Layout(
                                annotations = [
                                    {
                                      "x": -0.0111111111111,
                                      "y": 2381.92771084,
                                      "font": {
                                        "color": "rgb(0, 0, 0)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": "$2,242",
                                      "xref": "x",
                                      "yref": "y"
                                    },
                                    {
                                      "x": 0.995555555556,
                                      "y": 509.638554217,
                                      "font": {
                                        "color": "rgb(0, 0, 0)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": "$329",
                                      "xref": "x",
                                      "yref": "y"
                                    },
                                    {
                                      "x": 0.995551020408,
                                      "y": 1730.32432432,
                                      "font": {
                                        "color": "rgb(0, 0, 0)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": "You save<br><b>$1,913</b>",
                                      "xref": "x",
                                      "yref": "y"
                                    }
                                  ],
                                  autosize = False,
                                  height = 150,
                                  width = 340,
                                  bargap = 0.4,
                                  barmode = "stack",
                                  hovermode = "closest",
                                  margin = {
                                    "r": 40,
                                    "t": 20,
                                    "b": 20,
                                    "l": 40
                                  },
                                  showlegend = False,
                                  title = "",
                                  xaxis = {
                                    "autorange": True,
                                    "range": [-0.5, 1.5],
                                    "showline": True,
                                    "tickfont": {
                                      "family": "Raleway",
                                      "size": 10
                                    },
                                    "title": "",
                                    "type": "category",
                                    "zeroline": False
                                  },
                                  yaxis = {
                                    "autorange": False,
                                    "mirror": False,
                                    "nticks": 3,
                                    "range": [0, 3000],
                                    "showgrid": True,
                                    "showline": True,
                                    "tickfont": {
                                      "family": "Raleway",
                                      "size": 10
                                    },
                                    "tickprefix": "$",
                                    "title": "",
                                    "type": "linear",
                                    "zeroline": False
                                  }
                            )
                        },
                        config={
                            'displayModeBar': False
                        }
                    )
                ], className="six columns"),

            ], className="row "),

            # Row 3

            html.Div([

                html.Div([
                    html.H6(["Fees"],
                            className="gs-header gs-table-header padded"),

                    html.Br([]),

                    html.Div([

                        html.Div([
                            html.Strong(["Purchase fee"])
                        ], className="three columns right-aligned"),

                        html.Div([
                            html.P(["None"])
                        ], className="nine columns")


                    ], className="row "),

                    html.Div([

                        html.Div([
                            html.Strong(["Redemption fee"])
                        ], className="three columns right-aligned"),

                        html.Div([
                            html.P(["None"])
                        ], className="nine columns")

                    ], className="row "),

                    html.Div([

                        html.Div([
                            html.Strong(["12b-1 fee"])
                        ], className="three columns right-aligned"),

                        html.Div([
                            html.P(["None"])
                        ], className="nine columns")

                    ], className="row "),

                    html.Div([

                        html.Div([
                            html.Strong(["Account service fee"])
                        ], className="three columns right-aligned"),

                        html.Div([
                            html.Strong(["Nonretirement accounts, traditional IRAs, Roth IRAs, UGMAs/UTMAs, SEP-IRAs, and education savings accounts (ESAs)"]),
                            html.P(["We charge a $20 annual account service fee for each Vanguard Brokerage Account, as well as each individual Vanguard mutual fund holding with a balance of less than $10,000 in an account. This fee does not apply if you sign up for account access on vanguard.com and choose electronic delivery of statements, confirmations, and Vanguard fund reports and prospectuses. This fee also does not apply to members of Flagship Select™, Flagship®, Voyager Select®, and Voyager® Services."]),
                            html.Br([]),
                            html.Strong(["SIMPLE IRAs"]),
                            html.P(["We charge participants a $25 annual account service fee for each fund they hold in their Vanguard SIMPLE IRA. This fee does not apply to members of Flagship Select, Flagship, Voyager Select, and Voyager Services."]),
                            html.Br([]),
                            html.Strong(["403(b)(7) plans"]),
                            html.P(["We charge participants a $15 annual account service fee for each fund they hold in their Vanguard 403(b)(7) account. This fee does not apply to members of Flagship Select, Flagship, Voyager Select, and Voyager Services."]),
                            html.Br([]),
                            html.Strong(["Individual 401(k) plans"]),
                            html.P(["We charge participants a $20 annual account service fee for each fund they hold in their Vanguard Individual 401(k) account. This fee will be waived for all participants in the plan if at least 1 participant qualifies for Flagship Select, Flagship, Voyager Select, and Voyager Services"]),
                            html.Br([]),
                        ], className="nine columns")

                    ], className="row ")

                ], className="twelve columns")

            ], className="row "),

        ], className="subpage")

    ], className="page")

distributions = html.Div([  # page 5

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6(["Distributions"],
                            className="gs-header gs-table-header padded"),
                    html.Strong(["Distributions for this fund are scheduled quaterly"])
                ], className="twelve columns"),

            ], className="row "),

            # Row 2

            html.Div([

                html.Div([
                    html.Br([]),
                    html.H6(["Dividend and capital gains distributions"], className="gs-header gs-table-header tiny-header"),
                    html.Table(make_dash_table(df_dividend), className="tiny-header")
                ], className="twelve columns"),

            ], className="row "),

            # Row 3

            html.Div([

                html.Div([
                    html.H6(["Realized/unrealized gains as of 01/31/2018"], className="gs-header gs-table-header tiny-header")
                ], className=" twelve columns")

            ], className="row "),

            # Row 4

            html.Div([

                html.Div([
                    html.Table(make_dash_table(df_realized))
                ], className="six columns"),

                html.Div([
                    html.Table(make_dash_table(df_unrealized))
                ], className="six columns"),

            ], className="row "),

        ], className="subpage")

    ], className="page")

newsReviews = html.Div([  # page 6

        html.Div([

            # Header

            get_logo(),
            get_header(),
            html.Br([]),
            get_menu(),

            # Row 1

            html.Div([

                html.Div([
                    html.H6('Vanguard News',
                            className="gs-header gs-text-header padded"),
                    html.Br([]),
                    html.P('10/25/16    The rise of indexing and the fall of costs'),
                    html.Br([]),
                    html.P("08/31/16    It's the index mutual fund's 40th anniversary: Let the low-cost, passive party begin")
                ], className="six columns"),

                html.Div([
                    html.H6("Reviews",
                            className="gs-header gs-table-header padded"),
                    html.Br([]),
                    html.Li('Launched in 1976.'),
                    html.Li('On average, has historically produced returns that have far outpaced the rate of inflation.*'),
                    html.Li("Vanguard Quantitative Equity Group, the fund's advisor, is among the world's largest equity index managers."),
                    html.Br([]),
                    html.P("Did you know? The fund launched in 1976 as Vanguard First Index Investment Trust—the nation's first index fund available to individual investors."),
                    html.Br([]),
                    html.P("* The performance of an index is not an exact representation of any particular investment, as you cannot invest directly in an index."),
                    html.Br([]),
                    html.P("Past performance is no guarantee of future returns. See performance data current to the most recent month-end.")
                ], className="six columns"),

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
                #"https://codepen.io/bcd/pen/KQrXdb.css",
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
