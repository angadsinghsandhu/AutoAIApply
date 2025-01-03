# Notion API Reference: Databases

## Table of contents

- [Notion API Reference: Databases](#notion-api-reference-databases)
  - [Table of contents](#table-of-contents)
  - [Database object](#database-object)
    - [All Databases](#all-databases)
    - [Created by](#created-by)
    - [Created time](#created-time)
    - [Date](#date)
    - [Email](#email)
    - [Files](#files)
    - [Formula](#formula)
    - [Last edited by](#last-edited-by)
    - [Last edited time](#last-edited-time)
    - [Multi-select](#multi-select)
    - [Number](#number)
    - [People](#people)
    - [Phone number](#phone-number)
    - [Relation](#relation)
    - [Rich text](#rich-text)
    - [Rollup](#rollup)
    - [Select](#select)
    - [Status](#status)
    - [Title](#title)
    - [URL](#url)
  - [Working with databases](#working-with-databases)
    - [Overview](#overview)
    - [Additional types of databases](#additional-types-of-databases)
      - [Linked databases](#linked-databases)
      - [Wiki databases](#wiki-databases)
    - [Structure](#structure)
    - [Database properties example](#database-properties-example)
    - [Iterate over a database object](#iterate-over-a-database-object)
    - [Adding pages to a database](#adding-pages-to-a-database)
    - [Finding pages in a database](#finding-pages-in-a-database)
      - [Filtering database pages](#filtering-database-pages)
      - [Sorting database pages](#sorting-database-pages)
    - [Conclusion](#conclusion)
    - [Next steps](#next-steps)

---

## Database object

Database objects describe the **property schema** of a database in Notion. Pages are the items (or children) in a database. Page property values must conform to the property objects laid out in the parent database object.

### All Databases

> **Note:**  
> Properties marked with an * are accessible to integrations with any capabilities. Other properties require **read content** capabilities to be retrieved via the Notion API. For more details on integration capabilities, refer to the [Capabilities Guide](https://developers.notion.com/docs/editor-capabilities).

| **Field**           | **Type**                                 | **Description**                                                                                                                                     | **Example Value**                                                                                                                       |
|---------------------|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **object***         | `string`                                 | Always `"database"`.                                                                                                                                  | `"database"`                                                                                                                            |
| **id***             | `string` (UUID)                          | Unique identifier for the database.                                                                                                                  | `"2f26ee68-df30-4251-aad4-8ddc420cba3d"`                                                                                                |
| **created_time**    | `string` (ISO 8601)                      | Timestamp when the database was created, formatted as an ISO 8601 string.                                                                         | `"2020-03-17T19:10:04.968Z"`                                                                                                           |
| **created_by**      | [Partial User](https://developers.notion.com/reference/user) | User who created the database.                                                                                                                        | `{"object": "user","id": "45ee8d13-687b-47ce-a5ca-6e2e45548c4b"}`                                                                     |
| **last_edited_time**| `string` (ISO 8601)                      | Timestamp when the database was last updated, formatted as an ISO 8601 string.                                                                     | `"2020-03-17T21:49:37.913Z"`                                                                                                           |
| **last_edited_by**  | [Partial User](https://developers.notion.com/reference/user) | User who last edited the database.                                                                                                                     | `{"object": "user","id": "45ee8d13-687b-47ce-a5ca-6e2e45548c4b"}`                                                                     |
| **title**           | Array of [Rich Text Objects](https://developers.notion.com/reference/rich-text) | Name of the database as displayed in Notion.                                                                                                         | ```json
"title": [
  {
    "type": "text",
    "text": {
      "content": "Can I create a URL property",
      "link": null
    },
    "annotations": {
      "bold": false,
      "italic": false,
      "strikethrough": false,
      "underline": false,
      "code": false,
      "color": "default"
    },
    "plain_text": "Can I create a URL property",
    "href": null
  }
]
``` |
| **description**     | Array of [Rich Text Objects](https://developers.notion.com/reference/rich-text) | Description of the database as shown in Notion.                                                                                                     | *(Same structure as title, omitted for brevity.)*                                                                                       |
| **icon**            | `File Object` or `Emoji Object`          | Icon representing the page.                                                                                                                           | *(Either a file object or an emoji object.)*                                                                                             |
| **cover**           | `File Object` (`external` type)          | Cover image for the page.                                                                                                                             | *(File object details.)*                                                                                                                 |
| **properties***     | `object`                                 | Schema defining the database properties. Each key is a property name, and the value is the property object.                                           | ```json
"properties": {
  "Property Name": {
    "id": "some-id",
    "type": "rich_text",
    "rich_text": {}
  },
  ...
}
``` |
| **parent**          | `object`                                 | Information about the database's parent.                                                                                                             | `{ "type": "page_id", "page_id": "af5f89b5-a8ff-4c56-a5e8-69797d11b9f8" }`                                                           |
| **url**             | `string`                                 | URL of the Notion database.                                                                                                                           | `"https://www.notion.so/668d797c76fa49349b05ad288df2d136"`                                                                               |
| **archived**        | `boolean`                                | Indicates if the database is archived.                                                                                                                | `false`                                                                                                                                 |
| **in_trash**        | `boolean`                                | Indicates if the database has been deleted.                                                                                                           | `false`                                                                                                                                 |
| **is_inline**       | `boolean`                                | `true` if the database is displayed inline on a page; `false` if it's a child page.                                                                 | `false`                                                                                                                                 |
| **public_url**      | `string` or `null`                       | Public URL of the page if published to the web; otherwise, `null`.                                                                                   | `"https://jm-testing.notion.site/p1-6df2c07bfc6b4c46815ad205d132e22d"`                                                                    |

> **Note:**  
> **Maximum Schema Size Recommendation**  
> Notion recommends keeping the database schema size under 50KB. Larger schemas may be blocked to ensure optimal database performance.

---

## Database Properties

Database **property objects** represent the columns in the Notion UI. Each database includes a `properties` object containing individual **database property objects**, which define the schema.

> **Note:**  
> **Database Rows**  
> To work with database rows via the API, refer to the [Page Property Values Documentation](https://developers.notion.com/docs/page-property-values). The API treats database rows as pages.

Every **database property object** includes the following fields:

| **Field**   | **Type**          | **Description**                                                                                                                                                                    | **Example Value**          |
|-------------|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| `id`        | `string`          | Unique identifier for the property, typically a short string of random characters. Some property types have predefined IDs, such as `"title"` for Title properties.                      | `"fy:{"`                   |
| `name`      | `string`          | Name of the property as displayed in Notion.                                                                                                                                      | `"Task complete"`          |
| `description`| `string`         | Description of the property as shown in Notion.                                                                                                                                   | *(Optional)*               |
| `type`      | `string` (enum)   | Determines the property's behavior. Possible values include:<br>`"checkbox"`, `"created_by"`, `"created_time"`, `"date"`, `"email"`, `"files"`, `"formula"`,<br>`"last_edited_by"`, `"last_edited_time"`, `"multi_select"`, `"number"`, `"people"`, `"phone_number"`, `"relation"`, `"rich_text"`, `"rollup"`, `"select"`, `"status"`, `"title"`, `"url"` | `"rich_text"`              |
| **Type Object** | Depends on `type` | Contains type-specific configuration. The key corresponds to the property's `type`, and the value holds the configuration details.                                                   | See individual property type sections below. |

### Checkbox

A **checkbox** database property is rendered in the Notion UI as a column that contains checkboxes. The `checkbox` type object is empty; there is no additional property configuration.

**Example checkbox database property object**:

```json
"Task complete": {
  "id": "BBla",
  "name": "Task complete",
  "type": "checkbox",
  "checkbox": {}
}
```

### Created by

A **created_by** database property is rendered in the Notion UI as a column that contains people mentions of each row's author as values. The `created_by` type object is empty. There is no additional property configuration.

**Example created by database property object**:

```json
"Created by": {
   "id": "%5BJCR",
   "name": "Created by",
   "type": "created_by",
   "created_by": {}
}
```

### Created time

A **created_time** database property is rendered in the Notion UI as a column that contains timestamps of when each row was created as values. The `created_time` type object is empty. There is no additional property configuration.

**Example created time database property object**:

```json
"Created time": {
  "id": "XcAf",
  "name": "Created time",
  "type": "created_time",
  "created_time": {}
}
```

### Date

A **date** database property is rendered in the Notion UI as a column that contains date values. The `date` type object is empty; there is no additional configuration.

**Example date database property object**:

```json
"Task due date": {
  "id": "AJP%7D",
  "name": "Task due date",
  "type": "date",
  "date": {}
}
```

### Email

An **email** database property is represented in the Notion UI as a column that contains email values. The `email` type object is empty. There is no additional property configuration.

**Example email database property object**:

```json
"Contact email": {
  "id": "oZbC",
  "name": "Contact email",
  "type": "email",
  "email": {}
}
```

### Files

> **Note:**  
> The Notion API does not yet support uploading files to Notion.

A **files** database property is rendered in the Notion UI as a column that has values that are either files uploaded directly to Notion or external links to files. The `files` type object is empty; there is no additional configuration.

**Example files database property object**:

```json
"Product image": {
  "id": "pb%3E%5B",
  "name": "Product image",
  "type": "files",
  "files": {}
}
```

### Formula

A **formula** database property is rendered in the Notion UI as a column that contains values derived from a provided expression. The `formula` type object defines the expression in the following field:

| Field       | Type   | Description                                                   | Example value                                                                                   |
|-------------|--------|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| expression  | string | The formula that is used to compute the values for this property. Refer to the Notion help center for information about formula syntax. | `{{notion:block_property:BtVS:00000000-0000-0000-0000-000000000000:8994905a-074a-415f-9bcf-d1f8b4fa38e4}}/2` |

**Example formula database property object**:

```json
"Updated price": {
  "id": "YU%7C%40",
  "name": "Updated price",
  "type": "formula",
  "formula": {
    "expression": "{{notion:block_property:BtVS:00000000-0000-0000-0000-000000000000:8994905a-074a-415f-9bcf-d1f8b4fa38e4}}/2"
  }
}
```

### Last edited by

A **last_edited_by** database property is rendered in the Notion UI as a column that contains people mentions of the person who last edited each row as values. The `last_edited_by` type object is empty. There is no additional property configuration.

### Last edited time

A **last_edited_time** database property is rendered in the Notion UI as a column that contains timestamps of when each row was last edited as values. The `last_edited_time` type object is empty. There is no additional property configuration.

**Example last edited time database property object**:

```json
"Last edited time": {
  "id": "jGdo",
  "name": "Last edited time",
  "type": "last_edited_time",
  "last_edited_time": {}
}
```

### Multi-select

A **multi_select** database property is rendered in the Notion UI as a column that contains values from a range of options. Each row can contain one or multiple options.

The `multi_select` type object includes an array of `options` objects. Each option object details settings for the option, indicating the following fields:

| Field | Type   | Description                                                                                                                                                                                | Example value                                              |
|-------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| color | string (enum) | The color of the option as rendered in the Notion UI. Possible values include `blue`, `brown`, `default`, `gray`, `green`, `orange`, `pink`, `purple`, `red`, `yellow`               | `"blue"`                                                   |
| id    | string | An identifier for the option, which does not change if the name is changed. An id is sometimes, but not always, a UUID.                                                                    | `"ff8e9269-9579-47f7-8f6e-83a84716863c"`                   |
| name  | string | The name of the option as it appears in Notion. <br><br>**Note**: Commas (",") are not valid for multi-select properties.                                                                   | `"Fruit"`                                                 |

**Example multi-select database property**:

```json
"Store availability": {
  "id": "flsb",
  "name": "Store availability",
  "type": "multi_select",
  "multi_select": {
    "options": [
      {
        "id": "5de29601-9c24-4b04-8629-0bca891c5120",
        "name": "Duc Loi Market",
        "color": "blue"
      },
      {
        "id": "385890b8-fe15-421b-b214-b02959b0f8d9",
        "name": "Rainbow Grocery",
        "color": "gray"
      },
      {
        "id": "72ac0a6c-9e00-4e8c-80c5-720e4373e0b9",
        "name": "Nijiya Market",
        "color": "purple"
      },
      {
        "id": "9556a8f7-f4b0-4e11-b277-f0af1f8c9490",
        "name": "Gus's Community Market",
        "color": "yellow"
      }
    ]
  }
}
```

### Number

A **number** database property is rendered in the Notion UI as a column that contains numeric values. The `number` type object contains the following field:

| Field  | Type          | Description                                                                                                   | Example value |
|--------|--------------|---------------------------------------------------------------------------------------------------------------|--------------|
| format | string (enum) | The way that the number is displayed in Notion. Possible values include `number`, `number_with_commas`, `percent`, currency formats (`dollar`, `euro`, etc.), and more. See the full list in the docs. | `"percent"`   |

**Example number database property object**:

```json
"Price": {
  "id": "%7B%5D_P",
  "name": "Price",
  "type": "number",
  "number": {
    "format": "dollar"
  }
}
```

### People

A **people** database property is rendered in the Notion UI as a column that contains people mentions. The `people` type object is empty; there is no additional configuration.

**Example people database property object**:

```json
"Project owner": {
  "id": "FlgQ",
  "name": "Project owner",
  "type": "people",
  "people": {}
}
```

### Phone number

A **phone_number** database property is rendered in the Notion UI as a column that contains phone number values. The `phone_number` type object is empty. There is no additional property configuration.

**Example phone number database property object**:

```json
"Contact phone number": {
  "id": "ULHa",
  "name": "Contact phone number",
  "type": "phone_number",
  "phone_number": {}
}
```

### Relation

A **relation** database property is rendered in the Notion UI as a column that contains references (links) to pages in another database. The `relation` type object contains the following fields:

| Field                 | Type   | Description                                                                                                                               | Example value                               |
|-----------------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| database_id           | string (UUID) | The database that the relation property refers to. The corresponding linked page values must belong to the database in order to be valid. | `"668d797c-76fa-4934-9b05-ad288df2d136"`    |
| synced_property_id    | string | The id of the corresponding property that is updated in the related database when this property is changed.                               | `"fy:{"`                                    |
| synced_property_name  | string | The name of the corresponding property that is updated in the related database when this property is changed.                              | `"Ingredients"`                             |

**Example relation database property object**:

```json
"Projects": {
  "id": "~pex",
  "name": "Projects",
  "type": "relation",
  "relation": {
    "database_id": "6c4240a9-a3ce-413e-9fd0-8a51a4d0a49b",
    "synced_property_name": "Tasks",
    "synced_property_id": "JU]K"
  }
}
```

> **Note**  
> **Database relations must be shared with your integration**  
> To retrieve properties from database relations, the related database must be shared with your integration in addition to the database being retrieved. If the related database is not shared, properties based on relations will not be included in the API response.  
> Similarly, to update a database relation property via the API, share the related database with the integration.

### Rich text

A **rich_text** database property is rendered in the Notion UI as a column that contains text values. The `rich_text` type object is empty; there is no additional configuration.

**Example rich text database property object**:

```json
"Project description": {
  "id": "NZZ%3B",
  "name": "Project description",
  "type": "rich_text",
  "rich_text": {}
}
```

### Rollup

A **rollup** database property is rendered in the Notion UI as a column with values that are rollups, specific properties that are pulled from a related database.

The `rollup` type object contains the following fields:

| Field                   | Type   | Description                                                                                                                 | Example value                      |
|-------------------------|--------|-----------------------------------------------------------------------------------------------------------------------------|------------------------------------|
| function                | string (enum) | The function that computes the rollup value from the related pages.<br><br>Possible values include `"sum"`, `"count"`, `"unique"`, `"show_original"`, etc.                            | `"sum"`                             |
| relation_property_id    | string | The id of the related database property that is rolled up.                                                                 | `"fy:{"`                           |
| relation_property_name  | string | The name of the related database property that is rolled up.                                                               | `"Tasks"`                          |
| rollup_property_id      | string | The id of the rollup property.                                                                                             | `"fy:{"`                           |
| rollup_property_name    | string | The name of the rollup property.                                                                                           | `"Days to complete"`               |

**Example rollup database property object**:

```json
"Estimated total project time": {
  "id": "%5E%7Cy%3C",
  "name": "Estimated total project time",
  "type": "rollup",
  "rollup": {
    "rollup_property_name": "Days to complete",
    "relation_property_name": "Tasks",
    "rollup_property_id": "\\nyY",
    "relation_property_id": "Y]<y",
    "function": "sum"
  }
}
```

### Select

A **select** database property is rendered in the Notion UI as a column that contains values from a selection of options. Only one option is allowed per row. The `select` type object contains an array of objects representing the available options. Each option object includes the following fields:

| Field | Type           | Description                                                                                                                                                             | Example value                                               |
|-------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| color | string (enum) | The color of the option as rendered in the Notion UI. Possible values include: `blue`, `brown`, `default`, `gray`, `green`, `orange`, `pink`, `purple`, `red`, `yellow`. | `"red"`                                                     |
| id    | string        | An identifier for the option. It doesn't change if the name is changed. These are sometimes, but not always, UUIDs.                                                     | `"ff8e9269-9579-47f7-8f6e-83a84716863c"`                    |
| name  | string        | The name of the option as it appears in the Notion UI.<br><br>**Note:** Commas (",") are not valid for select values.                                                   | `"Fruit"`                                                   |

**Example select database property object**:

```json
"Food group": {
  "id": "%40Q%5BM",
  "name": "Food group",
  "type": "select",
  "select": {
    "options": [
      {
        "id": "e28f74fc-83a7-4469-8435-27eb18f9f9de",
        "name": "🥦Vegetable",
        "color": "purple"
      },
      {
        "id": "6132d771-b283-4cd9-ba44-b1ed30477c7f",
        "name": "🍎Fruit",
        "color": "red"
      },
      {
        "id": "fc9ea861-820b-4f2b-bc32-44ed9eca873c",
        "name": "💪Protein",
        "color": "yellow"
      }
    ]
  }
}
```

### Status

A **status** database property is rendered in the Notion UI as a column that contains values from a list of status options. The `status` type object includes an array of `options` objects and an array of `groups` objects.

- The **`options`** array is a **sorted list** of the available status options for the property. Each option object has the following fields:

  | Field | Type           | Description                                                                                                                                                             | Example value                                                 |
  |-------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
  | color | string (enum) | The color of the option as rendered in the Notion UI. Possible values include `blue`, `brown`, `default`, `gray`, `green`, `orange`, `pink`, `purple`, `red`, `yellow`. | `"green"`                                                     |
  | id    | string        | An identifier for the option. The id does not change if the name is changed. It is sometimes, but not always, a UUID.                                                   | `"ff8e9269-9579-47f7-8f6e-83a84716863c"`                      |
  | name  | string        | The name of the option as it appears in the Notion UI.<br><br>**Note:** Commas (",") are not valid for status values.                                                   | `"In progress"`                                               |

- A **`group`** is a collection of options. The `groups` array is a sorted list of the available groups for the property. Each group object in the array has the following fields:

  | Field      | Type           | Description                                                                                                                                                             | Example value                                                 |
  |------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
  | color      | string (enum) | The color of the option as rendered in the Notion UI. Possible values include `blue`, `brown`, `default`, `gray`, `green`, `orange`, `pink`, `purple`, `red`, `yellow`. | `"purple"`                                                    |
  | id         | string        | An identifier for the option. The id does not change if the name is changed. It is sometimes, but not always, a UUID.                                                   | `"ff8e9269-9579-47f7-8f6e-83a84716863c"`                      |
  | name       | string        | The name of the option as it appears in the Notion UI.<br><br>**Note:** Commas (",") are not valid for status values.                                                   | `"To do"`                                                     |
  | option_ids | array of strings (UUID) | A sorted list of ids of all of the options that belong to a group.                                                                                                                | Refer to example.                                             |

**Example status database property object**:

```json
"Status": {
  "id": "biOx",
  "name": "Status",
  "type": "status",
  "status": {
    "options": [
      {
        "id": "034ece9a-384d-4d1f-97f7-7f685b29ae9b",
        "name": "Not started",
        "color": "default"
      },
      {
        "id": "330aeafb-598c-4e1c-bc13-1148aa5963d3",
        "name": "In progress",
        "color": "blue"
      },
      {
        "id": "497e64fb-01e2-41ef-ae2d-8a87a3bb51da",
        "name": "Done",
        "color": "green"
      }
    ],
    "groups": [
      {
        "id": "b9d42483-e576-4858-a26f-ed940a5f678f",
        "name": "To-do",
        "color": "gray",
        "option_ids": [
          "034ece9a-384d-4d1f-97f7-7f685b29ae9b"
        ]
      },
      {
        "id": "cf4952eb-1265-46ec-86ab-4bded4fa2e3b",
        "name": "In progress",
        "color": "blue",
        "option_ids": [
          "330aeafb-598c-4e1c-bc13-1148aa5963d3"
        ]
      },
      {
        "id": "4fa7348e-ae74-46d9-9585-e773caca6f40",
        "name": "Complete",
        "color": "green",
        "option_ids": [
          "497e64fb-01e2-41ef-ae2d-8a87a3bb51da"
        ]
      }
    ]
  }
}
```

> **Note:**  
> It is **not possible** to update a status database property's name or option values via the API. Update these values from the Notion UI instead.

### Title

A **title** database property controls the title that appears at the top of a page when a database row is opened. The `title` type object itself is empty; there is no additional configuration.

**Example title database property object**:

```json
"Project name": {
  "id": "title",
  "name": "Project name",
  "type": "title",
  "title": {}
}
```

> **Note:**  
> All databases require **one**, and only one, title property. The API throws errors if you send a request to **Create a database** without a title property, or if you attempt to **Update a database** to add or remove a title property.
> **Note:**  
> **Title database property vs. database title**  
>
> - A **title database property** is a type of column in a database.
> - A **database title** defines the title of the database itself and is found on the database object.  
> Every database requires both a database title and a title database property.

### URL

A **url** database property is represented in the Notion UI as a column that contains URL values. The `url` type object is empty. There is no additional property configuration.

**Example URL database property object**:

```json
"Project URL": {
  "id": "BZKU",
  "name": "Project URL",
  "type": "url",
  "url": {}
}
```

---

## Working with databases

### Overview

Databases are collections of pages in a Notion workspace that can be filtered, sorted, and organized as needed. They allow users to create and manipulate structured data in Notion.

Integrations can be used to help users sync databases with external systems or build workflows around Notion databases.

In this guide, you'll learn:

- How databases are represented in the API.
- How to add items to a database.
- How to find items within databases.

### Additional types of databases

In addition to regular Notion databases, there are two other types of databases to be aware of. Neither of these database types are currently supported by the Public API.

#### Linked databases

Notion offers linked databases as a way of showing databases in multiple places. You can identify them by a ↗ next to the database title which, when clicked, takes you to the source database.

> **Note:**  
> The Public API does **not** currently support linked databases. When sharing a database with your integration, make sure it's the source one!

#### Wiki databases

Wiki databases are a special category of databases that allow Workspace Owners to organize child pages and databases with a homepage view. Wiki database pages can be verified by the Workspace Owner with an optional expiration date for the verification.

Pages in a wiki database will have a `verification` property that can be set through your Notion workspace. 

> **Note:**  
> Wiki databases can currently only be created through your Notion workspace directly (i.e., not the Public API).  
> For more info on wikis and verified pages, see [Wikis and verified pages](https://www.notion.so/help/wikis-and-verified-pages) and [Wiki guides](https://www.notion.so/help/wiki-guides).

### Structure

Database objects describe a part of what a user sees in Notion when they open a database. (See our documentation on [database objects](#database-object) and [database properties](#database-properties) for a complete description.)

The most important part is the database's **schema**, defined in the `properties` collection.

> **Note:**  
> The columns of a Notion database are referred to as its “properties” or “schema”.

Example (JavaScript):

```js
{
  "object": "database",

  "id": "2f26ee68-df30-4251-aad4-8ddc420cba3d",
  "created_time": "2020-03-17T19:10:04.968Z",
  "last_edited_time": "2020-03-17T21:49:37.913Z",
  "title": [/* details omitted */],
  "description": [/* details omitted */],

  "properties": {/* a collection of property objects */},
  "archived": false,
  "in_trash": false,
  "is_inline": false,
  "public_url": null
}
```

> **Note:**  
> **Maximum schema size recommendation**  
> Notion recommends a maximum schema size of 50KB. Updates to database schemas that are too large will be blocked to help maintain database performance.

### Database properties example

Imagine a database with three properties: **Grocery item**, **Price**, **Last ordered**.

```js
{
  "object": "database",
  
  "properties": {
    "Grocery item": {
      "id": "fy:{",
      "type": "title",
      "title": {}
    },
    "Price": {
      "id": "dia[",
      "type": "number",
      "number": {
        "format": "dollar"
      }
    },
    "Last ordered": {
      "id": "]\\R[",
      "type": "date",
      "date": {}
    }
  }
  // remaining details omitted
}
```

Here are some key takeaways:

1. The `"title"` type is special. Every database has exactly one property with the `"title"` type. This property corresponds to the page title for each item in the database.
2. The value of `type` corresponds to another key in the property object. Each property object has a nested property named the same as its `type` value. For example, `Last ordered` has the type `"date"`, and it also has a `date` property.
3. Certain property object types have additional configuration. In this example, `Price` has the type `"number"`. Number property objects have additional configuration inside the `number` property. In this example, the `format` is set to `"dollar"`.

### Iterate over a database object

A query to [Retrieve a database](https://developers.notion.com/reference/get-database) returns a database object. You can iterate over the `properties` object in the response to list information about each property. For example:

```js
Object.entries(database.properties).forEach(([propertyName, propertyValue]) => {
    console.log(`${propertyName}: ${propertyValue.type}`);
});
```

### Adding pages to a database

Pages are used as items inside a database, and each page's properties must conform to its parent database's schema. In other words, if you're viewing a database as a table, a page's properties define all the values in a single row.

> **Note:**  
> If you are creating a page in a database, the page properties must match the properties of the database. If you are creating a page that is not a child of a database, `title` is the only property that can be set.

Pages are added to a database using the [Create a page](https://developers.notion.com/reference/post-page) API endpoint. Let's try to add a page to the example database above.

The **Create a page** endpoint has two required parameters:

- `parent`
- `properties`

When adding a page to a database, the `parent` parameter must be a database parent. For example:

```json
{
  "type": "database_id",
  "database_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d"
}
```

> **Permissions**  
> Before an integration can create a page within a database, it needs access to the database. To share a database with an integration, click the ••• menu at the top right of the database page, scroll to **Add connections**, and select the integration.
> **Where can I find my database's ID?**  
> Open the database as a full page in Notion. Use the **Share** menu to **Copy link**, then paste the link. The URL has the format:  
> `https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`  
> The `{database_id}` is a 36-character long string. This is your database ID (hyphens or no hyphens both work when calling the API).

The `properties` parameter is an object which uses property names or IDs as keys, and **property value objects** as values. To create this parameter correctly, we refer to the property objects in the database's schema. For example:

```json
{
  "Grocery item": {
    "type": "title",
    "title": [
      { "type": "text", "text": { "content": "Tomatoes" } }
    ]
  },
  "Price": {
    "type": "number",
    "number": 1.49
  },
  "Last ordered": {
    "type": "date",
    "date": { "start": "2021-05-11" }
  }
}
```

> **Building a property value object in code**  
> Building the property value object manually is only helpful when you're working with one specific database that you know about ahead of time. In order to build an integration that works with **any** database, use the [Retrieve a database](https://developers.notion.com/reference/get-database) endpoint. Your integration can call this endpoint to get a current database schema, then construct the `properties` parameter dynamically.

Finally, we combine both parameters in our request to **Create a page**:

**cURL** example:

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "parent": {
      "type": "database_id",
      "database_id": "2f26ee68-df30-4251-aad4-8ddc420cba3d"
    },
    "properties": {
      "Grocery item": {
        "type": "title",
        "title": [
          { "type": "text", "text": { "content": "Tomatoes" } }
        ]
      },
      "Price": {
        "type": "number",
        "number": 1.49
      },
      "Last ordered": {
        "type": "date",
        "date": { "start": "2021-05-11" }
      }
    }
  }'
```

Once the page is added, you'll receive a response containing the new **page object**. An important property in the response is the page ID (`id`). If you're connecting Notion to an external system, store this page ID so that you can update page properties later using the [Update page properties](https://developers.notion.com/reference/patch-page) endpoint.

### Finding pages in a database

Pages can be read from a database using the [Query a database](https://developers.notion.com/reference/post-database-query) endpoint. This endpoint allows you to find pages based on criteria such as "which page has the most recent Last ordered date?" Some databases can be very large, so this endpoint also allows you to get results in a specific order and retrieve results in smaller batches.

> **Getting a specific page**  
> If you're looking for one specific page and already have its page ID, you don't need to query a database to find it. Instead, use the [Retrieve a page](https://developers.notion.com/reference/get-page) endpoint.

#### Filtering database pages

The criteria used to find pages are called **filters**. Filters can describe simple conditions (i.e., `"Tag includes Urgent"`) or more complex conditions (i.e., `"Tag includes Urgent AND Due date is within the next week AND Assignee equals Cassandra Vasquez"`). These more complex conditions are called **compound filters** because they use `"and"` or `"or"` to join multiple single property conditions.

> **Finding all pages in a database**  
> To find all the pages in a database, call **Query a database** without a filter parameter.

For example, using our schema above, the **Last ordered** property is of type `"date"`. We can build a filter that says **Last ordered** date is in the past week:

```json
{
  "property": "Last ordered",
  "date": {
    "past_week": {}
  }
}
```

We can pass this filter to the **Query a database** endpoint:

**cURL**:

```bash
curl -X POST https://api.notion.com/v1/databases/2f26ee68df304251aad48ddc420cba3d/query \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "filter": {
      "property": "Last ordered",
      "date": {
        "past_week": {}
      }
    }
  }'
```

You'll receive a response that contains a list of matching **page objects**:

```json
{
  "object": "list",
  "results": [
    {
      "object": "page",
      /* details omitted */
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

This is a **paginated** response. The maximum number of results in one response is 100. The [pagination reference](https://developers.notion.com/reference/pagination) explains how to use the `"start_cursor"` and `"page_size"` parameters to get more than 100 results.

#### Sorting database pages

If you want the results in a specific order, such as "most recently created" first, you can use the `sorts` parameter, which is an array of sort objects.

The time a page was created is not a page property (which must conform to the database schema); it’s one of two page timestamps. Specifically, it's called the `"created_time"` timestamp. We can build a sort object for `"created_time"`:

```json
{
  "timestamp": "created_time",
  "direction": "descending"
}
```

We can update our **Query a database** request to include this sort:

```bash
curl -X POST https://api.notion.com/v1/databases/2f26ee68df304251aad48ddc420cba3d/query \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
    "filter": {
      "property": "Last ordered",
      "date": {
        "past_week": {}
      }
    },
    "sorts": [
      { "timestamp": "created_time", "direction": "descending" }
    ]
  }'
```

### Conclusion

Understanding **database schemas** (made from a collection of database properties) is key to working with Notion databases. This enables you to add pages to a database and also find items in a database.

You're ready to help users take advantage of Notion's flexible and extensible database interface to work with structured data. There's more to learn and do with databases in the resources below.

### Next steps

- This guide explains working with page properties. Also see [working with page content](https://developers.notion.com/docs/working-with-page-content).
- Explore the [database object](https://developers.notion.com/reference/database) to see other kinds of information about databases available in the API.
- Learn more about the other [page property value types](https://developers.notion.com/docs/page-property-values). In particular, you can do more with **rich text**.
- Learn more about [pagination](https://developers.notion.com/reference/pagination) to handle large databases efficiently.
