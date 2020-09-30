import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import {requestPermissionsAsync, watchPositionAsync, Accuracy} from 'expo-location'; 
import AutoCompleteSearchBar from './components/AutoCompleteSearchBar';
import MapComponent from './components/MapComponent';

const GetInfoScreen = (props)=>{

    const[stateRegion, setStateRegion] = useState({ latitude:32.07358,longitude: 34.78805, latitudeDelta: 0.00122, longitudeDelta: 0.00121});
    const[selectedTime, setTime] = useState({selectedHours: 0, selectedMinutes: 0,});
    const [err, setErr] = useState(null);
    const action = props.navigation.getParam('id',{});




    const navigate = ()=>{
      let route = "route";
      
      action == "dayAnalysis" ? route = "DayAnlysis" : route = "reporter";
      props.navigation.navigate(route, {action:action, longitude:stateRegion.longitude, latitude: stateRegion.latitude});

        };
    
    const TrackUserGPS = async () =>{
      try{
        await requestPermissionsAsync();
        await  watchPositionAsync({
          accuracy: Accuracy.BestForNavigation,
          timeInterval: 10,
          distanceInterval: 10
        }, (location) => {
          console.log(location);
          setStateRegion({ latitude: location.coords.latitude, longitude:location.coords.longitude,latitudeDelta: 0.00122, longitudeDelta: 0.00121 });
        })
      }catch(e)
      {
        setErr(e);
      }
    };
  
     useEffect( ()=>{
          TrackUserGPS();
      },[]);

    return(

        <View>
        
       <AutoCompleteSearchBar
        setRegionCallback={(name, lat, lon )=>{ setStateRegion({latitude:lat, longitude:lon, latitudeDelta: 0.00122, longitudeDelta: 0.00121 })}}
        />

        <MapComponent 
        setRegionCallback={(lat, lon )=>{ setStateRegion({latitude:lat, longitude:lon, latitudeDelta: 0.00122, longitudeDelta: 0.00121 })}}
        stateRegionProp = {stateRegion}
        />
      
        <TouchableOpacity
                    style = {styles.buttonStyle}
                    onPress={()=>{navigate()}}
                     >
                        {action == "dayAnalysis" ?<Text>set wanted day and weather</Text> :<Text>set wanted time and date</Text>}
         </TouchableOpacity>


         <TouchableOpacity
                    style = {styles.buttonStyle}
                    onPress={()=>{TrackUserGPS();}}
                     >
                        <Text>Locate location</Text>
         </TouchableOpacity>
         

         
 
        </View>
    )

};



const styles = StyleSheet.create({
    container: {
      backgroundColor: '#F5FCFF',
      flex: 1,
      paddingTop: 25,
    },
    autocompleteContainer: {
      flex: 1,
      left: 0,
      position: 'absolute',
      paddingTop: 20,
      right: 0,
      top: 0,
      zIndex: 1,
    },
    itemText: {
      fontSize: 15,
      margin: 2,
      fontWeight: 'bold',
    },
    map:{
      height:600,
      marginTop: 30,
    },
    buttonStyle: {
      alignItems: "center",
      backgroundColor: "#f794db",
      padding: 4,
      marginVertical: 1
  },
  
  });


export default GetInfoScreen;