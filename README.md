# Ticket Analysis App

Ticket Analysis is an mobile community application which offers its users the following features:

1. reporting a ticket.
2. getting a probability chance for  a ticket based on a location, time duration,date and weather.
3. getting a recommendation with a lower probability for a ticket nearby where you wanted to park      with an option to navigate to that location in waze.
4. showing a graph that contains the different amount of ticket that were reported in different hours      in the day, the information  showed  defends on the duration back the users chooses.

Front End:   
The front end was written in react native and uses google maps, TomTom API in order to show auto complete search options, and axios API in order to perform get and post HTTP requests.

Back End:  

The backend was written in python, uses libraries like pandas and a data MongoDB database in order to do analysis computations.
In addition it uses Flask in order to receive get and post requests from the front end.

---

### Home page

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/home-page.jpeg" width="40%" height="40%">

---

### Get Ticket Information

> Prediction request parameters: location, date and hours.

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/map.jpeg" width="40%" height="40%">

> There is help of auto-filling for the desired location:

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/map-autoFill.jpeg" width="40%" height="40%">

> Set wanted time and date:

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/choose-date.jpeg" width="40%" height="40%">

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/choose-hour.jpeg" width="40%" height="40%">

> Prediction example:
- Indicate if an inspector has recently moved in the area

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/ticket-analysis-result.jpeg" width="40%" height="40%">

> Get other nearby location to park:
- Search a nearby parking area with lower percentages to get a report. 
  If such a place is found, you could navigate there with 'Waze app'.

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/suggest-diffrernt-location.jpeg" width="40%" height="40%">

---

### Post Ticket Information

> Parameters for publishing information: location, date and time.
- Returning information Whether the data was successfully received in the system.

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/post-data.jpeg" width="40%" height="40%">

---

### Show Ticket Analysis

> Show a graph about the amount of reports that exist in the system at a particular location.

> Parameters: day a week, weather and how long back.

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/graph-analysis.jpeg" width="40%" height="40%">

> Graph example:
- Amount of reports that were at any one time

<img src="https://github.com/shayei/Ticket-Analysis/blob/master/images/graph-result.jpeg" width="40%" height="40%">

---

## ENJOY
