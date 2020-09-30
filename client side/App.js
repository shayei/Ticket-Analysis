import {createStackNavigator} from 'react-navigation-stack';
import {createAppContainer} from 'react-navigation';
import GetInfoScreen from './src/screens/GetInfoScreen';
import LandingScreen from './src/screens/LandingScreen';
import ReporterScreen from './src/screens/ReporterScreen';
import TicketDayAnalysis from './src/screens/TicketDayAnalysis';
import DisplayTicketDayAnalysis from './src/screens/DisplayTicketDayAnalysis';

const naivgator= createStackNavigator({
GetInfo:GetInfoScreen,
landing:LandingScreen,  
reporter: ReporterScreen,
DayAnlysis:TicketDayAnalysis,
DisplayAnalysis:DisplayTicketDayAnalysis,

},{
  initialRouteName: 'landing',
  defaultNavigationOptions:{
    title:'Ticket Analysis'
  }
}
);

export default createAppContainer(naivgator);

