import { List, Datagrid, TextField, EditButton, Edit, Create,SimpleForm, TextInput} from "react-admin";

const filters = [
    <TextInput source="role_name" label="RoleName_Search" alwaysOn />,
];

export const RoleList = () => (
  <List filters={filters}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="role_name" />
      <EditButton />
    </Datagrid>
  </List>
);

export const RoleEdit = () => (
    <Edit>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="role_name"/>
        </SimpleForm>
    </Edit>
);

export const RoleCreate = () => (
    <Create>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="role_name"/>
        </SimpleForm>
    </Create>
);