import { List, Datagrid, TextField, EditButton, Edit, Create,SimpleForm, TextInput} from "react-admin";

const filters = [
    <TextInput source="user_name" label="UserName_Search" alwaysOn />,
];

export const UserList = () => (
  <List filters={filters}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="user_name" />
      <TextField source="password" />
      <EditButton />
    </Datagrid>
  </List>
);

export const UserEdit = () => (
    <Edit>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="user_name"/>
        <TextInput source="password" />
        </SimpleForm>
    </Edit>
);

export const UserCreate = () => (
    <Create>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="user_name"/>
        <TextInput source="password" />
        </SimpleForm>
    </Create>
);