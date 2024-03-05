<template>
  <div>
    <div class="header">
      <h3>Welcome {{ account }}</h3>
      <div class="header-links">
        <router-link to="/main" class="link">Back to main</router-link>
      </div>
    </div>

    <div class="container">
      <div class="table-container">
        <table class="data-table">
          <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>Email</th>
            <th>Weather</th>
            <th>Min Month</th>
            <th>Max Month</th>
            <th>Avg Month</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(entity, index) in entities" :key="index">
            <td><input type="checkbox" v-model="selectedRows" :value="entity.id" @click="selectRow(entity)"></td>
            <td>{{ entity.name }}</td>
            <td>{{ entity.email }}</td>
            <td>{{ entity.weather }}</td>
            <td>{{ entity.min_month }}</td>
            <td>{{ entity.max_month }}</td>
            <td>{{ entity.avg_month }}</td>
          </tr>
          </tbody>

        </table>
      </div>
    </div>
    <div class="button-container">
      <button class="delete-button" @click="deleteSelectedRows">Delete Selected Rows</button>
    </div>
  </div>
</template>

<script>


export default {
  name: "TheDelete",


  data() {
    return {
      account: '',
      entities: [],
      selectedRows: []
    };
  },

  created() {
    // Access the userName from the route's query parameters
    this.account = this.$route.query.account || 'Guest';
  },

  mounted() {
    this.fetchEntities();
  },

  methods: {
    fetchEntities() {
      // Make a GET request to your backend endpoint
      fetch('http://127.0.0.1:8000/entities-by-account/' + this.account)
          .then(response => response.json())
          .then(data => {
            this.entities = data;
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },

    selectRow(entity) {
      if (!this.selectedRows.includes(entity.id)) {
        this.selectedRows.push(entity.id);
      } else {
        this.selectedRows = this.selectedRows.filter(rowId => rowId !== entity.id);
      }
    },

    deleteSelectedRows() {
      this.selectedRows.forEach(selectedRow => {

        fetch(`http://127.0.0.1:8000/delete-entity/${selectedRow}`, {
          method: 'DELETE',
        })
            .then(response => {
              if (response.ok) {
                this.entities = this.entities.filter(entity => entity.id !== selectedRow);
              }
            })
            .catch(error => {
              console.error('Error deleting row:', error);
            });
      });

      this.selectedRows = [];
    }

  }
};
</script>

<style scoped>
.header {
  background-color: #45217a;
  color: #fff;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 50px; /* Add margin bottom to create space */

}

.header h3 {
  margin: 0;
}

.header-links .link {
  color: #fff;
  text-decoration: none;
  margin-left: 10px;
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #5c6bc0;
  transition: background-color 0.3s ease;
}

.header-links .link:hover {
  background-color: #3949ab;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.table-container {
  overflow-x: auto;
}

.data-table {
  margin-top: 20px;
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 15px 20px;
  border: 1px solid #ddd;
}

.data-table th {
  background-color: #f2f2f2;
  font-weight: bold;
  color: #555;
  text-align: left;
}

.data-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.data-table tbody tr:hover {
  background-color: #f0f0f0;
  transition: background-color 0.3s ease;
}
.button-container {
  /* Center the button */
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.delete-button {
  background-color: #45217a;
  color: #fff;
  font-size: 15px;
  padding: 20px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-button:hover {
  background-color: #2b0b5b;
}
</style>
