
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import MapView, { Marker } from 'react-native-maps';





const MapComponent = (props) => {

    

    return(

        <View>
                <MapView 
                 style={styles.map}
                 region={props.stateRegionProp}
                 >
                <Marker 
                draggable
                coordinate = {props.stateRegionProp}
                onDragEnd= { (e)=> { props.setRegionCallback(e.nativeEvent.coordinate.latitude , e.nativeEvent.coordinate.longitude)}}

                >
                </Marker>
                <Text></Text>
                </MapView>
        </View>   
    )
};



const styles = StyleSheet.create({
    map:{
      height:600,
      marginTop: 30,
    }
  });


export default MapComponent;