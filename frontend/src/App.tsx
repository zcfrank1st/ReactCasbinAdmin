import {Admin, Resource, ListGuesser} from "react-admin"
import simpleRestProvider from "ra-data-simple-rest"

const App = () => (
  <Admin dataProvider={simpleRestProvider('http://127.0.0.1:8000')}>
    <Resource name="policies" list={ListGuesser}/>
  </Admin>
);


export default App;