import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor,helper

df=pd.read_csv("C:\\Users\\SRN\\OneDrive\\Desktop\\Python\\projects\\olympics_till_2016\\athlete_events.csv")
region_df=pd.read_csv("C:\\Users\\SRN\\OneDrive\\Desktop\\Python\\projects\\olympics_till_2016\\noc_regions.csv")


df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    'Select an optoipon',
    ('Medal Tally','Overall Analysis', 'Country-wise Analysis','Athlete wise Analysis')
)

# st.dataframe(df)

if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country= helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year =='Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year !='Overall' and selected_country == 'Overall':
        st.title("Medal Tally in "+ str(selected_year)+ " Olympics")
    if selected_year =='Overall' and selected_country != 'Overall':
        st.title(str(selected_country)+": Overall performace")
    if selected_year !='Overall' and selected_country != 'Overall':
        st.title(str(selected_country)+": performance in "+str(selected_year)+ " Olympics")
    
    st.table(medal_tally)  

if user_menu== 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities= df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
        
    st.markdown("<h1>Top Statistics:</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<h2 style='color:blue;text-shadow: 2px 2px 2px #000;'>Editions</h4>", unsafe_allow_html=True)
        st.title(editions)
        st.markdown("---")
    with col2:
        st.markdown(f"<h2 style='color:green;text-shadow: 2px 2px 2px #000;'>Hosts</h3>", unsafe_allow_html=True)
        st.title(cities)
        st.markdown("---")
    with col3:
        st.markdown(f"<h2 style='color:orange;text-shadow: 2px 2px 2px #000;'>Sports</h3>", unsafe_allow_html=True)
        st.title(sports)
        st.markdown("---")

    # Second row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<h2 style='color:red;text-shadow: 2px 2px 2px #000;'>Events</h3>", unsafe_allow_html=True)
        st.title(events)
        st.markdown("---")
    with col2:
        st.markdown(f"<h2 style='color:purple;text-shadow: 2px 2px 2px #000;'>Athletes</h3>", unsafe_allow_html=True)
        st.title(athletes)
        st.markdown("---")
    with col3:
        st.markdown(f"<h2 style='color:pink;text-shadow: 2px 2px 2px #000;'>Nations</h3>", unsafe_allow_html=True)
        st.title(nations)
        st.markdown("---")

    #for year_vs_nation chart visualization
    year_vs_nation=helper.participating_nations_over_time(df)

    fig=px.line(year_vs_nation, x='Edition', y="Total Nations")

    st.title("Participating Nations over the Years")
    st.plotly_chart(fig)

    #for year_vs_event chart visualization
    year_vs_event=helper.total_events_over_the_years(df)

    fig=px.line(year_vs_event, x='Edition', y="Total Events")

    st.title("Total events conducted over the Years")
    st.plotly_chart(fig)

    #for year_vs_no.of_athletes chart visualization
    year_vs_athlete=helper.total_athletes_over_the_years(df)
    
    fig=px.line(year_vs_athlete, x='Edition', y="Total Athletes")

    st.title("Total athletes participated over the Years")
    st.plotly_chart(fig)

    #for heatmap of sports and the events over the years
    st.title("No.of Events in each Sports over the Years")
    fig,ax=plt.subplots(figsize=(20,20))

    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)

    st.pyplot(fig)

    #for most successfull Athletes
    st.title('Most successfull Athletes')

    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

#for country wise Analysis

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select a country',country_list)
    
    country_df=helper.yearwise_medal_tally(df,selected_country)

    fig=px.line(country_df, x='Year', y="Medal")

    st.title(selected_country + ": Medal Tally over the Years")
    st.plotly_chart(fig)

    #heatmap for country_event heatmap
    st.title(selected_country + ": excels in the following sports")

    pt=helper.country_event_heatmap(df,selected_country)

    fig,ax=plt.subplots(figsize=(20,20))

    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete wise Analysis':

    athlete_df=df.drop_duplicates(subset=['Name','region'])

    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)

    fig.update_layout(
    title="Distribution of Ages among Medalists",  # Title of the plot
    xaxis_title="Age",  # X-axis label
    yaxis_title="Density",  # Y-axis label
    legend_title="Medal Type",  # Legend title
    legend=dict(x=0.7, y=0.95),  # Adjust legend position
    )
    fig.update_layout(autosize=False,width=1000,height=600)

    st.plotly_chart(fig)


    #Distribution of Ages wrt Sport(Gold Medalist)
    
    all_sports=['Basketball', 'Judo', 'Football','Tug-Of-War', 'Athletics',
            'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions',
            'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
            'Rowing', 'Fencing', 'Equestrianism', 'Shooting', 'Boxing',
            'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
            'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
            'Volleyball', 'Synchronized Swimming', 'Table Tennis',
            'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
            'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo', 
            'Ice Hockey']
    
    x=[]   
    name=[]
    for sport in all_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)

    fig.update_layout(
    title="Distribution of Ages wrt Sport(Gold Medalist)",  # Title of the plot
    xaxis_title="Age",  # X-axis label
    yaxis_title="Density",  # Y-axis label
    legend_title="Medal Type",  # Legend title
    legend=dict(x=0.7, y=0.95),  # Adjust legend position
    )
    fig.update_layout(autosize=False,width=1000,height=600)

    st.plotly_chart(fig)


    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    st.title('Height vs Weight')
    selected_sports=st.selectbox('Select a Sport',sport_list)

    temp_df=helper.weight_vs_height(df,selected_sports)

    fig,ax=plt.subplots()

    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)

    st.pyplot(fig)

    st.title("Men vs Women Participation Over the Years")
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])

    fig.update_layout(autosize=False,width=1000,height=600)

    st.plotly_chart(fig)
 
