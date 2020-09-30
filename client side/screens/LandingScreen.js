import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View} from 'react-native';




const LandingScreen = (props) => {

    



        return(
            <View style={styles.containerStyle}>
                <Text style = {styles.inc}>Incopyright 2020</Text>
                
                
                <TouchableOpacity
                    style = {styles.buttonStyle}

                    onPress={()=>{props.navigation.navigate('GetInfo', {id: 'getInfo'})}} 
                   
                     >

                        <Text>Get Ticket Information</Text>
                     </TouchableOpacity>

                     
                <TouchableOpacity
                    style = {styles.buttonStyle}
                    onPress={()=>{props.navigation.navigate('GetInfo', {id: 'postInfo'})}}
                     >

                        <Text>Post Ticket Information</Text>
                     </TouchableOpacity>


                     
                <TouchableOpacity
                    style = {styles.buttonStyle}
                    onPress = {()=>{props.navigation.navigate('GetInfo', {id: 'dayAnalysis'})}}
                     >

                        <Text>Show Ticket Analysis</Text>
                     </TouchableOpacity>

                
            </View>
        )

    

};



const styles = StyleSheet.create({
  
        buttonStyle: {
            alignItems: "center",
            //backgroundColor: "#f794db",
            backgroundColor: "#BE8989",
            padding: 10,
            marginVertical: 40
        },
        
        containerStyle:{
            //backgroundColor: "#DDDDDD",
            backgroundColor: '#61dafb',
            flex: 1,
        },
        inc:{
            alignSelf: 'flex-start',
        }
  });


export default LandingScreen;