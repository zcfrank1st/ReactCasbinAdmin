import { List, Datagrid, TextField, EditButton, Edit, Create,SimpleForm, TextInput} from "react-admin";

export const UserRoleRelationList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="user_id" />
      <TextField source="role_id" />
      <EditButton />
    </Datagrid>
  </List>
);

export const UserRoleRelationEdit = () => (
    <Edit>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="user_id" />
        <TextInput source="role_id" />
        </SimpleForm>
    </Edit>
);

export const UserRoleRelationCreate = () => (
    <Create>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="user_id" />
        <TextInput source="role_id" />
        </SimpleForm>
    </Create>
);