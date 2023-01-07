import streamlit as st
import pandas as pd
import csv
import nltk
# Download the lexicon
nltk.download("vader_lexicon")
nltk.download('stopwords')
# Import the lexicon

from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer

@st.cache
def analyze_sentiment(file_path):
  # Initialize the SentimentIntensityAnalyzer
  sia = SentimentIntensityAnalyzer()

  # Read in the comments from the CSV or TXT file
  comments = []
  with open(file_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      comments.append(row[0])

  # Analyze the sentiment of each comment using the sia.polarity_scores method
  scores = []
  for comment in comments:
    score = sia.polarity_scores(comment)
    scores.append(score)

  # Join all the comments into a single string and remove stopwords
  stopwords = nltk.corpus.stopwords.words('english')
  text = " ".join([comment for comment in comments if comment not in stopwords])

  # Generate a wordcloud of the comments
  wcloud = WordCloud(width=500, height=200, background_color='white', stopwords=stopwords).generate(text)

  # Count the number of positive, negative, and neutral comments
  pos_count = 0
  neg_count = 0
  neu_count = 0
  for score in scores:
    if score['compound'] > 0:
      pos_count += 1
    elif score['compound'] < 0:
      neg_count += 1
    else:
      neu_count += 1

  # Calculate the average sentiment score
  average_score = sum([score['compound'] for score in scores]) / len(scores)

  return comments, scores, wcloud, pos_count, neg_count, neu_count, average_score

st.header('Sentiment Analysis App')
st.markdown('This app analyzes the sentiments from various social media. Please pass a cleaned text in a csv format'
            ' to use it or try out the samples'
             ' VADER( Valence Aware Dictionary for Sentiment Reasoning) is an NLTK module that provides sentiment scores based on the words used. ')


# Add a sidebar to the app
st.sidebar.header('Options')

# Allow the user to select a CSV file from the sidebar or upload their own
st.sidebar.subheader('Input File')
file_1 = 'clean_marvel_comments.csv'
file_2 = 'ken_block_death.csv'
file_3 = 'trump_clean.csv'
uploaded_file = st.sidebar.file_uploader('Upload a CSV file')
if uploaded_file is not None:
  file = uploaded_file.getvalue().decode()
else:
  file = st.sidebar.radio('Or choose a default CSV file', options=[file_1, file_2, file_3])
if st.sidebar.button('Analyze'):
  # Analyze the sentiment of the comments in the selected file
  comments, scores, wcloud, pos_count, neg_count, neu_count, average_score = analyze_sentiment(file)
else:
# Analyze the sentiment of the comments in the selected file
  comments, scores, wcloud, pos_count, neg_count, neu_count, average_score = analyze_sentiment(file)

# Display the results in two columns
st.subheader('The comments')
st.subheader("")
st.dataframe(comments)


## DISPLAYING WORDCLOUD
st.subheader(':cloud: Wordcloud :cloud:')
st.subheader("")
st.set_option('deprecation.showPyplotGlobalUse', False) #Versioning of pyplot global
plt.imshow(wcloud, interpolation='bilinear')
plt.axis("off")
#plt.show()
st.pyplot()


# Display the results in 3 columns
first_column, second_column, third_column = st.columns([1,1.3,1.8])


with first_column:
  st.subheader('Bar Chart')

  fig = px.bar(x=['Positive', 'Negative', 'Neutral'], y=[pos_count, neg_count, neu_count])
  fig.update_layout(height=500, width=400)
  fig.update_layout(xaxis_title='Sentiment', yaxis_title='No of comments')
  st.plotly_chart(fig)

with second_column:
  st.write("")

with third_column:
  st.subheader(':arrow_down: Overall sentiment :arrow_down:')
  if pos_count > neg_count:
    st.image(Image.open('smiling_face.png'), width=300)
  elif pos_count < neg_count:
    st.image(Image.open('sad_face.png'), width=300)
  else:
    st.image(Image.open('neutral_face.png'), width=300)


  # Display the wordcloud in the first column
  # st.subheader('Wordcloud')
  # st.image(wordcloud, use_column_width=True)

  # Display the bar chart and smiley face in the second column