import {Admin, Resource, EditGuesser } from "react-admin"
import simpleRestProvider from "ra-data-simple-rest"
import { PolicyList, PolicyEdit, PolicyCreate } from "./policies";
import { Dashboard } from './dashboard';

import PolicyIcon from '@mui/icons-material/Policy';

const App = () => (
  <Admin dataProvider={simpleRestProvider(import.meta.env.VITE_URL)} dashboard={Dashboard}>
    <Resource name="policies" list={PolicyList} edit={PolicyEdit} create={PolicyCreate} icon={PolicyIcon}/>
  </Admin>
);


export default App;