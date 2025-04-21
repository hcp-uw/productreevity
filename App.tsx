import React from 'react';
import { View, ScrollView } from 'react-native';
import Page1 from './Page1';
import Page2 from './Page2';
import Page3 from './Page3';

const App = () => {
  return (
    <ScrollView contentContainerStyle={{ padding: 20 }}>
      <Page1 />
      <Page2 />
      <Page3 />
    </ScrollView>
  );
};

export default App;
