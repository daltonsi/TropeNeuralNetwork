# Trope-Enabled Neural Network for Predicting Film Ratings
## Thesis Project for Winter 2017 Big Data Analytics Course
### Dalton Simancek and Dana Camerik

## INTRODUCTION

#### Story Yardsticks - A Call for Measuring Narrative Content
Stories are incredibly complex creations - capable of study in their structure, properties, composition, mechanisms as well as reactions from an audience. Authors and narratology scholars have produced a breadth of models for interpreting and understanding the structure of narrative characteristics and its various patterns and subcomponents.

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/heros_journey.png?raw=true">
<br><br>
<font color="blue">Figure 1: Joseph Campbell's The Hero's Journey</font>
</p>

<br><br>

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/vonnegut2.gif?raw=true">
<br><br>
<font color="blue">Figure 2: Kurt Vonnegut's The Shape of Stories</font>
</p>

<br><br>

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/Periodic-Table-of-Storytelling.jpg?raw=true">
<br><br>
<font color="blue">Figure 3: James Harris's Periodic Table of Storytelling</font>
</p>

Each of these models suggest a potential for representing narrative in an encoded data structure that may offer utility as a computational tool. Production companies could use such a tool to measure and weigh the narrative content of a project for its potential to resonate with an audience and/or generate profits. Online streaming users could benefit from improved recommendation engines through a more thorough analysis of narrative features. Generative and/or user choice-driven stories for interactive and virtual reality applications may be improved through the insights gleaned from the analysis of narrative structures.   

#### Harnessing the Utility of Narrative Content
In order to harness the utility of narrative content, a classification system and dictionary of subcomponents is needed to tag and interpret the various subcomponents and trends of narrative structures. One option would be to generate narrative features using Natural Language Processing(NLP) and Computer Vision(CV) techniques - training systems to learn and identify narrative features without human input in text and visual forms respectively.

While this project does not directly explore the potential of such intelligent text/image tagging systems, we acknowledge that their potential quality will only increase as NLP and CV processes become more and more sophisticated. Instead, this project relies on narrative feature tags already generated by humans.

