<template>
  <div class="container">
    <div class="table-container">
      <table class="data-table">
        <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Location</th>
          <th>Weather</th>
          <th>Min Month</th>
          <th>Max Month</th>
          <th>Avg Month</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(entity, index) in entities" :key="index">
          <td>{{ entity.name }}</td>
          <td>{{ entity.email }}</td>
          <td>{{ entity.location }}</td>
          <td>{{ entity.weather }}</td>
          <td>{{ entity.min_month }}</td>
          <td>{{ entity.max_month }}</td>
          <td>{{ entity.avg_month }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script>
export default {
  name: "TheTable",
  props: {
    entities: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>

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
</style>