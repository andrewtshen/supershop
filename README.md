# supershop
Super Shopping or something

### Tools
- Flask - Python webserver stuff
- SQL-Alchemy - SQL Database management
- Bulma - CSS stuff
- Jinja - HTML Variable Processing/Rendering

### Routes
- `/profile` - Default user homepage
- `/shoppinglist` - Shopping list information, automatically add expiration date or manual, FUNCTIONALITY: add new item, remove item, mark item as purchased, send it to inventory [POST] `/inventory`
- `/shoppinglist/newitem/` - [GET] Form to add new item to shopping list FUNCTIONALITY: drop down list for new items, [POST] Submit information to be added to shopping list
- `/inventory` - Shows what the user already bought + expiration date, manually be able to add/remove items 

### Extension
- Export shopping list to grocery store (COSTCO, Stop & Shop)
- Export to meal planner website
- Calender reminders
- Nutritional Data (in inventory/shopping list)

### Data Format
```
json file format

data = {
  "users": {
    "id": {
      "email": email@email.com,
      "firstName": "John",
      "lastName": "Smith",
      "groups": {
         "groupid": 0,
         "groupid1": 1,
      },
    },
  }

  "shoppinglists": {
    "shoppinglist_id": {
      item: {
        "name": null,
        "quantity": null,
        "expirationDate": 20210123,
      },
      item1: {...},
    }
  }
  "inventories": {
    "inventory_id": {
      "item": {...},
      "item1": {...},
    }
  }
}
```
