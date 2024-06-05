import React, { Component } from 'react';
import { StyleSheet, View, ScrollView } from 'react-native';
import { Table, TableWrapper, Row } from 'react-native-table-component';


export default class ResultTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      tableHead: this.props.headers,
    }
  }
  render() {
    const state = this.state;
    // const widthArr = !!this.props.headers ? new Array(this.props.headers.length).fill(140) : [];
    let widthArr = [80];
    for(let i = 0; i < this.props.headers.length -1; i++){
        widthArr.push(140);
    }
    let tableData = [];
    for(let i = 0; i < this.props.data.length; i++){
        let row = [];

        row.push(this.props.data[i][this.state.tableHead[0]]);
        row.push(this.props.data[i][this.state.tableHead[1]]);
        row.push(this.props.data[i][this.state.tableHead[2]]);
        tableData.push(row);
    }
    
    console.log(tableData);
    return (
      <View style={styles.container}>
        <ScrollView horizontal={true} keyboardShouldPersistTaps='never'>
            <View>
            <Table borderStyle={{borderColor: '#C1C0B9'}}>
                <Row data={state.tableHead} widthArr={widthArr} style={styles.head} textStyle={styles.headerText}/>
            </Table>
            <ScrollView style={styles.dataWrapper}>
                <Table borderStyle={{borderColor: '#C1C0B9'}}>
                {
                    tableData.map((dataRow, index) => (
                    <Row
                        key={index}
                        data={dataRow}
                        widthArr={widthArr}
                        style={[styles.row, index%2 && {backgroundColor: '#ffffff'}]}
                        textStyle={styles.text}
                    />
                    ))
                }
                </Table>
            </ScrollView>
            </View>
        </ScrollView>
      </View>
    )
  }
}
const styles = StyleSheet.create({
  container: { 
    flex: 1, 
    padding: 16, 
    paddingTop: 30, 
    backgroundColor: '#ffffff' ,
    // width: '100%'
  },
  head: { 
    height: 50, 
    backgroundColor: '#6F7BD9' 
  },
  text: { 
    textAlign: 'center', 
    fontWeight: '200'
  },
  headerText: { 
    textAlign: 'center', 
    fontWeight: 'bold'
  },
  dataWrapper: { 
    marginTop: -1,
    // width: '100%'
  },
  row: { 
    height: 40, 
    backgroundColor: '#F7F8FA' 
  }
});