import React, { useEffect, useState } from 'react';
import { View,Text, StyleSheet } from "react-native";
import TicketAnalysis from '../api/TicketAnalysis';
import PureChart from 'react-native-pure-chart';


const DisplayTicketDayAnalysis = (props) =>{

    const weather = props.navigation.getParam('id',{});
    const date = props.navigation.getParam('wantedDate',{});
    const longitude = props.navigation.getParam('longitude',{});
    const latitude = props.navigation.getParam('latitude',{});
    const duration = props.navigation.getParam('duration',{});
    const [error,setError]= useState(false);

    const requestInfo = {weather: weather,duration:duration, longitude: longitude,latitude: latitude, date:date};
    

    const [sampleData,setSampleData] = useState( [
        {
          seriesName: 'series1',
          data: [
            {x: '08:00 - 09:00', y: 0},
            {x: '09:00 - 10:00', y: 0},
            {x: '10:00 - 11:00', y: 0},
            {x: '11:00 - 12:00 ', y:0},
            {x: '12:00 - 13:00', y: 0},
            {x: '13:00 - 14:00', y: 0},
            {x: '14:00 - 15:00', y: 0},
            {x: '15:00 - 16:00', y: 0},
            {x: '16:00 - 17:00', y: 0},
            {x: '17:00 - 18:00', y: 0},
            {x: '18:00 - 19:00', y: 0},
            {x: '19:00 - 20:00', y: 0},
            {x: '20:00 - 21:00', y: 0},
            {x: '21:00 - 22:00', y: 0},
            {x: '22:00 - 23:00', y: 0},
            {x: '23:00 - 00:00', y: 0},
            {x: 'end', y: -1},
    
            
            
          ],
          color: '#297AB1'
        },
     
      ])

      
        

    const getTicketAnalysis = async (i_Route)=>{
       let analysis_error = false;
         try{
         const get_response = await  TicketAnalysis.get(`/${i_Route}`, {params: requestInfo});

      
        if(get_response.data.received_information.status_code != "404")
        {
        let responseData = [
          {
            seriesName: 'series1',
            data: [
              {x: '08:00 - 09:00', y: Number(get_response.data.received_information.calculation.Eight)},
              {x: '09:00 - 10:00', y: Number(get_response.data.received_information.calculation.Nine)},
              {x: '10:00 - 11:00', y: Number(get_response.data.received_information.calculation.Ten)},
              {x: '11:00 - 12:00 ', y: Number(get_response.data.received_information.calculation.Eleven)},
              {x: '12:00 - 13:00', y: Number(get_response.data.received_information.calculation.Twelve)},
              {x: '13:00 - 14:00', y: Number(get_response.data.received_information.calculation.Thirteen)},
              {x: '14:00 - 15:00', y: Number(get_response.data.received_information.calculation.Fourteen)},
              {x: '15:00 - 16:00', y: Number(get_response.data.received_information.calculation.Fifteen)},
              {x: '16:00 - 17:00', y: Number(get_response.data.received_information.calculation.Sixteen)},
              {x: '17:00 - 18:00', y: Number(get_response.data.received_information.calculation.Seventeen)},
              {x: '18:00 - 19:00', y: Number(get_response.data.received_information.calculation.Eighteen)},
              {x: '19:00 - 20:00', y: Number(get_response.data.received_information.calculation.Nineteen)},
              {x: '20:00 - 21:00', y: Number(get_response.data.received_information.calculation.Twenty)},
              {x: '21:00 - 22:00', y: Number(get_response.data.received_information.calculation.Twenty_one)},
              {x: '22:00 - 23:00', y: Number(get_response.data.received_information.calculation.Twenty_two)},
              {x: '23:00 - 00:00', y: Number(get_response.data.received_information.calculation.Twenty_three)},
              {x: 'end', y: -1},
      
              
              
            ],
            color: '#297AB1'
          },
       
        ]
      
        setSampleData(responseData);
        setError(analysis_error);
      }
         }catch(err){
          analysis_error = true;
          setError(analysis_error);
   
         }
   
       };

       useEffect(()=>{getTicketAnalysis("graph")},[]);

    return(

        <View style={{backgroundColor:"#99bbff",height:800}}>

        <Text> Reported tickets for the last {duration} weeks</Text>
         {error == false ? <View    style={{top:80}}>
            <Text>{weather}</Text>
            <PureChart data={sampleData}
             type='bar'
             width={'400%'}
             height={400} />
          </View>
          :<Text>a network error occured</Text>}

        </View>

    );




};

const styles = StyleSheet.create({});

export default DisplayTicketDayAnalysis;


