<template>
  <div>
    <div class="header">
      <h3>Welcome {{ account }}</h3>
      <div class="header-links">
        <router-link to="/" class="link add-button">Add</router-link>
        <router-link :to="{path: '/delete', query: {account: account}}" class="link delete-button">Delete</router-link>
        <router-link to="/edit" class="link">Edit</router-link>
      </div>
    </div>

    <div class="search-container">
      <input type="text" class="search-bar" v-model="searchQuery" placeholder="Search...">
    </div>
    <the-table :entities="filteredEntities"></the-table>
  </div>
</template>

<script>
import TheTable from "@/components/TheTable";

export default {
  components: {TheTable},
  data() {
    return {
      account: '',
      entities: [],
      searchQuery: ''
    };
  },
  mounted() {
    this.fetchEntities();
  },
  created() {
    // Access the userName from the route's query parameters
    this.account = this.$route.query.account || 'Guest';
  },
  methods: {
    fetchEntities() {
      // Make a GET request to your backend endpoint
      fetch('http://127.0.0.1:8000/all-entities')
          .then(response => response.json())
          .then(data => {
            this.entities = data;
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    }
  },
  computed: {
    filteredEntities() {
      // Filter entities based on search term
      return this.entities.filter((entity) => {
        return (
            entity.name.toLowerCase().startsWith(this.searchQuery.toLowerCase()) ||
            entity.email.toLowerCase().startsWith(this.searchQuery.toLowerCase()) ||
            entity.location.toLowerCase().startsWith(this.searchQuery.toLowerCase()) ||
            entity.location.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      });
    },
  },
  name: "TheList"
}
</script>

<style scoped>
.header {
  background-color: #45217a;
  color: #fff;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h3 {
  margin: 0;
}

.header-links .link {
  color: #fff;
  text-decoration: none;
  margin-left: 10px;
  padding: 8px 15px;
  border-radius: 20px;
  background-color: #5c6bc0;
  transition: background-color 0.3s ease;
  font-weight: bold;
  border: 2px solid #5c6bc0;
  transition: all 0.3s ease;
}

.header-links .link:hover {
  background-color: #3949ab;
  border-color: #3949ab;
  transform: scale(1.05);
}

.link.add-button {
  background-color: #2196f3;
}

.link.delete-button {
  background-color: #f44336;
}

.link.edit-button {
  background-color: #4caf50;
}

.search-container {
  display: flex;
  justify-content: center;
}

.search-bar {
  display: flex;
  justify-content: center;
  margin: 20px; /* Adjust margin as needed */
  width: 30rem; /* Adjust width as needed */
  background-color: #f0f0f0;
  border-radius: 50px;
  padding: 10px;
  border: none;
  outline: none;
  font-size: 16px;
}
</style>