TVtropes(http://tvtropes.org/) is an online community of users dedicated to viewing and tagging media content based on a shared common dictionary of narrative shorthands and features - i.e. Tropes. Thus, instead of building a narrative tagging system, we are taking advantage of the data generated by the TVtropes community. We thank Sam Carton(https://www.si.umich.edu/people/samuel-carton) for allowing us to use the data that he scraped from the TVtropes wiki for our project.

As a first step in exploring the utility of narrative data, this project aimed to explore the predictive power of the trope information for a movie's prestige. We created a neural network predictive model using the trope profile of a movie to predict a movie's IMDB rating. Given a model that accurately predicts a movie's IMDB rating using trope features allows us to comment on narrative metrics for success and the resulting implications for further research and the potential of narrative data-powered applications. 


## Data 
All trope and movie data was scraped from TVTropes.com and Wikipedia by Sam Carton(scarton@umich.edu) in November 2015. A total of 21,206 unique tropes and 13,138 movies were included in the tvtropes data. IMDB data - including IMDB rating - for each of the 13,138 movies was retrieved using the OMDB API in a python script. 

The raw data was filtered using the following criteria:
- Tropes with a frequency of 25 or less occurrences in the movie data are excluded.
- Movies without an IMDB rating are excluded.

A total of 4,336 tropes and 6,708 movies were selected from the raw data to train and test the neural network.

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/trope_frequency_top500.png?raw=true">
<br><br>
<font color="blue">Figure 4: Distribution of Trope Frequencies</font>
</p>


## Methods

### Feature Selection
Given the wide range of trope features, we calculated Pearson correlations between each trope and IMDB rating. Coefficients ranged from +/- 0.15 with p-values <<< 0.05. 

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/Best_Worst_Plot_Comparison.png?raw=true">
<br><br>
<font color="blue">Figure 5: Correlations with IMDB rating for Best and Worst tropes</font>
</p>

<br><br>

Below are the results for top 5 and bottom 5 tropes correlated with IMDB rating, which provide intuitive insights for using trope-features in the neural network model.

### Top 5 Tropes Correlated with IMDB Rating
   #### 1. Bittersweet Ending
       - 0.1458 (p-value: 3.11E-33)
       - When victory came at a harsh price, when, for whatever reason, the heroes cannot fully enjoy the reward of their actions, when some irrevocable loss has happened during the course of the events, and nothing will ever be the same again.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/BittersweetEnding

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/bittersweet_ending_3.jpg?raw=true">
<br><br>
<font color="blue">Lord of the Rings - The Return of the King (2003) </font>
</p>

  #### 2. Foreshadowing
       - 0.1284 (p-value: 4.57E-26)
       - A clue or allusion embedded in the narrative that predicts some later event or revelation.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/Foreshadowing
  #### 3. Deadpan Snarker
       - 0.1221 (p-value: 1.08E-23)
       - A character prone to gnomic, sarcastic, sometimes bitter, occasionally whimsical asides. They can vary wildly from rare, funny one-liners to complete obnoxiousness.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/DeadpanSnarker
   #### 4. Bookends
       - 0.1195 (p-value: 9.24E-23)
       - Matching scenes at the beginning and end of a story, often to show how things have changed through the course of the series, or to demonstrate that they haven't changed at all.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/BookEnds
  #### 5. Heroic BSOD
       - 0.1110 (p-value: 7.5E-20)
       - A stunning revelation or horrible event affects a character or someone they care deeply about, leaving them shocked to the point of mentally shutting down for a while
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/HeroicBSOD
<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/heroic_bsod.jpg?raw=true">
<br><br>
<font color="blue">The Dark Knight (2008) </font>
</p>

A crude subjective analysis of the top 5 tropes correlated IMDB rating suggest the following intuitive narrative characteristics of highly successful movies:
- Narrative Structural Intent (Bookends/Foreshadowing)
- Dramatic stakes/unrest (Heroic BSOD/Bittersweet Ending)
- Wit/comedic relief (Deadpan Snarker)


### Bottom 5 Tropes Correlated with IMDB Rating
  #### 1. Dull Surprise
       - -0.1464 (p-value: 1.91E-33)
       - A vague, wispy look given by a character in response to something that, theoretically, should produce a more intense or specific expression of shock, horror, or revelation.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/DullSurprise

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/dull_surprise.JPG?raw=true">
<br><br>
<font color="blue">Twilight (2008) </font>
</p>

  #### 2. Stock Footage
       - -0.1039 (p-value: 0.0000000000000000148)
       - A shot or series of shots reused in two or more productions.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/StockFootage
  #### 3. Super-Persistent Predator
       - -0.0902 (p-value: 0.000000000000139)
       - Villain, Monster or antagonistic force that pursues the protagonist in excess, often beyond the call of common sense.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/SuperPersistentPredator
  #### 4. B-Movie
       - -0.0893 (p-value: 0.000000000000238)
       - Productions explicitly intended to be cheap, disposable entertainment.
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/BMovie
  #### 5. Numbered Sequels
       - -0.0883 (p-value: 0.000000000000428)
       - A stunning revelation or horrible event affects a character or someone they care deeply about, leaving them shocked to the point of mentally shutting down for a while
       - http://tvtropes.org/pmwiki/pmwiki.php/Main/NumberedSequels

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/named_sequels.jpg?raw=true">
<br><br>
<font color="blue">Shrek Forever After (2010) </font>
</p>



A crude subjective analysis of the Bottom 5 tropes correlated IMDB rating suggest the following intuitive narrative characteristics of unsuccessful movies:
- Slasher Films (Super Persistent Predator)
- Cheap Production/“Lazy” Filmmaking (B-Movie, Stock Footage, Dull Surprise, Numbered Sequels)
- Cheap Thrills (B-Movie, Stock Footage, Super Persistent Predator)
- Bad Acting (Dual Surprise,B-Movie)

This preliminary trope analysis generated both statistical and intuitive support for using narrative features - tropes - in the training of a neural network model for predicting IMDB rating. 

### Building the Training/Test Data
Given the support of the trope correlation analysis, the baseline master data table includes each trope as an individual feature as well as select IMDB data variables(e.g. Runtime) 

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/trope_data_table.png?raw=true">
<br><br>
<font color="blue">Figure 6: Data Table Sample </font>
</p>

In addition to the one hot vectors for each trope and select IMDB data, we brainstormed other opportunities to explore the trope data and generate additional features (Trope Clustering, Trope Hierarchies, Time Series and more - see LIMITATIONS and FURTHER WORK) As a first step in generating complex trope features, we calculated regression coefficients for the times series of each trope (normalized by number of movies per year). The time series coefficients for the tropes of a particular movie were then averaged and included as an overall trope time series feature score with the hope of accounting some signals related to trope usage over time. 

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/time_series_example.png?raw=true">
<br><br>
<font color="blue">Figure 7: Time Series Regression Analysis - Shout Out </font>
</p>

Given the final master table including trope feature, IMDB data features and a trope time series score, we randomly divided the 6,708 movies into a training dataset of 5,366 movies and a test dataset of 1,342 movies.

### Building and Training the Neural Network

To build the neural network, we used the Keras Deep Learning Library(https://keras.io/) for Python. 

<p align="center">
<img src="https://github.com/daltonsi/TropeNeuralNetwork/blob/master/pictures/neural_network_viz.png?raw=true">
<br><br>
<font color="blue">Figure 8: Trope Neural Network for Predicting IMDB Rating </font>
</p>

Not only does a Neural Network offer the potential to consider movie features from multiple subdomains(narrative tropes, IMDB movie information and more), it also allows for the possibility to capture deeper interactions of two or more features.  

All neural network models were trained using a variety of features to predict a film's IMDB rating. Performance was measured using Mean Squared Error between the IMDB rating predictions with the actual IMDB rating. A baseline model was built using no hidden layers only using the year of the movie as the sole feature. From there, all features were added to test and improve results. In addition to feature inclusion experimentation, the neural network was tuned by changing parameters(i.e. number of hidden layers, size of hidden layers, batch sizes, number of epochs) in order to optimize performance.  



A notable feature we are using to develop our neural network is time series, that is, how much usage of a trope has changed over time. In particular, we are focusing on the ratio between the number of movies a trope is used in vs. the total number of movies released for each year in order to normalize the relationship. We are achieving this using visualizations for commonly used tropes, as well as calculating linear regression coefficients for a larger number of tropes.



## Results

### Baseline Model
- Mean Squared Error = 1.660
- IMDB Movie Year only
- 1 Hidden Layer
- 100 Epochs
- Batch Size = 5

### Best Model
- Mean Squared Error = 1.022
- 3 Hidden Layers (2150, 1000 and 500 nodes respectively)
- 120 Epochs
- Batch Size = 10


## Conclusions

## Limitations and Further Work


### Using Wiki Community Data
While TVtropes shares community customs for writing and maintaining the catalogue of tropes(http://tvtropes.org/pmwiki/pmwiki.php/Administrivia/TVTropesCustoms), there are no benchmarks for completion. Tasks related to naming tropes and maintaining an accurate and complete tagging of movies are largely dependent on the behavior and interest of the wiki community. As a result, popular movies would receive more interest/better tagging. Unpopular projects would have less favorable attention. Thus, there are inherent biases in the wiki community and the data they generate that can be acknowledged, even if those biases are not fully understood for this project. 

### Capturing Better Trope Features 
For many tropes, the wiki community groups subsets of tropes into categories and hierarchies. Our methodology treats as trope as a distinct unit, which is not the case. Our filtering techniques removed tropes with lower frequency, yet they may in fact be a specialized trope in a more generic category. Further work could explore the organization of tropes to capture trope information in a more meaningful manner.  

### Multi-Model Comparison
Neural Networks offer one of many models for the prediction task of this work. Further work could compare the performance of the neural network against other machine learning models.  Doing so would further elucidate the advantages and disadvantages of using neural networks to capture and use trope information.

## Appendix

### Presentation Poster
![alt text](https://github.com/daltonsi/TropeNeuralNetwork/blob/master/poster.png?raw=true)
