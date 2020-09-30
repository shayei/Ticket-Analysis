import React, { useState} from 'react';
import { StyleSheet, Text, TouchableOpacity, View, Button, Linking} from 'react-native';
import DateTimePickerModal from "react-native-modal-datetime-picker";
import TicketAnalysis from '../api/TicketAnalysis';




const ReporterScreen = (props) => {

    const dateTimeObject = new Date();
    const current_date = dateTimeObject.toISOString().slice(0, dateTimeObject.toISOString().indexOf("T"));
    const current_time = dateTimeObject.toLocaleTimeString().slice(0,5);
    const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
    const [chosenStartingTime, setStartingTime] = useState(current_time);
    const [choseStartingnDate, setStartingtDate] = useState(current_date);
    const [chosenEndingTime, setEndingTime] = useState(current_time);
    const [choseEndingnDate, setEndingDate] = useState(current_date);
    const [isStartingInfoChoosen, setStartingOption] = useState(false);
    const [response, setResponse] = useState({received_information:{status_code:'',text_response:'',percent:-1}, supplied_information:{request_route:'',supplied_params:{latitude:'',longitude:'',date:'',start_time:'',end_time:''}}});
    const [ isPercentDisplayed, setIsPercentDisplayed] = useState(false);
    const [ showOtherResults, setShowOtherResults] = useState(false);

    /*style props */
    const buttonStyle={marginTop:20, borderBottomWidth:1, marginTop:40};
    const error_Message_style = {marginTop: 120,fontSize: 20,fontWeight: "bold",borderBottomWidth: 1,borderTopWidth:1,padding:10};
    const  text_time_style = {marginTop: 20,borderWidth: 2,color:'#BE8989'};
    /*style props */

    /*routing and action variables */
    const gta_route = "/gta";
    const sdl_route = "/sdl";
    const report_route ="/report";
    const get_info_action = 'getInfo';
    const post_info_action = 'psotInfo';
    /*routing and action variables */


    /*parameters passed from GetInfoScreen */
    let lon_fromScreen = props.navigation.getParam('longitude',{});
    let lat_fromScreen = props.navigation.getParam('latitude',{});
    let action = props.navigation.getParam('action',{});
    /*parameters passed from GetInfoScreen */

    
    let requestInfo = {};
    let postInfo = {};
    let buttoToDisplay = '';




    if(action == get_info_action)
    {
      if(response.supplied_information.request_route == '/gta' ||response.supplied_information.request_route == '' || showOtherResults == false)
      {
        buttoToDisplay ="Get Ticket Anylysis information";
      }
      else
      {
        buttoToDisplay = "null";
      }
    }
    else
    {
      buttoToDisplay = "Post Ticket Anylysis information";
    }

    const setRequestInfo = (i_Route)=>{
      const display = true;
      if (i_Route == "gta")
      { 
        requestInfo = {latitude:lat_fromScreen , longitude:lon_fromScreen , date: choseStartingnDate , start_time: chosenStartingTime  , end_time : chosenEndingTime};
      }
      else
      {
        requestInfo = {latitude: response.supplied_information.supplied_params.latitude , longitude: response.supplied_information.supplied_params.longitude   , date: response.supplied_information.supplied_params.date , start_time: response.supplied_information.supplied_params.start_time  , end_time : response.supplied_information.supplied_params.end_time, current_location_result:response.received_information.percent };
        
      }

      getTicketAnalysis(i_Route);
      setIsPercentDisplayed(display);

    };

    const setPostInfo = () => {
      postInfo = {latitude:lat_fromScreen , longitude:lon_fromScreen , date: choseStartingnDate , time: chosenStartingTime};
      postTicketAnalysis();
    }
  
    const postTicketAnalysis = async () => {

      try{
      const post_response = await TicketAnalysis.post('/report', postInfo);
      const temporary_response = `server description:\n ${post_response.data.received_information.text_response}\n\n server response: ${post_response.data.response}`;
      setResponse(post_response.data);
      }catch(err){

        const err_message = {received_information:{status_code:'404 Bad',text_response:'network error occured',percent:-1}, supplied_information:{request_route:'/sdl',supplied_params:{latitude:'',longitude:'',date:'',start_time:'',end_time:''}}};
        setResponse(err_message);
      }
    }

    const getTicketAnalysis = async (i_Route)=>{
     const showOtherResultsButton = true;


      try{

      const get_response = await  TicketAnalysis.get(`/${i_Route}`, {params: requestInfo});
      setResponse(get_response.data);
      setShowOtherResults(showOtherResultsButton);
      }catch(err){

        const err_message = {received_information:{status_code:'404 Bad',text_response:'network error occured',percent:-1}, supplied_information:{request_route:'/gta',supplied_params:{latitude:'',longitude:'',date:'',start_time:'',end_time:''}}};
        
        setResponse(err_message);
      }

    };

    const openWaze = ()=>{

      const url = "https://waze.com/ul?q=66%20Acacia%20Avenue&ll=" +response.received_information.location.latitude + ","+response.received_information.location.longitude+"&navigate=yes";
      console.log(url);
      Linking.openURL(url);
    };


    const showDatePicker = () => {
      const value = true;
        setDatePickerVisibility(value);
      };
     
      const hideDatePicker = () => {
        const showOtherResultsButton = false;
        setDatePickerVisibility(false);
        setShowOtherResults(showOtherResultsButton);
      };
     
      const handleConfirm = (date) => {
    
        hideDatePicker();
        if (isStartingInfoChoosen)
        {
          let option =false;
          setStartingTime(`${date.toLocaleTimeString().slice(0,5)}`);
          setStartingtDate( date.toISOString().slice(0, date.toISOString().indexOf("T")));
          setStartingOption(option);
        }
        if(!isStartingInfoChoosen){
          setEndingTime( `${date.toLocaleTimeString().slice(0,5)}`);
          setEndingDate(date.toISOString().slice(0, date.toISOString().indexOf("T")));
          
        }
      };



      const activateTimePicker = () =>{
        showDatePicker();
  
      }

        return(
            <View>
                <Text >heyy inside TestValue</Text>
                <TouchableOpacity
                    onPress={()=>{setStartingOption(true);showDatePicker();}}
                      style={buttonStyle}
                     >
                       {action == get_info_action ? <Text>Please click here to choose Starting parking Time and Date</Text> : <Text>Please click here to choose ticket time and date</Text>}
                </TouchableOpacity>

                   <Text style = {text_time_style}> choosen time is: {chosenStartingTime}, chosen date is: {choseStartingnDate}</Text>

                <TouchableOpacity
                    onPress={()=>{showDatePicker();}}
                    style ={action == get_info_action ? buttonStyle: null}
                     >
                        {action == get_info_action ? <Text>Please click here to choose Ending parking Time and Date</Text> : null}
                </TouchableOpacity>

                      {action == get_info_action ?  <Text style= {text_time_style}> choosen time is: {chosenEndingTime}, chosen date is: {choseEndingnDate}</Text> : null}

               <TouchableOpacity
                    onPress={()=>{ action == get_info_action ? setRequestInfo("gta"): setPostInfo();}}
                    style = {buttonStyle}
                     >
                      {buttoToDisplay != "null" && !showOtherResults ? <Text>{buttoToDisplay} </Text>  : null}
                </TouchableOpacity>

               

                <DateTimePickerModal
                isVisible={isDatePickerVisible}
                mode="datetime"
                onConfirm={handleConfirm}
                onCancel={hideDatePicker}
                />

                
                {response.supplied_information.request_route == gta_route || response.supplied_information.request_route == report_route  ? <Text style = {error_Message_style}>{response.received_information.text_response}</Text> : null}

                <TouchableOpacity
                    onPress={()=>{ action == get_info_action ? setRequestInfo("sdl"): null;}}
                    style = {buttonStyle}
                     >
                        {action == get_info_action && showOtherResults && response.supplied_information.request_route != sdl_route && response.received_information.status_code == "200 OK"  ? <Text>Click here to get other nearby location to park</Text> : null}
                </TouchableOpacity>

                {response.supplied_information.request_route == sdl_route && showOtherResults ? <Text style = {error_Message_style}>{response.received_information.text_response}</Text> : null}


                {response.supplied_information.request_route == sdl_route && showOtherResults && response.received_information.status_code =="200 OK" ? 
                                                                                                                                                    <Button
                                                                                                                                                      title="open location in waze"
                                                                                                                                                      onPress={()=>{openWaze()}}
                                                                                                                                                    /> : null}
                

        
            </View>
        );

    

};




styles = StyleSheet.create({
  button:{
    marginTop: 20,
    borderBottomWidth:1,
    marginTop:40,
  },

  error_Message :{
    marginTop: 120,
    fontSize: 20,
    fontWeight: "bold",
    borderBottomWidth: 1,
    borderTopWidth:1,
    padding:10,
  },
  text_time_style:{
    marginTop: 20,
    borderWidth: 2,
    color:'#BE8989',
  },
});

export default ReporterScreen;