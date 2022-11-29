import { List, Datagrid, TextField, EditButton, Edit, Create,SimpleForm, TextInput, ReferenceField, ReferenceInput, SelectInput} from "react-admin";

const filters = [
    <TextInput source="v0" label="V0_Search" alwaysOn />,
];

export const PolicyList = () => (
  <List filters={filters}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="ptype" />
      <ReferenceField source="v0" reference="roles">
        <TextField source="role_name" />
      </ReferenceField>
      <TextField source="v1" />
      <TextField source="v2" />
      {/* <TextField source="v3" />
      <TextField source="v4" />
      <TextField source="v5" /> */}
      <EditButton />
    </Datagrid>
  </List>
);

export const PolicyEdit = () => (
    <Edit>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="ptype"/>
        <ReferenceInput source="v0" reference="roles">
          <SelectInput optionText="role_name" />
        </ReferenceInput>
        <TextInput source="v1" />
        <TextInput source="v2" />
        {/* <TextInput source="v3" />
        <TextInput source="v4" />
        <TextInput source="v5" /> */}
        </SimpleForm>
    </Edit>
);

export const PolicyCreate = () => (
    <Create>
        <SimpleForm>
        <TextInput source="id" disabled />
        <TextInput source="ptype"/>
        <ReferenceInput source="v0" reference="roles">
          <SelectInput optionText="role_name" />
        </ReferenceInput>
        <TextInput source="v1" />
        <TextInput source="v2" />
        {/* <TextInput source="v3" />
        <TextInput source="v4" />
        <TextInput source="v5" /> */}
        </SimpleForm>
    </Create>
);