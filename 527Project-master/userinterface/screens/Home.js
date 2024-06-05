import React from 'react';
import { View, Text, TextInput, StyleSheet,ScrollView } from 'react-native';
import { RadioGroup } from 'react-native-radio-buttons-group';
import { Button } from 'react-native';
import { parseQuery } from '../api';
import ResultTable from './Table';

const databases = [
  {
    id: '1',
    label: 'MySQL',
    value: 'mysql'
  },
  {
    id: '2',
    label: 'Redshift',
    value: 'redshift'
  }
];

const schemas = [
  {
    id: '1',
    label: 'Instacart',
    value: 'instacart'
  },
  {
    id: '2',
    label: 'ABC_Retail',
    value: 'abcretail'
  }
];

const MultiTextInput = (props) => {
  return (
    <TextInput
      {...props}
      editable
      maxLength={1000}
    />
  );
}

const Home = ({ navigation }) => {
  const [query, onChangeQuery] = React.useState('');
  const [databaseSelected, setDatabase] = React.useState('');
  const [radioButtons, setRadioButtons] = React.useState(databases);
  const [selectedSchema, setSchema] = React.useState('');
  const [columns, setColumns] = React.useState(undefined);
  const [tableData, setTableData] = React.useState(undefined);
  const [showTable, setShowTable] = React.useState(false);
  const [timeToExecute, setTime] = React.useState('');

  function onPressRadioButton(radioButtonsArray){
    setRadioButtons(radioButtonsArray);
  }

  const executeQuery = () => {
    setShowTable(false);
    let databaseType = databaseSelected[0]['selected'] ? databaseSelected[0]['value']: databaseSelected[1]['value'];
    let schemaType = selectedSchema[0]['selected'] ? selectedSchema[0]['value']: selectedSchema[1]['value'];


    console.log("sdajdkls",schemaType);

    parseQuery(databaseType, schemaType, query).then((response) => {
      setColumns(response.data.columns);
      setTableData(response.data.results);
      setTime(response.data.time);
      setShowTable(true);
    });
  };

  
  return (
    <View style={styles.container} keyboardShouldPersistTaps='never'>
      <Text style={{paddingBottom:20, fontWeight: 'bold'}}>Enter Query in below text area:</Text>
      <View style={styles.body}>
        <View style={styles.radioGroup}>
          <Text>Please select the database: </Text>
          <View style={styles.radioBut}>
            <RadioGroup
              radioButtons={databases}
              onPress={(value) => setDatabase(value)}
              layout = {'row'}

            />
          </View>
        </View>
        <View>
          <Text>Please select the schema: </Text>
          <View style={styles.radioBut}>
            <RadioGroup
              radioButtons={schemas}
              onPress={(value) => setSchema(value)}
              layout = {'row'}

            />
          </View>
        </View>
        <View style={styles.textBox}  keyboardShouldPersistTaps='never'>
          <MultiTextInput
            multiline
            numberOfLines={10}
            placeholder={'select * from table;'}
            onChangeText = {(text) => onChangeQuery(text)}
            value={query}
            style={{padding:'2%', width: '98%', borderWidth:2}}
          />
        </View>
        <Button
          title='Execute'
          onPress={executeQuery}
        />
        </View>
      {showTable && <Text>Query executed in {timeToExecute}</Text>}
      {showTable && <ResultTable headers={columns} data={tableData}/>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  body:{
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start'
  },
  radioGroup:{
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-start',
  },
  radioBut:{
    alignItems: 'center',
    marginTop: 8,
    marginBottom: 16
  },
  scrollContainer:{
    minWidth: '100%'
  },
  tableHeader:{
    // width: '25%'
  },
});

export default Home;