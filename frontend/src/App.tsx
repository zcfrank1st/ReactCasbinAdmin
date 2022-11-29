import {Admin, Resource, EditGuesser } from "react-admin"
import simpleRestProvider from "ra-data-simple-rest"
import { PolicyList, PolicyEdit, PolicyCreate } from "./policies";
import { UserList, UserEdit, UserCreate } from "./users";
import { RoleList, RoleEdit, RoleCreate } from "./roles";
import { UserRoleRelationList, UserRoleRelationEdit, UserRoleRelationCreate } from "./user_role_relations";
import { Dashboard } from './dashboard';

import PolicyIcon from '@mui/icons-material/Policy';
import PersonIcon from '@mui/icons-material/Person';
import SupervisedUserCircleIcon from '@mui/icons-material/SupervisedUserCircle';
import CommitIcon from '@mui/icons-material/Commit';

const App = () => (
  <Admin dataProvider={simpleRestProvider(import.meta.env.VITE_URL)} dashboard={Dashboard}>
    <Resource name="policies" list={PolicyList} edit={PolicyEdit} create={PolicyCreate} icon={PolicyIcon}/>
    <Resource name="users" list={UserList} edit={UserEdit} create={UserCreate} icon={PersonIcon}/>
    <Resource name="roles" list={RoleList} edit={RoleEdit} create={RoleCreate} icon={SupervisedUserCircleIcon}/>
    <Resource name="user_role_relations" list={UserRoleRelationList} edit={UserRoleRelationEdit} create={UserRoleRelationCreate} icon={CommitIcon}/>
  </Admin>
);


export default App;