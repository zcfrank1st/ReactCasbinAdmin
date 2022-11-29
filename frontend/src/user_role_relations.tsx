import { List, Datagrid, TextField, ReferenceField, EditButton, Edit, Create,SimpleForm, TextInput, ReferenceInput, SelectInput} from "react-admin";

export const UserRoleRelationList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <ReferenceField source="user_id" reference="users">
        <TextField source="user_name" />
      </ReferenceField>
      <ReferenceField source="role_id" reference="roles">
        <TextField source="role_name" />
      </ReferenceField>
      <EditButton />
    </Datagrid>
  </List>
);

export const UserRoleRelationEdit = () => (
    <Edit>
        <SimpleForm>
        <TextInput source="id" disabled />
        <ReferenceInput source="user_id" reference="users">
          <SelectInput optionText="user_name" />
        </ReferenceInput>
        <ReferenceInput source="role_id" reference="roles">
        <SelectInput optionText="role_name" />
        </ReferenceInput>
        </SimpleForm>
    </Edit>
);

export const UserRoleRelationCreate = () => (
    <Create>
        <SimpleForm>
        <TextInput source="id" disabled />
        <ReferenceInput source="user_id" reference="users">
          <SelectInput optionText="user_name" />
        </ReferenceInput>
        <ReferenceInput source="role_id" reference="roles">
        <SelectInput optionText="role_name" />
        </ReferenceInput>
        </SimpleForm>
    </Create>
);