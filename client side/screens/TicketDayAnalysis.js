import React, { useState} from 'react';
import { StyleSheet, Text, TouchableOpacity, View, FlatList, Button } from 'react-native';
import DateTimePickerModal from "react-native-modal-datetime-picker";



 /*style props */
 const date_Option_style ={margin: 20,borderWidth:1,padding:10,backgroundColor:'#456ba8'};
 const text_style= {fontWeight: "bold"};
 const item_style = {padding: 10,marginVertical: 8,marginHorizontal: 16,width: 150,height: 50,};
 const title_style=  {fontSize: 16};
 const view_style={width: 400,height: 550,flexDirection: 'column',justifyContent: 'center',alignItems: 'flex-start',backgroundColor:'#456bb8'};
 const text_Info_style = {position:"absolute",top:40,right:0,bottom:0,left:200};
 const duration_style={position:"absolute",left:200,top:40,height:500,backgroundColor:'#546aa8'};
/*style props */





const Item = ({ item, onPress, style }) => (
                 
                 <TouchableOpacity onPress={onPress} style={[item_style, style]}>
                    <Text style={title_style}>{item.title}</Text>
                </TouchableOpacity>
  );




const TicketDayAnalysis = (props)=>{
    
    const dateTimeObject = new Date();
    const current_date = dateTimeObject.toISOString().slice(0, dateTimeObject.toISOString().indexOf("T"));
    const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
    const [wantedDate, setWantedDate] = useState(current_date);
    const [selectedId, setSelectedId] = useState("3ac68afc-c605-48d3-a4f8-fbd91aa97f63");
    const [selectedWeather,SetSelectedWeather] = useState("Sunny");
    const [selecteDuration,SetSelectedDuratoin] = useState("ONE_WEEK");
    const choosenLongitude = props.navigation.getParam('longitude',{});
    const choosenLatitude = props.navigation.getParam('latitude',{});
    const [selectedDuarationId, setSelecteDurationId] = useState("1");
    
   



    const weatherOptions = [
        {
          id: "bd7acbea-c1b1-46c2-aed5-3ad53abb28ba",
          title: "Heat wave",
        },
        {
          id: "3ac68afc-c605-48d3-a4f8-fbd91aa97f63",
          title: "Sunny",
        },
        {
          id: "58694a0f-3da1-471f-bd96-145571e29d72",
          title: "Cloudy",
        },{
            id: "bd7acbea-c1b1-46c2-aed5-3ad53abb28bb",
            title: "Rainy",
          },
          {
            id: "3ac68afc-c605-48d3-a4f8-fbd91aa97f64",
            title: "Stormy",
          },
          {
            id: "58694a0f-3da1-471f-bd96-145571e29d73",
            title: "Windy",
          },
      ];

      const durationOptions = [
        {
          id: "1",
          title: "ONE_WEEK",
        },
        {
          id: "2",
          title: "TWO_WEEKS",
        },
        {
          id: "3",
          title: "THREE_WEEKS",
        },{
            id: "4",
            title: "ONE_MONTH",
          },
          {
            id: "8",
            title: "TWO_MONTH",
          },
          {
            id: "12",
            title: "THREE_MONTH",
          },
          {
            id: "26",
            title: "HALF_YEAR",
          },
          {
            id: "52",
            title: "ONE_YEAR",
          },
      ];





    

    const showDatePicker = () => {
        const value = true;

        setDatePickerVisibility(value);
        };
       
        const hideDatePicker = () => {
          const showOtherResultsButton = false;
         
          setDatePickerVisibility(false);
        };
       
        const handleConfirm = (date) => {
      
          hideDatePicker();
          setWantedDate(date.toISOString().slice(0, date.toISOString().indexOf("T")));
         
        };

        const renderWeather = ({ item }) => {
            const backgroundColor = item.id === selectedId ? "#6e3b6e" : "#f9c2ff";
            const result = weatherOptions.filter(item => item.id == selectedId);

            SetSelectedWeather(result[0].title);
            return (
              <Item
                item={item}
                onPress={() => setSelectedId(item.id)}
                style={{ backgroundColor }}
              />
            );
          };


        const renderDuration = ({ item }) => {
            const backgroundColor = item.id === selectedDuarationId ? "#6e3b6e" : "#f9c2ff";
            const result = durationOptions.filter(item => item.id == selectedDuarationId);

            SetSelectedDuratoin(result[0].title);
            return (
              <Item
                item={item}
                onPress={() => setSelecteDurationId(item.id)}
                style={{ backgroundColor }}
              />
            );
          };



    
          

    return(

        <View style={{backgroundColor:"#8b8bbb",height:700}}>

                <TouchableOpacity onPress={()=>{showDatePicker() }} style = {date_Option_style}>

                      <Text style = {text_style}>please click here to choose the the wanted day</Text>
                    
                </TouchableOpacity>


                <Text style ={{position:"absolute",left:0, top:65}}  >choosen date is {wantedDate}</Text>
           
                  <TouchableOpacity
                    onPress={()=>{}}
                    >
                      <Text style = {{fontWeight: "bold",top:4}}>please choose one of the following weather and duration options:</Text>
                    
                  </TouchableOpacity>

                  
                  <View   style={{height:400, width:150,position:"absolute",left:0, top:130}}>

                        <FlatList
                        data={weatherOptions}
                        renderItem={renderWeather}
                        keyExtractor={(item) => item.id}
                        extraData={selectedId}
                    />

                  </View>
 
                  <View style={{height:520, width:350,position:"absolute",left:200, top:130}}>
                          <FlatList
                            data={durationOptions}
                            renderItem={renderDuration}
                            keyExtractor={(item) => item.id}
                            extraData={selectedDuarationId}
                          />
                  </View>
 

                  
                  <View style={{top:550}}>

                      <Button 
                        onPress={()=>{props.navigation.navigate('DisplayAnalysis', {wantedDate:wantedDate,id: selectedWeather,longitude:choosenLongitude,latitude:choosenLatitude,duration:selectedDuarationId})}}
                        title="Request Ticket day analysis"
                        color="#841584"
                        />
                      </View> 


        
            <DateTimePickerModal
                isVisible={isDatePickerVisible}
                mode="date"
                onConfirm={handleConfirm}
                onCancel={hideDatePicker}
                />


        </View>


    );

};




styles = StyleSheet.create({

    dateOption:{
        margin: 20,
        borderWidth:1,
        padding:10,
        backgroundColor:'#456ba8',
    },
    textStyle:{

        fontWeight: "bold"
    },
    item: {
        padding: 10,
        marginVertical: 8,
        marginHorizontal: 16,
        width: 150,
        height: 50,

      },
      title: {
        fontSize: 16,
      },
      viewStyle:{
        width: 400,
        height: 550,
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'flex-start',
        backgroundColor:'#456bb8',
        
      },
      textInfo:{
        position:"absolute",
        top:40,
        right:0,
        bottom:0,
        left:200,

      },
});




export default TicketDayAnalysis;