# Steps To Run project
- Run python manage.py loaddata  /your_path/fixtures.json
- Run project python manage.py runserver
    * http://localhost:8000/graphql
    
## Queries

<code> 

- query {
  allIngredients{
    id,
    name,
    notes,
    category{
      id
    }
  }
}

- query {
   categoryByName(name:"testing"){
     id, 
    name
  }
}

- query hello

- mutation {
  createIngredient(input: {name: "testing2", notes: "Testing Notes 2", category: {id: 1}}) {
    ok
    ingredient {
      id
      name
      notes
      category {
        id
      }
    }
  }
}

- mutation {
  updateIngredient(input: {id: 6 , name: "updated testing2", notes: "Updated Testing Notes 2", category: {id: 2}}) {
    ok
    ingredient {
      id
      name
      notes
      category {
        id
      }
    }
  }
}

- mutation {
  createCategory(input : {name: "category1"}){
    ok,
    category{
       id,
      name
    }
  }
}

- mutation {
  updateCategory(id:5,name:"updated3"){
    ok,
    category{
      id,
      name
    }
  }
}


</code>

![Operation image](https://github.com/abhi904485/graphql_with_django/blob/master/graphql.png?raw=true)