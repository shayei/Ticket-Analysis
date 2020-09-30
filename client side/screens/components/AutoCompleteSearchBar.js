
import Autocomplete from 'react-native-autocomplete-input';
import React, { useState} from 'react';
import { StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import TomTom from '../../api/TomTom';




const AutoCompleteSearchBar = (props)=>{

    const [results, setResults] = useState([]);
    const[placeQuery, setPlaceQuery] = useState('');



    const onPressFN = (name,lat,lon) =>{
        setResults([]);
        setPlaceQuery(name);
        props.setRegionCallback(name,lat,lon);

    }



    const searchApi = async (i_Query) => {
        try{
        let apiURL = '/'+ i_Query +'.json?key=O39cJUgKuUE0js4ARn11GJ2ZhHQYiyu6&typeahead=true&limit=10&countrySet=IL';
        let places = [];
        const response = await TomTom.get(apiURL);
        setResults(response);
        let arr = response.data.results;
        let obj = arr.address;
        
        let appiresult= [];
        for( let i=0 ; i<arr.length; i++)
        {
            appiresult.push({
                name: arr[i].address.freeformAddress,
                address:arr[i].address.freeformAddress,
                lat:arr[i].position.lat,
                lon:arr[i].position.lon,
            });
        }
        setResults(appiresult);
    }catch(err){
        console.log("error");
    }

        
    };


    return (
        <View>
          <Autocomplete
          containerStyle={styles.autocompleteContainer}
          placeholder="Enter place name"
            data={results}
            defaultValue={placeQuery}
            onChangeText={text => searchApi(text)}
            renderItem={(obj) => (
              <TouchableOpacity onPress={() => onPressFN(obj.item.name, obj.item.lat, obj.item.lon)}>
                <Text style={styles.itemText}>{obj.item.name}</Text>
              </TouchableOpacity>
            )}
          />
  
  
        </View>      
        )

       
  
    




};




const styles = StyleSheet.create({
   
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
    }
  });



  export default AutoCompleteSearchBar;