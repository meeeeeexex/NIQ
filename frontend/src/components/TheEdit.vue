<template>
  <div>
    <div class="header">
      <h3>Welcome {{ account }}</h3>
      <div class="header-links">
        <router-link to="/main" class="link">Back to main</router-link>
      </div>
    </div>
    <the-table :entities="entities"></the-table>
  </div>
</template>

<script>
import TheTable from "@/components/TheTable";

export default {
  name: "TheEdit",
  components: {TheTable},
  data() {
    return {
      account: '',
      entities: []
    };
  },
  mounted() {
    this.fetchEntities();
  },
  created() {
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
}
</script>
